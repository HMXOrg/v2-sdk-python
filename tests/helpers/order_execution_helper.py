from web3 import Web3
from hmx2.constants import LIMIT_TRADE_HANDLER_ADDRESS
from hmx2.constants import LIMIT_TRADE_HANDLER_ABI_PATH
from hmx2.helpers.contract_loader import load_contract
from tests.constants import MARKET_ORDER_EXECUTIONER_ADDRESS
from tests.constants import ECOPYTH_CALLDATA_BUILDER_ADDRESS
from tests.constants import get_default_price_data
import time


class OrderExecutionHelper(object):
  def __init__(self, rpc_url):
    self.__w3 = Web3(Web3.HTTPProvider(rpc_url))

  def execute_orders(
    self,
    accounts: list[str],
    sub_account_ids: list[int],
    order_indexes: list[int],
    is_revert: bool,
    override_price_data=None
  ):
    limit_trade_handler_instance = load_contract(
      self.__w3, LIMIT_TRADE_HANDLER_ADDRESS, LIMIT_TRADE_HANDLER_ABI_PATH
    )
    eco_pyth_calldata_builder_instance = load_contract(
      self.__w3, ECOPYTH_CALLDATA_BUILDER_ADDRESS, "../tests/abis/EcoPythCalldataBuilder.json")
    price_data = get_default_price_data(int(time.time()), override_price_data)
    [min_published_time, price_update_data,
     publish_time_update_data] = eco_pyth_calldata_builder_instance.functions.build(price_data).call()
    return limit_trade_handler_instance.functions.executeOrders(
      accounts,
      sub_account_ids,
      order_indexes,
      MARKET_ORDER_EXECUTIONER_ADDRESS,
      price_update_data,
      publish_time_update_data,
      min_published_time, b'',
      is_revert
    ).transact({'from': MARKET_ORDER_EXECUTIONER_ADDRESS, 'gas': 8_000_000})
