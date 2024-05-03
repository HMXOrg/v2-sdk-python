from hmx2.modules.oracle.pyth_oracle import PythOracle
from hmx2.modules.oracle.glp_oracle import GlpOracle
from hmx2.modules.oracle.cix_oracle import CixOracle
from hmx2.modules.oracle.gm_oracle import GmOracle
from hmx2.modules.oracle.onchain_pricelens_oracle import OnchainPricelensOracle
from hmx2.modules.oracle.calc_pricelens_oracle import CalcPricelensOracle
from hmx2.constants.assets import (
  ASSETS,
  ASSET_USDCe,
  ASSET_gmBTC,
  ASSET_gmETH,
  ASSET_DIX,
  ASSET_GLP,
  ASSET_wstETH,
  ASSET_1000PEPE,
  ASSET_1000SHIB,
  ASSET_JPY,
  ASSET_ybETH,
  ASSET_ybUSDB,
)
from typing import List


class OracleMiddleware(object):
  def __init__(self, pyth_oracle: PythOracle, glp_oracle: GlpOracle, dix_oracle: CixOracle,
               gm_btc_oracle: GmOracle, gm_eth_oracle: GmOracle, onchain_pricelens_oracle: OnchainPricelensOracle,
               calc_pricelens_oracle: CalcPricelensOracle):
    self.glp_oracle = glp_oracle
    self.pyth_oracle = pyth_oracle
    self.dix_oracle = dix_oracle
    self.gm_btc_oracle = gm_btc_oracle
    self.gm_eth_oracle = gm_eth_oracle
    self.onchain_pricelens_oracle = onchain_pricelens_oracle
    self.calc_pricelens_oracle = calc_pricelens_oracle

  def get_price(self, asset_id: str):
    '''
    Get the latest price of the asset.

    :param asset_id: required
    :type asset_id: str in list ASSET_IDS
    '''
    if asset_id not in ASSETS:
      raise Exception('Invalid asset_id')

    if asset_id == ASSET_GLP:
      return self.glp_oracle.get_price(asset_id)

    if asset_id == ASSET_DIX:
      return self.dix_oracle.get_price(asset_id)

    if asset_id == ASSET_gmBTC:
      return self.gm_btc_oracle.get_price(asset_id)

    if asset_id == ASSET_gmETH:
      return self.gm_eth_oracle.get_price(asset_id)

    if asset_id == ASSET_wstETH:
      return self.onchain_pricelens_oracle.get_price(asset_id)

    if asset_id in [ASSET_1000PEPE, ASSET_1000SHIB]:
      return self.pyth_oracle.get_price(asset_id) * 1000

    if asset_id in [ASSET_JPY]:
      return 1 / self.pyth_oracle.get_price(asset_id)

    if asset_id in [ASSET_ybETH, ASSET_ybUSDB]:
      return self.calc_pricelens_oracle.get_price(asset_id)

    return self.pyth_oracle.get_price(asset_id)

  def get_multiple_price(self, asset_ids: List[str]):

    price_object = {}

    if set(asset_ids) - set(ASSETS):
      raise Exception('Invalid asset_ids')

    if ASSET_GLP in asset_ids:
      price_object[ASSET_GLP] = self.glp_oracle.get_price(ASSET_GLP)
      asset_ids.remove(ASSET_GLP)

    if ASSET_DIX in asset_ids:
      price_object[ASSET_DIX] = self.dix_oracle.get_price(ASSET_DIX)
      asset_ids.remove(ASSET_DIX)

    if ASSET_gmBTC in asset_ids:
      price_object[ASSET_gmBTC] = self.gm_btc_oracle.get_price(ASSET_gmBTC)
      asset_ids.remove(ASSET_gmBTC)

    if ASSET_gmETH in asset_ids:
      price_object[ASSET_gmETH] = self.gm_eth_oracle.get_price(ASSET_gmETH)
      asset_ids.remove(ASSET_gmETH)

    if ASSET_wstETH in asset_ids:
      price_object[ASSET_wstETH] = self.onchain_pricelens_oracle.get_price(
        ASSET_wstETH)
      asset_ids.remove(ASSET_wstETH)
    if ASSET_USDCe in asset_ids:
      price_object[ASSET_USDCe] = self.get_price("USDC")
      asset_ids.remove(ASSET_USDCe)

    if ASSET_ybETH in asset_ids:
      price_object[ASSET_ybETH] = self.calc_pricelens_oracle.get_price(
        ASSET_ybETH)
      asset_ids.remove(ASSET_ybETH)

    if ASSET_ybUSDB in asset_ids:
      price_object[ASSET_ybUSDB] = self.calc_pricelens_oracle.get_price(
        ASSET_ybUSDB)
      asset_ids.remove(ASSET_ybUSDB)

    raw_prices = self.pyth_oracle.get_multiple_price(asset_ids)

    for index, asset_id in enumerate(asset_ids):
      if asset_id in [ASSET_1000PEPE, ASSET_1000SHIB]:
        price_object[asset_id] = raw_prices[index] * 1000

      elif asset_id in [ASSET_JPY]:
        price_object[asset_id] = 1 / raw_prices[index]

      else:
        price_object[asset_id] = raw_prices[index]

    return price_object
