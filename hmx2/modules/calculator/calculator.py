from hmx2.constants import DAYS


class Calculator:
  @staticmethod
  def get_funding_rate(trading_config, market_config, market, block_timestamp: int):
    next_funding_rate = Calculator.get_funding_rate_velocity(
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
    funding_rate = Calculator.get_funding_rate_velocity_with_out_interval(
      max_funding_rate, max_skew_scale_usd, long_position_size, short_position_size)
    interval = Calculator.proportional_elapsed_in_day(
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
    return Calculator.get_next_borrowing_rate_without_interval(
      asset_class_config["base_borrowing_rate"], asset_class["reserve_value_e30"], hlp_tvl) // 10**18

  @staticmethod
  def get_next_borrowing_rate(base_borrowing_rate: int, reserve_value_e30: int, hlp_tvl: int, block_timestamp: int, last_borrowing_time: int, funding_interval: int):
    if last_borrowing_time + funding_interval > block_timestamp:
      return 0
    borrowing_rate = Calculator.get_next_borrowing_rate_without_interval(
      base_borrowing_rate, reserve_value_e30, hlp_tvl)
    intervals = (block_timestamp - last_borrowing_time) // funding_interval

    return borrowing_rate * intervals

  @staticmethod
  def get_next_borrowing_rate_without_interval(base_borrowing_rate: int, reserve_value_e30: int, hlp_tvl: int):
    if hlp_tvl == 0:
      return 0
    return base_borrowing_rate * reserve_value_e30 // hlp_tvl

  @staticmethod
  def get_pnl(position, market, market_config, trading_config, market_price: int, block_timestamp: int):
    adaptive_price = Calculator.get_adaptive_price(
      market_price,
      market["long_position_size"],
      market["short_position_size"],
      market_config["max_skew_scale_usd"],
      position["position_size_e30"] * -1
    )
    (is_profit, delta) = Calculator.get_delta(
      position["avg_entry_price_e30"],
      adaptive_price,
      position["position_size_e30"] > 0,
      abs(position["position_size_e30"]),
      position["reserve_value_e30"],
      position["last_increase_timestamp"],
      trading_config["min_profit_duration"],
      block_timestamp,
    )
    return delta if is_profit else delta * -1

  @staticmethod
  def get_delta(avg_entry_price_e30: int, market_price: int, is_long: int, size: int, reserve_value_e30: int, last_increase_timestamp: int, min_profit_duration: int, block_timestamp: int):
    if avg_entry_price_e30 == 0:
      return (False, 0)

    price_delta = avg_entry_price_e30 - \
        market_price if avg_entry_price_e30 > market_price else market_price - avg_entry_price_e30
    delta = size * price_delta // avg_entry_price_e30
    is_profit = market_price > avg_entry_price_e30 if is_long else market_price < avg_entry_price_e30

    if is_profit:
      delta = min(delta, reserve_value_e30)

      if block_timestamp < (last_increase_timestamp + min_profit_duration):
        return (is_profit, 0)

    return (is_profit, delta)

  @staticmethod
  def get_adaptive_price(oracle_price: int, long_position_size: int, short_position_size: int, max_skew: int, size_delta: int):
    skew = long_position_size - short_position_size
    premium = skew * 10**30 // max_skew
    premium_after = (skew + size_delta) * 10**30 // max_skew
    premium_median = (premium + premium_after) // 2
    return oracle_price * (10**30 + premium_median) // 10**30

  @staticmethod
  def get_next_funding_accrued(trading_config, market_config, market, block_timestamp):
    proportionnal_elapsed_in_day = Calculator.proportional_elapsed_in_day(
      block_timestamp, trading_config["funding_interval"], market["last_funding_time"])

    funding_rate = Calculator.get_funding_rate_velocity_with_out_interval(
      market_config["max_funding_rate"], market_config["max_skew_scale_usd"], market["long_position_size"], market["short_position_size"])

    next_funding_rate = market["current_funding_rate"] + funding_rate

    return (market["funding_accrued"] + market["current_funding_rate"] +
            next_funding_rate) * proportionnal_elapsed_in_day // 2 // 1e18

  @staticmethod
  def get_fuding_fee(size: int, current_funding_accrued: int, last_funding_accrued: int):
    funding_rate = current_funding_accrued - last_funding_accrued
    return size * funding_rate // 10**18
