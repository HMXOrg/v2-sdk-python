from typing import List
from web3 import Web3
from hmx2.helpers.contract_loader import load_contract
from hmx2.modules.oracle.pyth_oracle import PythOracle
from hmx2.constants.contracts import GM_PRICE_ADAPTER_ABI_PATH
import math


class GmOracle(object):
  def __init__(self, gm_adapter_address: str, asset_ids: List, pyth_oracle: PythOracle, eth_provider: Web3):
    self.pyth_oracle = pyth_oracle
    self.eth_provider = eth_provider
    # asset_ids[0] = index token asset id
    # asset_ids[1] = long token asset id
    # asset_ids[2] = short token asset id
    self.asset_ids = asset_ids
    self.gm_adapter_instance = load_contract(
      self.eth_provider, gm_adapter_address, GM_PRICE_ADAPTER_ABI_PATH)

  def get_price(self, asset_id: str) -> float:
    prices = []
    prices.append(math.floor(
      self.pyth_oracle.get_price(self.asset_ids[0]) * 1e8))
    prices.append(math.floor(
      self.pyth_oracle.get_price(self.asset_ids[1]) * 1e8))
    prices.append(math.floor(
      self.pyth_oracle.get_price(self.asset_ids[2]) * 1e8))

    # Calculate the price
    price = self.gm_adapter_instance.functions.getPrice(prices).call()

    return price / 1e18
