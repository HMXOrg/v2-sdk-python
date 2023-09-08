from hmx2.modules.oracle.pyth_oracle import PythOracle
from hmx2.modules.oracle.glp_oracle import GlpOracle
from hmx2.constants import ASSETS


class OracleMiddleware(object):
  def __init__(self, pyth_oracle: PythOracle, glp_oracle: GlpOracle):
    self.glp_oracle = glp_oracle
    self.pyth_oracle = pyth_oracle

  def get_price(self, asset_id: str):
    '''
    Get the latest price of the asset.

    :param asset_id: required
    :type asset_id: str in list ASSET_IDS
    '''
    if asset_id not in ASSETS:
      raise Exception('Invalid asset_id')

    if asset_id == 'GLP':
      return self.glp_oracle.get_price(asset_id)

    return self.pyth_oracle.get_price(asset_id)
