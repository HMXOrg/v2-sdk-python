from web3 import Web3, Account
from web3.middleware.signing import construct_sign_and_send_raw_middleware
from web3.logs import DISCARD
from time import sleep
from hmx2.constants.contracts import (
  CROSS_MARGIN_HANDLER_ABI_PATH,
  LIMIT_TRADE_HANDLER_ABI_PATH,
  VAULT_STORAGE_ABI_PATH,
  PERP_STORAGE_ABI_PATH,
  CONFIG_STORAGE_ABI_PATH,
  ERC20_ABI_PATH,
  CALCULATOR_ABI_PATH
)
from hmx2.constants.common import (
  ADDRESS_ZERO,
  MAX_UINT,
  EXECUTION_FEE,
  BPS,
)
from hmx2.enum import Cmd
from hmx2.helpers.contract_loader import load_contract
from simple_multicall_v6 import Multicall
from hmx2.helpers.mapper import (
  get_contract_address,
  get_token_profile,
  get_collateral_address_asset_map,
  get_collateral_address_list
)
from hmx2.modules.oracle.oracle_middleware import OracleMiddleware
from eth_abi.abi import encode
import decimal

decimal.getcontext().prec = 15
decimal.getcontext().rounding = "ROUND_HALF_DOWN"


class Private(object):

  def __init__(self, chain_id: int, eth_provider: Web3,
               eth_signer: Account, oracle_middleware: OracleMiddleware):
    self.chain_id = chain_id
    self.eth_provider = eth_provider
    self.eth_signer = eth_signer
    self.oracle_middleware = oracle_middleware
    self.eth_provider.middleware_onion.add(
      construct_sign_and_send_raw_middleware(self.eth_signer))
    self.contract_address = get_contract_address(chain_id)
    self.collateral_address_asset_map = get_collateral_address_asset_map(
      chain_id)
    self.collateral_address_list = get_collateral_address_list(chain_id)
    self.token_profile = get_token_profile(chain_id)
    # load contract
    self.limit_trade_handler_instance = load_contract(
      self.eth_provider, self.contract_address["LIMIT_TRADE_HANDLER_ADDRESS"], LIMIT_TRADE_HANDLER_ABI_PATH)
    self.perp_storage_instance = load_contract(
      self.eth_provider, self.contract_address["PERP_STORAGE_ADDRESS"], PERP_STORAGE_ABI_PATH)
    self.config_storage_instance = load_contract(
      self.eth_provider, self.contract_address["CONFIG_STORAGE_ADDRESS"], CONFIG_STORAGE_ABI_PATH)
    self.vault_storage_instance = load_contract(
      self.eth_provider, self.contract_address["VAULT_STORAGE_ADDRESS"], VAULT_STORAGE_ABI_PATH)
    self.cross_margin_handler_instance = load_contract(
      self.eth_provider, self.contract_address["CROSS_MARGIN_HANDLER_ADDRESS"], CROSS_MARGIN_HANDLER_ABI_PATH)
    self.calculator_instance = load_contract(
      self.eth_provider, self.contract_address["CALCULATOR_ADDRESS"], CALCULATOR_ABI_PATH
    )
    self.multicall_instance = Multicall(w3=self.eth_provider,
                                        custom_address=self.contract_address["MULTICALL_ADDRESS"])

  def get_public_address(self):
    '''
    Get the public address of the signer.
    '''
    return self.eth_signer.address

  def get_collaterals(self, sub_account_id: int):
    self.__check_sub_account_id_param(sub_account_id)

    calls = [
      self.multicall_instance.create_call(
        self.vault_storage_instance,
          "traderBalances",
          [self.eth_signer.address, collateral],
      )
      for collateral in self.collateral_address_list
    ]
    collateral_usd = [
      self.oracle_middleware.get_price(
        self.collateral_address_asset_map[collateral])
      for collateral in self.collateral_address_list
    ]

    results = self.multicall_instance.call(calls)

    ret = {}
    for index, collateral in enumerate(self.collateral_address_list):
      amount = int(
          results[1][index].hex(), 16) / 10 ** self.token_profile[collateral]["decimals"]
      ret[self.token_profile[collateral]["symbol"]] = {
        'amount': amount,
        'value_usd': amount * collateral_usd[index]
      }

    return ret

  def deposit_erc20_collateral(self, sub_account_id: int, token_address: str, amount: float):
    '''
    Deposit ERC20 token as collateral.

    :param sub_account_id: required
    :type sub_account_id: int between 0 and 255

    :param token_address: required
    :type token_address: str in list COLLATERALS

    :param amount: required
    :type amount: float
    '''
    if token_address not in self.collateral_address_list:
      raise Exception("Invalid collateral address")
    self.__check_sub_account_id_param(sub_account_id)

    amount_wei = int(
      amount * 10 ** self.token_profile[token_address]["decimals"])
    token_instance = load_contract(
      self.eth_provider, token_address, ERC20_ABI_PATH)

    CROSS_MARGIN_HANDLER_ADDRESS = self.contract_address["CROSS_MARGIN_HANDLER_ADDRESS"]

    allowance = token_instance.functions.allowance(
        self.eth_signer.address, CROSS_MARGIN_HANDLER_ADDRESS).call()
    if allowance < amount_wei:
      token_instance.functions.approve(
          CROSS_MARGIN_HANDLER_ADDRESS, amount_wei).transact({"from": self.eth_signer.address})

    return self.cross_margin_handler_instance.functions.depositCollateral(
      sub_account_id,
      token_address,
      amount_wei,
      False
    ).transact({"from": self.eth_signer.address})

  def withdraw_collateral(self, sub_account_id: int, token_address: str, amount: float, wrap: bool = False):
    '''
    Withdraw ERC20 token as collateral.

    :param sub_account_id: required
    :type sub_account_id: int between 0 and 255

    :param token_address: required
    :type token_address: str in list COLLATERALS

    :param amount: required
    :type amount: float
    '''
    if token_address not in self.collateral_address_list:
      raise Exception("Invalid collateral address")
    self.__check_sub_account_id_param(sub_account_id)
    wrap = wrap if self.token_profile[token_address]['symbol'] == "WETH" else False

    amount_wei = int(
      amount * 10 ** self.token_profile[token_address]["decimals"])

    transact_param = {"value": EXECUTION_FEE, "from": self.eth_signer.address,
                      "gas": 10000000} if self.chain_id == 421614 else {"value": EXECUTION_FEE, "from": self.eth_signer.address}

    return self.cross_margin_handler_instance.functions.createWithdrawCollateralOrder(
      sub_account_id,
      token_address,
      amount_wei,
      EXECUTION_FEE,
      wrap
    ).transact(transact_param)

  def deposit_eth_collateral(self, sub_account_id: int, amount: float):
    '''
    Deposit ETH as collateral.

    :param sub_account_id: required
    :type sub_account_id: int between 0 and 255

    :param amount: required
    :type amount: float
    '''
    self.__check_sub_account_id_param(sub_account_id)

    amount_wei = int(amount * 10 ** 18)

    return self.cross_margin_handler_instance.functions.depositCollateral(
      sub_account_id,
      self.token_profile['WETH']['address'],
      amount_wei,
      True
    ).transact({"from": self.eth_signer.address, "value": amount_wei})

  def create_market_order(self, sub_account_id: int, market_index: int, buy: bool, size: float, reduce_only: bool, tp_token: str = ADDRESS_ZERO):
    '''
    Post a market order

    :param sub_account_id: required
    :type sub_account_id: int between 0 and 255

    :param market_index: required
    :type market_index: int in list MARKET

    :param buy: required
    :type buy: bool

    :param size: required
    :type size: float

    :param reduce_only: required
    :type reduce_only: bool

    :param tp_token
    :type tp_token: str in list COLLATERALS address
    '''
    self.__check_sub_account_id_param(sub_account_id)

    order = {
      "cmd": Cmd.CREATE,
      "market_index": market_index,
      "size_delta": Web3.to_wei(size, "tether") if buy else -Web3.to_wei(size, "tether"),
      "trigger_price": 0,
      "acceptable_price": MAX_UINT if buy else 0,
      "trigger_above_threshold": True,
      "execution_fee": EXECUTION_FEE,
      "reduce_only": reduce_only,
      "tp_token": tp_token
    }

    tx = self.__create_order_batch(
      self.eth_signer.address, sub_account_id, [order]
    )

    # wait for transaction to be complete
    self.eth_provider.eth.wait_for_transaction_receipt(tx)

    events = self.__parse_log(tx, "LogCreateLimitOrder")
    args = {}
    args["tx"] = events[0]["transactionHash"]
    args["order"] = events[0]["args"]
    return args

  def create_trigger_order(self, sub_account_id: int, market_index: int, buy: bool, size: float, trigger_price: float, trigger_above_threshold: bool, reduce_only: bool, tp_token: str = ADDRESS_ZERO):
    '''
    Post a trigger order

    :param sub_account_id: required
    :type sub_account_id: int between 0 and 255

    :param market_index: required
    :type market_index: int in list MARKET

    :param buy: required
    :type buy: bool

    :param size: required
    :type size: float

    :param trigger_price: required
    :type trigger_price: float

    :param trigger_above_threshold: required
    :type trigger_above_threshold: bool

    :param reduce_only: required
    :type reduce_only: bool

    :param tp_token
    :type tp_token: str in list COLLATERALS address
    '''
    order = {
      "cmd": Cmd.CREATE,
      "market_index": market_index,
      "size_delta": Web3.to_wei(size, "tether") if buy else -Web3.to_wei(size, "tether"),
      "trigger_price": Web3.to_wei(trigger_price, "tether"),
      "acceptable_price": Web3.to_wei(
        self.__add_slippage(
          trigger_price) if size > 0 else self.__sub_slippage(trigger_price),
        "tether"
      ),
      "trigger_above_threshold": trigger_above_threshold,
      "execution_fee": EXECUTION_FEE,
      "reduce_only": reduce_only,
      "tp_token": tp_token
    }

    tx = self.__create_order_batch(
      self.eth_signer.address, sub_account_id, [order]
    )

    self.eth_provider.eth.wait_for_transaction_receipt(tx)

    events = self.__parse_log(tx, "LogCreateLimitOrder")
    args = {}
    args["tx"] = events[0]["transactionHash"]
    args["order"] = events[0]["args"]
    return args

  def update_trigger_order(self, sub_account_id: int, order_index: int, buy: bool, size: float, trigger_price: float, trigger_above_threshold: bool, reduce_only: bool, tp_token: str = ADDRESS_ZERO):
    '''
    Update a trigger order

    :param sub_account_id: required
    :type sub_account_id: int between 0 and 255

    :param order_index: required
    :type order_index: int

    :param buy: required
    :type buy: bool

    :param size: required
    :type size: float

    :param trigger_price: required
    :type trigger_price: float

    :param trigger_above_threshold: required
    :type trigger_above_threshold: bool

    :param reduce_only: required
    :type reduce_only: bool

    :param tp_token: required
    :type tp_token: str in list COLLATERALS address
    '''
    size_delta = Web3.to_wei(size, "tether")
    acceptable_price = self.__add_slippage(
      trigger_price) if size > 0 else self.__sub_slippage(trigger_price)
    order = {
      "cmd": Cmd.UPDATE,
      "order_index": order_index,
      "size_delta": size_delta if buy else -size_delta,
      "trigger_price": Web3.to_wei(trigger_price, "tether"),
      "acceptable_price": Web3.to_wei(acceptable_price, "tether"),
      "trigger_above_threshold": trigger_above_threshold,
      "reduce_only": reduce_only,
      "tp_token": tp_token
    }

    tx = self.__create_order_batch(
      self.eth_signer.address, sub_account_id, [order]
    )

    self.eth_provider.eth.wait_for_transaction_receipt(tx)

    events = self.__parse_log(tx, "LogUpdateLimitOrder")
    args = {}
    args["tx"] = events[0]["transactionHash"]
    args["order"] = events[0]["args"]
    return args

  def cancel_trigger_order(self, sub_account_id: int, order_index: int):
    '''
    Cancel a trigger order

    :param sub_account_id: required
    :type sub_account_id: int between 0 and 255

    :param order_index: required
    :type order_index: int
    '''
    order = {
      "cmd": Cmd.CANCEL,
      "order_index": order_index,
    }

    tx = self.__create_order_batch(
      self.eth_signer.address, sub_account_id, [order]
    )

    self.eth_provider.eth.wait_for_transaction_receipt(tx)

    events = self.__parse_log(tx, "LogCancelLimitOrder")
    args = {}
    args["tx"] = events[0]["transactionHash"]
    args["order"] = events[0]["args"]
    return args

  def __add_slippage(self, value: float):
    return decimal.Decimal(value) * (BPS + 25) / BPS

  def __sub_slippage(self, value: float):
    return decimal.Decimal(value) * (BPS - 25) / BPS

  def __create_order_batch(self, account: str, sub_account_id: int, orders):
    (cmds, datas) = self.__prepare_batch_input(orders)
    return self.limit_trade_handler_instance.functions.batch(
      account,
      sub_account_id,
      cmds,
      datas
    ).transact({"from": self.eth_signer.address, "value": EXECUTION_FEE * cmds.count(Cmd.CREATE)})

  def __prepare_batch_input(self, orders):
    return ([order["cmd"] for order in orders], [self.__prepare_order_call_data(order) for order in orders])

  def __prepare_order_call_data(self, order):
    if order["cmd"] == Cmd.CREATE:
      return self.__prepare_create_order_call_data(
        order["market_index"],
        order["size_delta"],
        order["trigger_price"],
        order["acceptable_price"],
        order["trigger_above_threshold"],
        order["execution_fee"],
        order["reduce_only"],
        order["tp_token"]
      )
    if order["cmd"] == Cmd.UPDATE:
      return self.__prepare_update_order_call_data(
        order["order_index"],
        order["size_delta"],
        order["trigger_price"],
        order["acceptable_price"],
        order["trigger_above_threshold"],
        order["reduce_only"],
        order["tp_token"]
      )
    if order["cmd"] == Cmd.CANCEL:
      return self.__prepare_cancel_order_call_data(order["order_index"])

  def __prepare_create_order_call_data(self, market_index: int, size_delta: float, trigger_price: float, acceptable_price: float, trigger_above_threshold: bool, execution_fee: float, reduce_only: bool, tp_token: str):
    return encode(
      ["uint256", "int256", "uint256", "uint256",
       "bool", "uint256", "bool", "address"],
      [market_index, size_delta, trigger_price, acceptable_price,
       trigger_above_threshold, execution_fee, reduce_only, tp_token]
    )

  def __prepare_update_order_call_data(self, order_index: int, size_delta: float, trigger_price: float, acceptable_price: float, trigger_above_threshold: bool, reduce_only: bool, tp_token: str):
    return encode(
      ["uint256", "int256", "uint256", "uint256",
       "bool", "bool", "address"],
      [order_index, size_delta, trigger_price, acceptable_price,
       trigger_above_threshold, reduce_only, tp_token]
    )

  def __prepare_cancel_order_call_data(self, order_index: int):
    return encode(
      ["uint256"],
      [order_index]
    )

  def __check_sub_account_id_param(self, sub_account_id):
    if sub_account_id not in range(0, 256):
      raise Exception("Invalid sub account id")

  def __parse_log(self, tx, topic):
    receipt = self.eth_provider.eth.get_transaction_receipt(tx)
    return self.limit_trade_handler_instance.events[topic](
      ).process_receipt(receipt, DISCARD)
