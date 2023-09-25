from hmx2.constants import DAYS


class FeeCalculator:
  @staticmethod
  def get_funding_rate(trading_config, market_config, market, block_timestamp: int):
    next_funding_rate = FeeCalculator.get_funding_rate_velocity(
      market_config["max_funding_rate"],
      market_config["max_skew_scale_usd"],
      market["long_position_size"],
      market["short_position_size"],
      block_timestamp,
      trading_config["funding_interval"],
      market["last_funding_time"]
    )
    return (market["current_funding_rate"] + next_funding_rate)

  @staticmethod
  def get_funding_rate_velocity(max_funding_rate: int, max_skew_scale_usd: int, long_position_size: int, short_position_size: int, block_timestamp: int, funding_interval: int, last_funding_time: int) -> int:
    funding_rate = FeeCalculator.get_funding_rate_velocity_with_out_interval(
      max_funding_rate, max_skew_scale_usd, long_position_size, short_position_size)
    interval = FeeCalculator.proportional_elapsed_in_day(
      block_timestamp, funding_interval, last_funding_time)
    return funding_rate * interval // 10**18

  @staticmethod
  def get_funding_rate_velocity_with_out_interval(max_funding_rate: int, max_skew_scale_usd: int, long_position_size: int, short_position_size: int) -> int:
    if max_funding_rate == 0 or max_skew_scale_usd == 0:
      return 0
    market_skew_usd_e30 = long_position_size - short_position_size
    ratio = market_skew_usd_e30 * max_funding_rate // max_skew_scale_usd
    return min(max_funding_rate, ratio) if (ratio > 0) else max(max_funding_rate * -1, ratio)

  @staticmethod
  def proportional_elapsed_in_day(block_timestamp: int, funding_interval: int, last_funding_time: int) -> int:
    elapsed_intervals = (
      block_timestamp - last_funding_time) // funding_interval
    intervals_in_one_day = DAYS // funding_interval
    return elapsed_intervals * 10**18 // intervals_in_one_day

  @staticmethod
  def get_borrowing_rate(asset_class_config, asset_class, hlp_tvl):
    return FeeCalculator.get_next_borrowing_rate_without_interval(
      asset_class_config["base_borrowing_rate"], asset_class["reserve_value_e30"], hlp_tvl) // 10**18

  @staticmethod
  def get_next_borrowing_rate(base_borrowing_rate: int, reserve_value_e30: int, hlp_tvl: int, block_timestamp: int, last_borrowing_time: int, funding_interval: int):
    if last_borrowing_time + funding_interval > block_timestamp:
      return 0
    borrowing_rate = FeeCalculator.get_next_borrowing_rate_without_interval(
      base_borrowing_rate, reserve_value_e30, hlp_tvl)
    intervals = (block_timestamp - last_borrowing_time) // funding_interval

    return borrowing_rate * intervals

  @staticmethod
  def get_next_borrowing_rate_without_interval(base_borrowing_rate: int, reserve_value_e30: int, hlp_tvl: int):
    if hlp_tvl == 0:
      return 0
    return base_borrowing_rate * reserve_value_e30 // hlp_tvl
