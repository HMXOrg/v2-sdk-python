from hmx2.modules.oracle.pyth_oracle import PythOracle
from hmx2.modules.oracle.glp_oracle import GlpOracle
from hmx2.modules.oracle.cix_oracle import CixOracle
from hmx2.modules.oracle.gm_oracle import GmOracle
from hmx2.constants import ASSETS, ASSET_gmBTC, ASSET_gmETH, ASSET_DIX, ASSET_GLP


class OracleMiddleware(object):
  def __init__(self, pyth_oracle: PythOracle, glp_oracle: GlpOracle, dix_oracle: CixOracle,
               gm_btc_oracle: GmOracle, gm_eth_oracle: GmOracle):
    self.glp_oracle = glp_oracle
    self.pyth_oracle = pyth_oracle
    self.dix_oracle = dix_oracle
    self.gm_btc_oracle = gm_btc_oracle
    self.gm_eth_oracle = gm_eth_oracle

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

    return self.pyth_oracle.get_price(asset_id)
