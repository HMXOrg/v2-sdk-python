from web3 import Web3, Account
from web3.middleware import construct_sign_and_send_raw_middleware
from hmx2.constants import TOKEN_PROFILE
from hmx2.helpers.contract_loader import load_contract
from tests.constants import UNISWAP_SWAP_ROUTER_02_ADDRESS


class ActionHelper(object):
  def __init__(self, rpc_url, eth_private_key):
    self.__w3 = Web3(Web3.HTTPProvider(rpc_url))
    self.__eth_account = Account.from_key(eth_private_key)
    self.__w3.middleware_onion.add(
        construct_sign_and_send_raw_middleware(self.__eth_account)
    )

  def wrap_eth(self, amount):
    weth_instance = load_contract(
        self.__w3, TOKEN_PROFILE["WETH"]["address"], "../tests/abis/aeWETH.json"
    )
    return weth_instance.functions.deposit().transact(
        {"from": self.__eth_account.address,
         "value": Web3.to_wei(amount, "ether")}
    )

  def approve(self, token_address, spender_address, amount):
    token_instance = load_contract(
      self.__w3, token_address, "abis/ERC20.json")
    token_deciamls = token_instance.functions.decimals().call()
    return token_instance.functions.approve(spender_address, amount * 10 ** token_deciamls).transact(
        {"from": self.__eth_account.address}
    )

  def my_balance(self, token_address):
    token_instance = load_contract(
      self.__w3, token_address, "abis/ERC20.json")
    return token_instance.functions.balanceOf(self.__eth_account.address).call()

  def swapExactTokensForTokens(self, token_in, token_out, fee, amount_in):
    swap_router_instance = load_contract(
        self.__w3, UNISWAP_SWAP_ROUTER_02_ADDRESS, "../tests/abis/SwapRouter02.json"
    )
    token_in_instance = load_contract(
      self.__w3, token_in, "abis/ERC20.json"
    )
    decimals = token_in_instance.functions.decimals().call()
    amount_in_wei = amount_in * 10 ** decimals
    return swap_router_instance.functions.exactInputSingle(
        {
            "tokenIn": token_in,
            "tokenOut": token_out,
            "fee": fee,
            "recipient": self.__eth_account.address,
            "deadline": 4121449723,  # 77 years. Virtually impossible to reach.
            "amountIn": amount_in_wei,
            "amountOutMinimum": 0,
            "sqrtPriceLimitX96": 0
        }
    ).transact({"from": self.__eth_account.address})
