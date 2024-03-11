from web3 import Web3
from hmx2.helpers.contract_loader import load_contract
from hmx2.modules.oracle.pyth_oracle import PythOracle
from hmx2.constants.contracts import CIX_PRICE_ADAPTER_ABI_PATH


class CixOracle(object):
  def __init__(self, cix_adapter_address: str, pyth_oracle: PythOracle, eth_provider: Web3) -> None:
    self.pyth_oracle = pyth_oracle
    self.eth_provider = eth_provider
    self.cix_adapter_instance = load_contract(
      self.eth_provider, cix_adapter_address, CIX_PRICE_ADAPTER_ABI_PATH)

  def get_price(self, asset_id: str) -> float:
    cix_config = self.cix_adapter_instance.functions.getConfig().call()

    # Parse the config
    accum = cix_config[0] / 1e8
    cix_prices = []
    cix_asset_ids = []
    cix_weights = []
    cix_is_inverse = []
    for i in range(0, len(cix_config[1])):
      asset_id_str = cix_config[1][i].decode('utf-8').rstrip('\0')
      cix_asset_ids.append(asset_id_str)
      cix_prices.append(self.pyth_oracle.get_price(asset_id_str))
      cix_weights.append(cix_config[2][i] / 1e8)
      cix_is_inverse.append(cix_config[3][i])

    # Calculate the price
    for i in range(0, len(cix_asset_ids)):
      weight = cix_weights[i]
      if cix_is_inverse[i]:
        weight = -weight
      accum = accum * (pow(cix_prices[i], weight))

    return accum
