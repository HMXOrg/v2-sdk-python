from web3 import Web3, Account
from hmx2.constants import DEFAULT_PYTH_PRICE_SERVICE_URL
from hmx2.modules.private import Private
from hmx2.modules.public import Public
from hmx2.modules.oracle.pyth_oracle import PythOracle
from hmx2.modules.oracle.glp_oracle import GlpOracle
from hmx2.modules.oracle.oracle_middleware import OracleMiddleware


class Client(object):
  def __init__(self, rpc_url, eth_private_key=None, pyth_price_service_url=DEFAULT_PYTH_PRICE_SERVICE_URL):
    self.__eth_provider = Web3(Web3.HTTPProvider(
      rpc_url, request_kwargs={'timeout': 60}))
    self.__chain_id = self.__eth_provider.eth.chain_id
    if eth_private_key is not None:
      self.__eth_signer = Account.from_key(eth_private_key)

    pyth_oracle = PythOracle(self.__chain_id, pyth_price_service_url)
    glp_oracle = GlpOracle(self.__eth_provider)
    self.__oracle_middleware = OracleMiddleware(pyth_oracle, glp_oracle)

    self.__private = None
    self.__public = Public(self.__eth_provider, self.__oracle_middleware)

  @property
  def public(self):
    '''
    Get the public module, used for permissionless actions.
    Such as, get price, get funding rate, and etc.
    '''
    return self.__public

  @property
  def private(self):
    '''
    Get the private module, used for permissioned actions.
    Such as, deposit collateral, withdraw collateral, trade, etc.
    '''
    if not self.__private:
      if self.__eth_signer:
        self.__private = Private(
          self.__chain_id, self.__eth_provider, self.__eth_signer, self.__oracle_middleware)
      else:
        raise Exception("Private module requires eth_private_key")
    return self.__private
