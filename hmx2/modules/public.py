from web3 import Web3
from hmx2.constants import (
  MULTICALL_ADDRESS,
  VAULT_STORAGE_ADDRESS,
  PERP_STORAGE_ADDRESS,
  CONFIG_STORAGE_ADDRESS,
  TRADE_HELPER_ADDRESS,
  CALCULATOR_ADDRESS,
  VAULT_STORAGE_ABI_PATH,
  PERP_STORAGE_ABI_PATH,
  CONFIG_STORAGE_ABI_PATH,
  TRADE_HELPER_ABI_PATH,
  CALCULATOR_ABI_PATH,
  HOURS,
  DAYS,
  YEARS,
  MARKET_PROFILE,
  DELISTED_MARKET
)
from hmx2.helpers.contract_loader import load_contract
from hmx2.modules.oracle.oracle_middleware import OracleMiddleware
from hmx2.modules.calculator.calculator import Calculator
from simple_multicall import Multicall
from eth_abi.abi import decode


class Public(object):
  def __init__(self, eth_provider: Web3, oracle_middleware: OracleMiddleware):
    self.eth_provider = eth_provider
    self.oracle_middleware = oracle_middleware
    self.perp_storage_instance = load_contract(
      self.eth_provider, PERP_STORAGE_ADDRESS, PERP_STORAGE_ABI_PATH)
    self.config_storage_instance = load_contract(
      self.eth_provider, CONFIG_STORAGE_ADDRESS, CONFIG_STORAGE_ABI_PATH)
    self.vault_storage_instance = load_contract(
      self.eth_provider, VAULT_STORAGE_ADDRESS, VAULT_STORAGE_ABI_PATH)
    self.trade_helper_instance = load_contract(
      self.eth_provider, TRADE_HELPER_ADDRESS, TRADE_HELPER_ABI_PATH
    )
    self.calculator_instance = load_contract(
      self.eth_provider, CALCULATOR_ADDRESS, CALCULATOR_ABI_PATH
    )
    self.multicall_instance = Multicall(w3=self.eth_provider,
                                        chain='arbitrum', custom_address=MULTICALL_ADDRESS)

  def __get_position(self, account: str, sub_account_id: int, market_index: int):
    position_id = self.get_position_id(account, sub_account_id, market_index)
    (
      primary_account,
      market_index,
      avg_entry_price_e30,
      entry_borrowing_rate,
      reserve_value_e30,
      last_increase_timestamp,
      position_size_e30,
      realized_pnl,
      last_funding_accrued,
      sub_account_id
    ) = self.perp_storage_instance.functions.positions(position_id).call()

    return {
      "primary_account": primary_account,
        "market_index": market_index,
        "avg_entry_price_e30": avg_entry_price_e30,
        "entry_borrowing_rate": entry_borrowing_rate,
        "reserve_value_e30": reserve_value_e30,
        "last_increase_timestamp": last_increase_timestamp,
        "position_size_e30": position_size_e30,
        "realized_pnl": realized_pnl,
        "last_funding_accrued": last_funding_accrued,
        "sub_account_id": sub_account_id,
    }
  
  def __multicall_all_market_data(self):
    ACTIVE_MARKET = [x for x in MARKET_PROFILE.keys() if x not in DELISTED_MARKET]
    market_config_calls = list(map(lambda market_index: self.multicall_instance.create_call(
        self.config_storage_instance, "marketConfigs", [market_index]
      ), ACTIVE_MARKET))
    
    market_config_results = self.multicall_instance.call(market_config_calls)
    data = market_config_results[1]

    market_config_data = {}

    for market_index in ACTIVE_MARKET:
      (
        asset_id,
        max_long_position_size,
        max_short_position_size,
        increase_position_fee_rate_bps,
        decrease_position_fee_rate_bps,
        initial_margin_fraction_bps,
        maintenance_margin_fraction_bps,
        max_profit_rate_bps,
        asset_class,
        allow_increase_position,
        active,
        max_skew_scale_usd,
        max_funding_rate,
      ) = decode(
          ['bytes32', 'uint256', 'uint256', 'uint32', 'uint32', 'uint32',
          'uint32', 'uint32', 'uint8', 'bool', 'bool', 'uint256', 'uint256'],
          data.pop(0)
        )
      
      market_config_data[market_index] = {
        "asset_id": asset_id.hex(),
        "max_long_position_size": max_long_position_size,
        "max_short_position_size": max_short_position_size,
        "increase_position_fee_rate_bps": increase_position_fee_rate_bps,
        "decrease_position_fee_rate_bps": decrease_position_fee_rate_bps,
        "initial_margin_fraction_bps": initial_margin_fraction_bps,
        "maintenance_margin_fraction_bps": maintenance_margin_fraction_bps,
        "max_profit_rate_bps": max_profit_rate_bps,
        "asset_class": asset_class,
        "allow_increase_position": allow_increase_position,
        "active": active,
        "max_skew_scale_usd": max_skew_scale_usd,
        "max_funding_rate": max_funding_rate
      }

    market_calls = list(map(lambda market_index: self.multicall_instance.create_call(
        self.perp_storage_instance, "markets", [market_index]
      ), ACTIVE_MARKET))
    
    market_results = self.multicall_instance.call(market_calls)
    data = market_results[1]
    
    market_data = {}
    for market_index in ACTIVE_MARKET:
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
      funding_accrued,
    ) = decode(
      ['uint256', 'uint256', 'uint256', 'uint256', 'uint256',
       'uint256', 'int256', 'uint256', 'int256', 'int256', 'int256'],
      data.pop(0)
    )
      market_data[market_index] = {
        "long_position_size": long_position_size,
        "long_accum_se": long_accum_se,
        "long_accum_s2e": long_accum_s2e,
        "short_position_size": short_position_size,
        "short_accum_se": short_accum_se,
        "short_accum_s2e": short_accum_s2e,
        "current_funding_rate": current_funding_rate,
        "last_funding_time": last_funding_time,
        "accum_funding_long": accum_funding_long,
        "accum_funding_short": accum_funding_short,
        "funding_accrued": funding_accrued
      }
    
    trade_config_result = self.config_storage_instance.functions.tradingConfig().call()
    
    (
      funding_interval,
      min_profit_duration,
      dev_fee_rate_bps,
      max_position
    ) = trade_config_result
    
    trade_config_data = {
        "funding_interval": funding_interval,
        "min_profit_duration": min_profit_duration,
        "dev_fee_rate_bps": dev_fee_rate_bps,
        "max_position": max_position
      }

    market_asset_class_map = {market_index: market_config_data[market_index]['asset_class'] for market_index in ACTIVE_MARKET}

    asset_class_list = list(set(market_asset_class_map.values()))

    asset_class_config_calls = list(map(lambda asset_class: self.multicall_instance.create_call(
        self.config_storage_instance, "assetClassConfigs", [asset_class]
      ), asset_class_list))
    
    asset_class_config_results = self.multicall_instance.call(asset_class_config_calls)
    data = asset_class_config_results[1]

    asset_class_config_data = {}

    for asset_class in asset_class_list:
      base_borrowing_rate = int(data.pop(0).hex(), 16)
      asset_class_config_data[asset_class] = {
        "base_borrowing_rate": base_borrowing_rate
      }

    asset_class_calls = list(map(lambda asset_class: self.multicall_instance.create_call(
        self.perp_storage_instance, "assetClasses", [asset_class]
      ), asset_class_list))
    
    asset_class_results = self.multicall_instance.call(asset_class_calls)
    data = asset_class_results[1]

    asset_class_data = {}

    for asset_class in asset_class_list:
      (
      reserve_value_e30,
      sum_borrowing_rate,
      last_borrowing_time,
      sum_borrowing_fee_e30,
      sum_settled_borrowing_fee_e30
    ) = decode(
      ['uint256', 'uint256', 'uint256', 'uint256', 'uint256'],
      data.pop(0)
    )
      asset_class_data[asset_class] = {
        "reserve_value_e30": reserve_value_e30,
        "sum_borrowing_rate": sum_borrowing_rate,
        "last_borrowing_time": last_borrowing_time,
        "sum_borrowing_fee_e30": sum_borrowing_fee_e30,
        "sum_settled_borrowing_fee_e30": sum_settled_borrowing_fee_e30
      }

    market_info_map = {}
    for market_index in ACTIVE_MARKET:
      market_info_map[market_index] = {
        "market_config": market_config_data[market_index],
        "market": market_data[market_index],
        "trading_config": trade_config_data,
        "asset_class_config": asset_class_config_data[market_asset_class_map[market_index]],
        "asset_class": asset_class_data[market_asset_class_map[market_index]]
      }

    return market_info_map

  def __multicall_market_data(self, market_index: int):
    calls = [
      self.multicall_instance.create_call(
        self.config_storage_instance, "marketConfigs", [market_index]
      ),
      self.multicall_instance.create_call(
        self.perp_storage_instance, "markets", [market_index]
      ),
      self.multicall_instance.create_call(
        self.config_storage_instance, "tradingConfig", []
      )
    ]

    results = self.multicall_instance.call(calls)
    data = results[1]
    (
      asset_id,
      max_long_position_size,
      max_short_position_size,
      increase_position_fee_rate_bps,
      decrease_position_fee_rate_bps,
      initial_margin_fraction_bps,
      maintenance_margin_fraction_bps,
      max_profit_rate_bps,
      asset_class,
      allow_increase_position,
      active,
      max_skew_scale_usd,
      max_funding_rate,
    ) = decode(
        ['bytes32', 'uint256', 'uint256', 'uint32', 'uint32', 'uint32',
         'uint32', 'uint32', 'uint8', 'bool', 'bool', 'uint256', 'uint256'],
        data.pop(0)
      )
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
      funding_accrued,
    ) = decode(
      ['uint256', 'uint256', 'uint256', 'uint256', 'uint256',
       'uint256', 'int256', 'uint256', 'int256', 'int256', 'int256'],
      data.pop(0)
    )
    (
      funding_interval,
      min_profit_duration,
      dev_fee_rate_bps,
      max_position
    ) = decode(
      ['uint256', 'uint256', 'uint32', 'uint8'],
      data.pop(0)
    )

    calls = [
      self.multicall_instance.create_call(
        self.config_storage_instance, "assetClassConfigs", [asset_class]
      ),
      self.multicall_instance.create_call(
        self.perp_storage_instance, "assetClasses", [asset_class]
      ),
    ]
    results = self.multicall_instance.call(calls)
    data = results[1]
    base_borrowing_rate = int(data.pop(0).hex(), 16)
    (
      reserve_value_e30,
      sum_borrowing_rate,
      last_borrowing_time,
      sum_borrowing_fee_e30,
      sum_settled_borrowing_fee_e30
    ) = decode(
      ['uint256', 'uint256', 'uint256', 'uint256', 'uint256'],
      data.pop(0)
    )

    return {
      "market_config": {
        "asset_id": asset_id.hex(),
        "max_long_position_size": max_long_position_size,
        "max_short_position_size": max_short_position_size,
        "increase_position_fee_rate_bps": increase_position_fee_rate_bps,
        "decrease_position_fee_rate_bps": decrease_position_fee_rate_bps,
        "initial_margin_fraction_bps": initial_margin_fraction_bps,
        "maintenance_margin_fraction_bps": maintenance_margin_fraction_bps,
        "max_profit_rate_bps": max_profit_rate_bps,
        "asset_class": asset_class,
        "allow_increase_position": allow_increase_position,
        "active": active,
        "max_skew_scale_usd": max_skew_scale_usd,
        "max_funding_rate": max_funding_rate
      },
      "market": {
        "long_position_size": long_position_size,
        "long_accum_se": long_accum_se,
        "long_accum_s2e": long_accum_s2e,
        "short_position_size": short_position_size,
        "short_accum_se": short_accum_se,
        "short_accum_s2e": short_accum_s2e,
        "current_funding_rate": current_funding_rate,
        "last_funding_time": last_funding_time,
        "accum_funding_long": accum_funding_long,
        "accum_funding_short": accum_funding_short,
        "funding_accrued": funding_accrued
      },
      "trading_config": {
        "funding_interval": funding_interval,
        "min_profit_duration": min_profit_duration,
        "dev_fee_rate_bps": dev_fee_rate_bps,
        "max_position": max_position
      },
      "asset_class_config": {
        "base_borrowing_rate": base_borrowing_rate
      },
      "asset_class": {
        "reserve_value_e30": reserve_value_e30,
        "sum_borrowing_rate": sum_borrowing_rate,
        "last_borrowing_time": last_borrowing_time,
        "sum_borrowing_fee_e30": sum_borrowing_fee_e30,
        "sum_settled_borrowing_fee_e30": sum_settled_borrowing_fee_e30
      }
    }

  def __get_block(self):
    return self.eth_provider.eth.get_block("latest")

  def __get_hlp_tvl(self, is_max_price: bool = True):
    return self.calculator_instance.functions.getHLPValueE30(is_max_price).call()

  def get_price(self, market_index: int, buy: bool = None, size: float = None):
    '''Get price from a market (adaptive price if input 'buy' and 'size')

      Args:
        market_index: market index
        buy: true for buy, false for sell
        size: size of position

      Returns:
        price object
    '''

    if buy is None and size is None:
      price = self.oracle_middleware.get_price(MARKET_PROFILE[market_index]["asset"])
      print(MARKET_PROFILE[market_index]["name"])
      print("price", price)
      print('-----------------------------------------------------------------------------------------------')
      asset_decimal = MARKET_PROFILE[market_index]["display_decimal"]
      return {
        "market": MARKET_PROFILE[market_index]["name"],
        "price": round(price, asset_decimal),
        "adaptive_price": None,
        "price_impact": None,
      }
  
    data = self.__multicall_market_data(market_index)
    oracle_price = self.oracle_middleware.get_price(
      MARKET_PROFILE[market_index]["asset"]) * 10**30
    adaptive_price = Calculator.get_adaptive_price(
      oracle_price,
      data["market"]["long_position_size"],
      data["market"]["short_position_size"],
      data["market_config"]["max_skew_scale_usd"],
      Web3.to_wei(size, "tether") if buy else -Web3.to_wei(size, "tether")
    )
    price_impact = (adaptive_price * 10**30 // oracle_price) - 10**30

    return {
      "market": MARKET_PROFILE[market_index]["name"],
      "price": round(oracle_price, asset_decimal) / 10**30,
      "adaptive_price": round(adaptive_price, asset_decimal) / 10**30,
      "price_impact": price_impact * 100 / 10**30,
    }


  def get_market_info(self, market_index: int):
    '''Get a market info

      Args:
      market_index: market index

      Returns:
      market info object
    '''
    data = self.__multicall_market_data(market_index)
    block = self.__get_block()
    tvl = self.__get_hlp_tvl()

    price = self.get_price(market_index)["price"]

    funding_rate = Calculator.get_funding_rate(
      data["trading_config"],
      data["market_config"],
      data["market"],
      block["timestamp"],
    )

    borrowing_rate = Calculator.get_borrowing_rate(
      data["asset_class_config"], data["asset_class"], tvl)

    return {
      "market": MARKET_PROFILE[market_index]["name"],
      "price": price,
      "long_size": data["market"]["long_position_size"] / 10**30,
      "short_size": data["market"]["short_position_size"] / 10**30,
      "funding_rate": {
        "1H": funding_rate * HOURS / DAYS * 100 / 10**18,
        "8H": funding_rate * 8 * HOURS / DAYS * 100 / 10**18,
        "24H": funding_rate * 100 / 10**18,
        "1Y": funding_rate * 365 * 100 / 10**18,
      },
      "borrowing_rate": {
        "1H": borrowing_rate * HOURS * 100 / 10**18,
        "8H": borrowing_rate * 8 * HOURS * 100 / 10**18,
        "24H": borrowing_rate * DAYS * 100 / 10**18,
        "1Y": borrowing_rate * YEARS * 100 / 10**18,
      }
    }

  def get_all_market_info(self):
    '''Get all market info

      Returns:
        market info dict with market_index as key
    '''
    tvl = self.__get_hlp_tvl()
    block = self.__get_block()

    market_info = {}
    raw_market_data = self.__multicall_all_market_data()


    for market_index in MARKET_PROFILE.keys():
      if market_index not in DELISTED_MARKET:
        current_raw_market_data = raw_market_data[market_index]
        price = self.get_price(market_index)["price"]
        funding_rate = Calculator.get_funding_rate(
          current_raw_market_data["trading_config"],
          current_raw_market_data["market_config"],
          current_raw_market_data["market"],
          block["timestamp"],
        )

        borrowing_rate = Calculator.get_borrowing_rate(
          current_raw_market_data["asset_class_config"], current_raw_market_data["asset_class"], tvl)
        
        
        market_info[market_index] = {
          "market": MARKET_PROFILE[market_index]["name"],
          "price": price,
          "long_size": current_raw_market_data["market"]["long_position_size"] / 10**30,
          "short_size": current_raw_market_data["market"]["short_position_size"] / 10**30,
          "funding_rate": {
            "1H": funding_rate * HOURS / DAYS * 100 / 10**18,
            "8H": funding_rate * 8 * HOURS / DAYS * 100 / 10**18,
            "24H": funding_rate * 100 / 10**18,
            "1Y": funding_rate * 365 * 100 / 10**18,
          },
          "borrowing_rate": {
            "1H": borrowing_rate * HOURS * 100 / 10**18,
            "8H": borrowing_rate * 8 * HOURS * 100 / 10**18,
            "24H": borrowing_rate * DAYS * 100 / 10**18,
            "1Y": borrowing_rate * YEARS * 100 / 10**18,
          }
        }
    return market_info

  def get_sub_account(self, account: str, sub_account_id: int):
    '''Get address of sub_account

      Args:
        account: account address
        sub_account_id: sub account number

      Returns:
        sub_account address
    '''
    return Web3.to_checksum_address(hex(int(account, 16) ^ sub_account_id))

  def get_position_id(self, account: str, sub_account_id: int, market_index: int):
    return Web3.solidity_keccak(
      ['address', 'uint256'],
      [self.get_sub_account(account, sub_account_id), market_index]
    )

  def get_position_info(self, account: str, sub_account_id: int, market_index: int):
    market_data = self.__multicall_market_data(market_index)
    tvl = self.__get_hlp_tvl()

    position = self.__get_position(account, sub_account_id, market_index)
    reserved_value = position['reserve_value_e30']
    sum_borrowing_rate = market_data['asset_class']['sum_borrowing_rate']
    entry_borrowing_rate = position['entry_borrowing_rate']
    block = self.__get_block()
    price = int(self.oracle_middleware.get_price(
        MARKET_PROFILE[market_index]["asset"]) * 10 ** 30)

    pnl = Calculator.get_pnl(
      position, market_data["market"], market_data["market_config"], market_data["trading_config"], price, block["timestamp"])

    current_funding_accrued = Calculator.get_next_funding_accrued(
      market_data["trading_config"], market_data["market_config"], market_data["market"], block["timestamp"])
    funding_fee = Calculator.get_funding_fee(
      position["position_size_e30"], current_funding_accrued, position["last_funding_accrued"])
    
    next_borrowing_rate = Calculator.get_next_borrowing_rate(
      market_data['asset_class_config']['base_borrowing_rate'],
      reserved_value,
      tvl, 
      block["timestamp"], 
      market_data["asset_class"]['last_borrowing_time'], 
      market_data["trading_config"]['funding_interval'])
    
    borrowing_fee = Calculator.get_borrowing_fee(reserved_value=reserved_value, sum_borrowing_rate=(sum_borrowing_rate + next_borrowing_rate), entry_borrowing_rate=entry_borrowing_rate)

    return {
      "primary_account": position["primary_account"],
      "sub_account_id": position["sub_account_id"],
      "market": MARKET_PROFILE[market_index]["name"],
      "position_size": position["position_size_e30"] / 10**30,
      "avg_entry_price": position["avg_entry_price_e30"] / 10**30,
      "pnl": pnl / 10**30,
      "funding_fee": funding_fee / 10**30,
      "borrowing_fee": borrowing_fee / 10**30,
    }
  
  def get_adaptive_fee(self, size_delta: int, market_index: int, is_increase: bool):
    base_fee_bps = 7
    raw_market_config = self.config_storage_instance.functions.getMarketConfigByIndex(market_index).call()
    (
      asset_id,
      max_long_position_size,
      max_short_position_size,
      increase_position_fee_rate_bps,
      decrease_position_fee_rate_bps,
      initial_margin_fraction_bps,
      maintenance_margin_fraction_bps,
      max_profit_rate_bps,
      asset_class,
      allow_increase_position,
      active,
      funding_rate
    ) = raw_market_config

    if is_increase:
      base_fee_bps = increase_position_fee_rate_bps
    else:
      base_fee_bps = decrease_position_fee_rate_bps

    raw_fee = self.trade_helper_instance.functions.getAdaptiveFeeBps(size_delta , market_index, base_fee_bps).call()
    fee = Web3.to_int(raw_fee)

    return fee
