import math
from web3 import Web3
from hmx2.constants.common import BIE18, BIE8
from hmx2.helpers.contract_loader import load_contract
from hmx2.helpers.util import convert_asset_to_byte32
from hmx2.modules.oracle.pyth_oracle import PythOracle
from hmx2.constants.contracts import CALC_PRICELENS_ABI_PATH
from hmx2.constants.tokens import (
  ASSET_ybETH,
  ASSET_ETH,
  ASSET_ybUSDB,
  ASSET_DAI
)


BLAST_PRICESOURCE_OPTION = {
  ASSET_ybETH: [ASSET_ETH],
  ASSET_ybUSDB: [ASSET_DAI],
}


class CalcPricelensOracle(object):
  def __init__(self, calc_pricelens_address: str, pyth_oracle: PythOracle, eth_provider: Web3) -> None:
    self.pyth_oracle = pyth_oracle
    self.eth_provider = eth_provider
    self.calc_pricelen_instance = load_contract(
      self.eth_provider, calc_pricelens_address, CALC_PRICELENS_ABI_PATH)

  def get_price(self, asset_id: str) -> float | None:
    pricesource_options_e8 = [math.floor(self.pyth_oracle.get_price(
      pricesource_asset) * BIE8)
        for pricesource_asset in BLAST_PRICESOURCE_OPTION[asset_id]]

    price = self.calc_pricelen_instance.functions.getPrice(
      convert_asset_to_byte32(asset_id), pricesource_options_e8).call()
    return price / BIE18
