from web3 import Web3
from hmx2.helpers.contract_loader import load_contract
from hmx2.constants.contracts import GLP_MANAGER_ABI_PATH
from hmx2.constants.assets import ASSET_GLP
from hmx2.helpers.mapper import get_contract_address
from simple_multicall_v6 import Multicall
from eth_abi.abi import decode


class GlpOracle(object):
  def __init__(self, eth_provider: Web3) -> None:
    self.eth_provider = eth_provider
    self.contract_address = get_contract_address(self.eth_provider.eth.chain_id)
    self.glp_manager_instance = load_contract(
      self.eth_provider, self.contract_address["GLP_MANAGER_ADDRESS"], GLP_MANAGER_ABI_PATH)
    self.multicall_instance = Multicall(w3=self.eth_provider,
                                        custom_address=self.contract_address["MULTICALL_ADDRESS"])

  def get_price(self, asset_id: str) -> float:
    '''
    Get the latest price of the asset.

    :param asset_id: required
    :type asset_id: str only GLP
    '''
    if asset_id != ASSET_GLP:
      raise Exception('Only GLP is supported')

    calls = [self.multicall_instance.create_call(
      self.glp_manager_instance,
      "getPrice",
      [is_true]
    ) for is_true in [False, True]]

    contract_data_raw = self.multicall_instance.call(calls)[1]

    mid_price = (decode(['uint256'], contract_data_raw[0])[0] +
                 decode(['uint256'], contract_data_raw[1])[0]) / 2

    return mid_price / 10 ** 30
