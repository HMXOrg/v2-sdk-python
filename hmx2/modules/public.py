class Public(object):
  def __init__(self, eth_provider):
    self.eth_provider = eth_provider

  def get_market(self, market_index: int):
    (
      long_position_size,
      long_accum_se,
      long_accum_s2e,
      short_position_size,
      short_accum_se,
      short_accum_s2e,
      current_funding_rate,
      last_funding_time,
      accum_funding_long,
      accum_funding_short,
      funding_accrued
    ) = self.perp_storage_instance.functions.markets(market_index).call()
    return {
      "long_position_size": long_position_size / 1e30,
      "long_accum_se": long_accum_se,
      "long_accum_s2e": long_accum_s2e,
      "short_position_size": short_position_size,
      "short_accum_se": short_accum_se,
      "short_accum_s2e": short_accum_s2e,
      "current_funding_rate": current_funding_rate,
      "last_funding_time": last_funding_time,
      "accum_funding_long": accum_funding_long,
      "accum_funding_short": accum_funding_short,
      "funding_accrued": funding_accrued,
    }
