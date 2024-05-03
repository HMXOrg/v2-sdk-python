from web3 import Web3
from hmx2.constants.contracts import (
  ADAPTIVE_FEE_CALCULATOR_ABI,
  VAULT_STORAGE_ABI_PATH,
  PERP_STORAGE_ABI_PATH,
  CONFIG_STORAGE_ABI_PATH,
  TRADE_HELPER_ABI_PATH,
  CALCULATOR_ABI_PATH,
  ORDERBOOK_ORACLE_ABI
)
from hmx2.constants.intent import INTENT_TRADE_API
from hmx2.constants.markets import (
    DELISTED_MARKET
)
from hmx2.constants.common import (
  BPS,
  BYTE_ZERO,
  HOURS,
  DAYS,
  YEARS
)
from hmx2.enum import IntentOrderStatus
from hmx2.helpers.contract_loader import load_contract
from hmx2.helpers.mapper import (
  get_collateral_address_asset_map,
  get_collateral_address_list,
  get_contract_address,
  get_token_profile,
  get_market_profile,
)
from hmx2.helpers.util import get_sub_account, is_blast_chain
from hmx2.modules.oracle.oracle_middleware import OracleMiddleware
from hmx2.modules.calculator.calculator import Calculator
from simple_multicall_v6 import Multicall
from eth_abi.abi import decode
from typing import List
import requests as r


class Public(object):
  def __init__(self, chain_id: int, eth_provider: Web3, oracle_middleware: OracleMiddleware):
    self.chain_id = chain_id
    self.eth_provider = eth_provider
    self.oracle_middleware = oracle_middleware
    self.contract_address = get_contract_address(chain_id)
    self.perp_storage_instance = load_contract(
      self.eth_provider, self.contract_address["PERP_STORAGE_ADDRESS"], PERP_STORAGE_ABI_PATH)
    self.config_storage_instance = load_contract(
      self.eth_provider, self.contract_address["CONFIG_STORAGE_ADDRESS"], CONFIG_STORAGE_ABI_PATH)
    self.vault_storage_instance = load_contract(
      self.eth_provider, self.contract_address["VAULT_STORAGE_ADDRESS"], VAULT_STORAGE_ABI_PATH)
    self.trade_helper_instance = load_contract(
      self.eth_provider, self.contract_address["TRADE_HELPER_ADDRESS"], TRADE_HELPER_ABI_PATH
    )
    self.calculator_instance = load_contract(
      self.eth_provider, self.contract_address["CALCULATOR_ADDRESS"], CALCULATOR_ABI_PATH
    )
    self.orderbook_oracle_instance = load_contract(
      self.eth_provider, self.contract_address["ORDERBOOK_ORACLE_ADDRESS"], ORDERBOOK_ORACLE_ABI)
    self.adaptive_fee_calculator_instance = load_contract(
      self.eth_provider, self.contract_address["ADAPTIVE_FEE_CALCULATOR_ADDRESS"], ADAPTIVE_FEE_CALCULATOR_ABI)
    self.multicall_instance = Multicall(w3=self.eth_provider,
                                        custom_address=self.contract_address["MULTICALL_ADDRESS"])
    self.market_profile = get_market_profile(chain_id)

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

  def __get_all_position(self, account: str, sub_account_list: List[int]):

    if sub_account_list == []:
      sub_account_list = list(map(lambda sub_account_id: get_sub_account(
        account, sub_account_id), range(0, 256)))
    else:
      sub_account_list = list(map(lambda sub_account_id: get_sub_account(
       account, sub_account_id), sub_account_list))

    position_number_call = list(map(lambda sub_account_address: self.multicall_instance.create_call(
        self.perp_storage_instance, "getNumberOfSubAccountPosition", [
          sub_account_address]
      ), sub_account_list))

    position_number_result = self.multicall_instance.call(position_number_call)
    data = position_number_result[1]

    active_sub_account_number = []
    position_number = {}
    for sub_account_id, sub_account_address in enumerate(sub_account_list):
      sub_account_position_number = decode(['uint256'], data.pop(0))

      if sub_account_position_number[0] > 0:
        position_number[sub_account_address] = sub_account_position_number[0]
        active_sub_account_number.append(sub_account_id)
    sub_account_list = active_sub_account_number

    position_data = {}

    position_calls = list(map(lambda active_sub_account_address: self.multicall_instance.create_call(
        self.perp_storage_instance, "getPositionBySubAccount",
        [active_sub_account_address]
      ), list(position_number.keys())))

    position_result = self.multicall_instance.call(position_calls)
    data = position_result[1]

    position_data = {}

    for sub_account_id in sub_account_list:
      data_pop = data.pop(0)
      # backward compatibility on `getPositionBySubAccount`
      raw_sub_account_position = {}
      try:
        (
            raw_sub_account_position
          ) = decode(
              ['(address,uint256,uint256,uint256,uint256,uint256,int256,int256,int256,uint8)[]'],
              data_pop
          )
      except:
        (
            raw_sub_account_position
          ) = decode(
              ['(address,uint256,uint256,uint256,uint256,uint256,int256,int256,int256,uint8,uint256)[]'],
              data_pop
          )

      raw_sub_account_position = [
        x for y in raw_sub_account_position for x in y]

      sub_account_position = []
      for position in raw_sub_account_position:
        last_increase_size = None
        try:
          last_increase_size = position[10]
        except:
          pass
        _position = {
          "primary_account": position[0],
          "market_index": position[1],
          "avg_entry_price_e30": position[2],
          "entry_borrowing_rate": position[3],
          "reserve_value_e30": position[4],
          "last_increase_timestamp": position[5],
          "position_size_e30": position[6],
          "realized_pnl": position[7],
          "last_funding_accrued": position[8],
          "sub_account_id": position[9],
          "last_increase_size": last_increase_size,
        }
        sub_account_position.append(_position)

      position_data[sub_account_id] = sub_account_position

    return position_data

  def __multicall_all_market_data(self):
    ACTIVE_MARKET = [
      x for x in self.market_profile.keys()]
    market_config_calls = list(map(lambda market_index: self.multicall_instance.create_call(
        self.config_storage_instance, "marketConfigs", [market_index]
      ), ACTIVE_MARKET))

    market_data_calls = list(map(lambda market_index: self.multicall_instance.create_call(
        self.perp_storage_instance, "markets", [market_index]
      ), ACTIVE_MARKET))

    trade_config_call = [self.multicall_instance.create_call(
        self.config_storage_instance, "tradingConfig", []
      )]

    market_calls = market_config_calls + market_data_calls + trade_config_call

    market_results = self.multicall_instance.call(market_calls)
    data = market_results[1]

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

    (
      funding_interval,
      min_profit_duration,
      dev_fee_rate_bps,
      max_position
    ) = decode(['uint256', 'uint256', 'uint32', 'uint8',], data.pop(0))

    trade_config_data = {
        "funding_interval": funding_interval,
        "min_profit_duration": min_profit_duration,
        "dev_fee_rate_bps": dev_fee_rate_bps,
        "max_position": max_position
      }

    market_asset_class_map = {
      market_index: market_config_data[market_index]['asset_class'] for market_index in ACTIVE_MARKET}

    asset_class_list = list(set(market_asset_class_map.values()))

    asset_class_config_calls = list(map(lambda asset_class: self.multicall_instance.create_call(
        self.config_storage_instance, "assetClassConfigs", [asset_class]
      ), asset_class_list))

    asset_class_calls = list(map(lambda asset_class: self.multicall_instance.create_call(
        self.perp_storage_instance, "assetClasses", [asset_class]
      ), asset_class_list))

    asset_call = asset_class_config_calls + asset_class_calls

    asset_result = self.multicall_instance.call(
      asset_call)
    data = asset_result[1]

    asset_class_config_data = {}

    for asset_class in asset_class_list:
      base_borrowing_rate = int(data.pop(0).hex(), 16)
      asset_class_config_data[asset_class] = {
        "base_borrowing_rate": base_borrowing_rate
      }

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

    price = self.oracle_middleware.get_price(
      self.market_profile[market_index]["asset"])
    asset_decimal = self.market_profile[market_index]["display_decimal"]
    if buy is None and size is None:
      return {
        "market": self.market_profile[market_index]["name"],
        "price": round(price, asset_decimal),
        "adaptive_price": None,
        "price_impact": None,
      }
    data = self.__multicall_market_data(market_index)
    oracle_price = price * 10**30
    adaptive_price = Calculator.get_adaptive_price(
      oracle_price,
      data["market"]["long_position_size"],
      data["market"]["short_position_size"],
      data["market_config"]["max_skew_scale_usd"],
      Web3.to_wei(size, "tether") if buy else -Web3.to_wei(size, "tether")
    )
    price_impact = (adaptive_price * 10**30 // oracle_price) - 10**30

    return {
      "market": self.market_profile[market_index]["name"],
      "price": round(oracle_price / 10**30, asset_decimal),
      "adaptive_price": round(adaptive_price / 10**30, asset_decimal),
      "price_impact": price_impact * 100 / 10**30,
    }

  def get_multiple_price(self, market_indices: List[int] = []):
    if not market_indices:
      market_indices = list(
        set(self.market_profile.keys()) - set(DELISTED_MARKET))

    asset_ids = list(
      map(lambda market_index: self.market_profile[market_index]["asset"], market_indices))

    price_object = self.oracle_middleware.get_multiple_price(
        asset_ids
      )

    market_prices = {}

    for market_index in market_indices:
      asset_id = self.market_profile[market_index]["asset"]
      asset_decimal = self.market_profile[market_index]["display_decimal"]
      price = round(
        price_object[asset_id], asset_decimal)
      market_prices[market_index] = price

    return market_prices

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
      "market": self.market_profile[market_index]["name"],
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

    market_prices = self.get_multiple_price()

    for market_index in self.market_profile.keys():
      if market_index not in DELISTED_MARKET:
        current_raw_market_data = raw_market_data[market_index]
        price = market_prices[market_index]
        funding_rate = Calculator.get_funding_rate(
          current_raw_market_data["trading_config"],
          current_raw_market_data["market_config"],
          current_raw_market_data["market"],
          block["timestamp"],
        )

        borrowing_rate = Calculator.get_borrowing_rate(
          current_raw_market_data["asset_class_config"], current_raw_market_data["asset_class"], tvl)

        market_info[market_index] = {
          "market": self.market_profile[market_index]["name"],
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

  def get_position_id(self, account: str, sub_account_id: int, market_index: int):
    return Web3.solidity_keccak(
      ['address', 'uint256'],
      [get_sub_account(account, sub_account_id), market_index]
    )

  def get_all_position_info(self, account: str, sub_account_id: int | List[int] = []):
    if type(sub_account_id) == int:
      sub_account_id = [sub_account_id]
    market_datas = self.__multicall_all_market_data()
    tvl = self.__get_hlp_tvl()
    block = self.__get_block()

    positions = self.__get_all_position(account, sub_account_id)

    positions_flat = [
        x for y in list(positions.values()) for x in y]

    active_market_list = list(set(
      map(lambda position: position['market_index'], positions_flat)))

    adaptive_fee_infos = self.__get_adaptive_fee_infos(active_market_list)

    maker_taker_fee_infos = self.__get_maker_taker_fee_e8(active_market_list)

    price_map = self.get_multiple_price(active_market_list)

    position_infos = []

    for position in positions_flat:
      market_index = position['market_index']
      market_data = market_datas[market_index]

      position_reserved_value = position['reserve_value_e30']
      asset_class_reserved_value = market_data["asset_class"]["reserve_value_e30"]
      sum_borrowing_rate = market_data['asset_class']['sum_borrowing_rate']
      entry_borrowing_rate = position['entry_borrowing_rate']
      price = price_map[market_index] * 10**30

      pnl = Calculator.get_pnl(
        position, market_data["market"], market_data["market_config"], market_data["trading_config"], price, block["timestamp"])

      current_funding_accrued = Calculator.get_next_funding_accrued(
        market_data["trading_config"], market_data["market_config"], market_data["market"], block["timestamp"])

      funding_fee = Calculator.get_funding_fee(
        position["position_size_e30"], int(current_funding_accrued), position["last_funding_accrued"])

      next_borrowing_rate = Calculator.get_next_borrowing_rate(
        market_data['asset_class_config']['base_borrowing_rate'],
        asset_class_reserved_value,
        tvl,
        block["timestamp"],
        market_data["asset_class"]['last_borrowing_time'],
        market_data["trading_config"]['funding_interval'])

      borrowing_fee = Calculator.get_borrowing_fee(reserved_value=position_reserved_value, sum_borrowing_rate=(
        sum_borrowing_rate + next_borrowing_rate), entry_borrowing_rate=entry_borrowing_rate)

      base_fee_bps = market_data["market_config"]["decrease_position_fee_rate_bps"]

      skew = market_data["market"]["long_position_size"] - \
          market_data["market"]["short_position_size"]

      trading_fee = Calculator.get_trading_fee(
        position["position_size_e30"] * -1, base_fee_bps, skew, adaptive_fee_infos[market_index], maker_taker_fee_infos[market_index])

      position_info = {
        "primary_account": position["primary_account"],
        "sub_account_id": position["sub_account_id"],
        "market": self.market_profile[market_index]["name"],
        "position_size": position["position_size_e30"] / 10**30,
        "avg_entry_price": position["avg_entry_price_e30"] / 10**30,
        "pnl": pnl / 10**30,
        "funding_fee": funding_fee / 10**30,
        "borrowing_fee": borrowing_fee / 10**30,
        "trading_fee": trading_fee / 10**30
      }
      position_infos.append(position_info)

    return position_infos

  def get_position_info(self, account: str, sub_account_id: int, market_index: int):
    market_data = self.__multicall_market_data(market_index)
    tvl = self.__get_hlp_tvl()

    position = self.__get_position(account, sub_account_id, market_index)

    adaptive_fee_infos = self.__get_adaptive_fee_infos([market_index])

    maker_taker_fee_infos = self.__get_maker_taker_fee_e8([market_index])

    position_reserved_value = position['reserve_value_e30']
    asset_class_reserved_value = market_data["asset_class"]["reserve_value_e30"]

    sum_borrowing_rate = market_data['asset_class']['sum_borrowing_rate']
    entry_borrowing_rate = position['entry_borrowing_rate']
    block = self.__get_block()
    price = int(self.oracle_middleware.get_price(
        self.market_profile[market_index]["asset"]) * 10 ** 30)

    pnl = Calculator.get_pnl(
      position, market_data["market"], market_data["market_config"], market_data["trading_config"], price, block["timestamp"])

    current_funding_accrued = Calculator.get_next_funding_accrued(
      market_data["trading_config"], market_data["market_config"], market_data["market"], block["timestamp"])

    funding_fee = Calculator.get_funding_fee(
      position["position_size_e30"], current_funding_accrued, position["last_funding_accrued"])

    next_borrowing_rate = Calculator.get_next_borrowing_rate(
      market_data['asset_class_config']['base_borrowing_rate'],
      asset_class_reserved_value,
      tvl,
      block["timestamp"],
      market_data["asset_class"]['last_borrowing_time'],
      market_data["trading_config"]['funding_interval'])

    borrowing_fee = Calculator.get_borrowing_fee(reserved_value=position_reserved_value, sum_borrowing_rate=(
      sum_borrowing_rate + next_borrowing_rate), entry_borrowing_rate=entry_borrowing_rate)
    base_fee_bps = market_data["market_config"]["decrease_position_fee_rate_bps"]

    skew = market_data["market"]["long_position_size"] - \
        market_data["market"]["short_position_size"]

    trading_fee = Calculator.get_trading_fee(
        position["position_size_e30"] * -1, base_fee_bps, skew, adaptive_fee_infos[market_index], maker_taker_fee_infos[market_index])

    return {
      "primary_account": position["primary_account"],
      "sub_account_id": position["sub_account_id"],
      "market": self.market_profile[market_index]["name"],
      "position_size": position["position_size_e30"] / 10**30,
      "avg_entry_price": position["avg_entry_price_e30"] / 10**30,
      "pnl": pnl / 10**30,
      "funding_fee": funding_fee / 10**30,
      "borrowing_fee": borrowing_fee / 10**30,
      "trading_fee": trading_fee / 10**30
    }

  def get_adaptive_fee(self, size_delta: int, market_index: int, is_increase: bool):
    base_fee_bps = 7
    raw_market_config = self.config_storage_instance.functions.getMarketConfigByIndex(
      market_index).call()
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

    raw_fee = self.trade_helper_instance.functions.getAdaptiveFeeBps(
      size_delta, market_index, base_fee_bps).call()
    fee = Web3.to_int(raw_fee)

    return fee

  def get_equity(self, account: str, sub_account_id: int):
    return self.calculator_instance.functions.getEquity(get_sub_account(account, sub_account_id), 0, BYTE_ZERO).call() / 10 ** 30

  def get_leverage(self, account: str, sub_account_id: int):
    equity = self.get_equity(account, sub_account_id)

    if equity == 0:
      return 0

    positions = self.get_all_position_info(account, [sub_account_id])

    sizes = sum(map(lambda position: abs(position["position_size"]), positions))

    return sizes / equity

  def get_collaterals(self, account: str, sub_account_id: int):

    sub_account_address = get_sub_account(account, sub_account_id)
    collateral_address_list = get_collateral_address_list(self.chain_id)
    collateral_address_asset_map = get_collateral_address_asset_map(
      self.chain_id)

    # filter for blast
    if is_blast_chain(self.chain_id):
      token_profile = get_token_profile(self.chain_id)
      weth_address = token_profile["WETH"]["address"]
      usdb_address = token_profile["USDB"]["address"]
      collateral_address_list.remove(weth_address)
      collateral_address_asset_map.pop(weth_address)
      collateral_address_list.remove(usdb_address)
      collateral_address_asset_map.pop(usdb_address)

    token_profile = get_token_profile(self.chain_id)

    token_config_calls = [self.multicall_instance.create_call(
      self.config_storage_instance,
      "getCollateralTokenConfigs",
      [token_address]
    ) for token_address in collateral_address_list]

    token_configs_raw = self.multicall_instance.call(token_config_calls)[1]

    token_configs = {}

    for index, token_config in enumerate(token_configs_raw):
      collateral_address = collateral_address_list[index]
      data = decode(['address', 'uint32', 'bool'], token_config)
      token_configs[collateral_address] = {
        "settle_strategy": data[0],
        "collateral_factor_bps": data[1],
        "accepted": data[2],
      }

    calls = [
      self.multicall_instance.create_call(
        self.vault_storage_instance,
          "traderBalances",
          [sub_account_address, collateral],
      )
      for collateral in collateral_address_list
    ]

    collateral_asset_ids_list = list(map(
      lambda collateral: collateral_address_asset_map[collateral], collateral_address_list))

    collateral_price_dict = self.oracle_middleware.get_multiple_price(
        collateral_asset_ids_list
      )

    results = self.multicall_instance.call(calls)

    ret = {}
    for index, collateral in enumerate(collateral_address_list):
      amount = int(
          results[1][index].hex(), 16) / 10 ** token_profile[collateral]["decimals"]
      collatral_factor = token_configs[collateral]["collateral_factor_bps"] / BPS
      ret[token_profile[collateral]["symbol"]] = {
        'amount': amount,
        'value_usd': amount * collateral_price_dict[token_profile[collateral]["asset"]] * collatral_factor,
        'value_without_factor_usd': amount * collateral_price_dict[token_profile[collateral]["asset"]]
      }

    return ret

  def get_active_intent_orders(self, address: str, sub_account_id: int):
    return self.__get_intent_trade_orders_api(address, sub_account_id)

  def __get_intent_trade_orders_api(self, address: str, sub_account_id: int):
    params = {
      "chainId": self.chain_id,
      "status": IntentOrderStatus.Pending,
    }
    return r.get(f'{INTENT_TRADE_API}/v1/intent-handler/{address}/{sub_account_id}/trade-orders', headers={'Content-Type': 'application/json'}, params=params)

  def get_collateral_without_factor_usd(self, account: str, sub_account_id: int):
    collaterals = self.get_collaterals(account, sub_account_id)
    total_value_without_factor_usd = sum(v["value_without_factor_usd"]
                                         for v in collaterals.values())

    return total_value_without_factor_usd

  def get_collateral_usd(self, account: str, sub_account_id: int):
    collaterals = self.get_collaterals(account, sub_account_id)
    total_value_usd = sum(v["value_usd"] for v in collaterals.values())

    return total_value_usd

  def get_total_pnl_and_fee(self, account: str, sub_account_id: int):
    positions = self.get_all_position_info(account, sub_account_id)
    total_pnl_usd = sum(position["pnl"]
                        for position in positions)
    total_fee_usd = sum(position["funding_fee"] +
                        position["borrowing_fee"] + position["trading_fee"]
                        for position in positions)
    return {
      "total_pnl_usd": total_pnl_usd,
      "total_fee_usd": total_fee_usd
    }

  def get_portfolio_value(self, account: str, sub_account_id: int):
    vault_storage_state = self.__get_trader_vault_state(account, sub_account_id)
    collateral_without_factor = self.get_collateral_without_factor_usd(
      account, sub_account_id)

    pnl_and_fee = self.get_total_pnl_and_fee(account, sub_account_id)

    total_pnl_and_fee = pnl_and_fee["total_pnl_usd"] - \
        pnl_and_fee["total_fee_usd"]

    portfolio_value = collateral_without_factor \
        + total_pnl_and_fee \
        - vault_storage_state["trading_fee"] \
        - vault_storage_state["borrowing_fee"] \
        - vault_storage_state["funding_fee"] \
        - vault_storage_state["loss_fee"]

    return max(portfolio_value, 0)

  def __get_adaptive_fee_infos(self, market_indices: List[int]):

    adaptive_fee_info = {k: None for k in market_indices}

    is_adaptive_fee_enabled_calls = [self.multicall_instance.create_call(
      self.config_storage_instance,
      "isAdaptiveFeeEnabledByMarketIndex",
      [market_index]
    ) for market_index in market_indices
    ]

    is_adaptive_fee_enabled_data_raw = self.multicall_instance.call(
      is_adaptive_fee_enabled_calls)[1]

    is_adaptive_fee_enabled_data = {}

    for index, market_index in enumerate(market_indices):
      is_adaptive_fee_enabled_data[market_index] = decode(
        ['bool'], is_adaptive_fee_enabled_data_raw[index])[0]

    adaptive_fee_market_indices = [
      k for k, v in is_adaptive_fee_enabled_data.items() if v]

    if len(adaptive_fee_market_indices) == 0:
      return adaptive_fee_info

    orderbook_calls = [self.multicall_instance.create_call(
        self.orderbook_oracle_instance,
        "getData",
        [market_index]
    ) for market_index in adaptive_fee_market_indices]

    epoch_volume_buy_calls = [self.multicall_instance.create_call(
      self.perp_storage_instance,
      "getEpochVolume",
      [True, market_index]
    ) for market_index in adaptive_fee_market_indices]

    epoch_volume_sell_calls = [self.multicall_instance.create_call(
      self.perp_storage_instance,
      "getEpochVolume",
      [False, market_index]
    ) for market_index in adaptive_fee_market_indices]

    max_adaptive_fee_bps_call = self.multicall_instance.create_call(
      self.trade_helper_instance,
      "maxAdaptiveFeeBps",
      []
    )

    k1_call = self.multicall_instance.create_call(
      self.adaptive_fee_calculator_instance,
      "k1",
      []
    )

    k2_call = self.multicall_instance.create_call(
      self.adaptive_fee_calculator_instance,
      "k2",
      []
    )

    adaptive_fee_calculator_calls = orderbook_calls + epoch_volume_buy_calls + \
        epoch_volume_sell_calls + \
        [max_adaptive_fee_bps_call] + [k1_call] + [k2_call]

    contract_data = self.multicall_instance.call(
      adaptive_fee_calculator_calls)
    adaptive_fee_calculator_data_raw = contract_data[1]

    orderbook_data_raw = adaptive_fee_calculator_data_raw[0: len(
      adaptive_fee_market_indices)]
    del adaptive_fee_calculator_data_raw[0: len(adaptive_fee_market_indices)]

    epoch_volume_buy_data_raw = adaptive_fee_calculator_data_raw[0: len(
      adaptive_fee_market_indices)]
    del adaptive_fee_calculator_data_raw[0: len(adaptive_fee_market_indices)]

    epoch_volume_sell_data_raw = adaptive_fee_calculator_data_raw[0: len(
      adaptive_fee_market_indices)]
    del adaptive_fee_calculator_data_raw[0: len(adaptive_fee_market_indices)]

    orderbook_data = {}
    epoch_volume_buy_data = {}
    epoch_volume_sell_data = {}

    for index, market_index in enumerate(adaptive_fee_market_indices):
      orderbook_data[market_index] = decode(
        ['uint256', 'uint256', 'uint256'], orderbook_data_raw[index])
      epoch_volume_buy_data[market_index] = decode(
        ['uint256'], epoch_volume_buy_data_raw[index])
      epoch_volume_sell_data[market_index] = decode(
        ['uint256'], epoch_volume_sell_data_raw[index])

      max_adaptive_fee_bps, k1, k2 = (decode(
        ['uint32'], adaptive_fee_calculator_data_raw[
            0]),
          decode(
        ['uint256'], adaptive_fee_calculator_data_raw[
            1]),
          decode(
        ['uint256'], adaptive_fee_calculator_data_raw[
            2]))

    for index, market_index in enumerate(adaptive_fee_market_indices):
      adaptive_fee_info[market_index] = {
        "ask": orderbook_data[market_index][0],
        "bid": orderbook_data[market_index][1],
        "coeff": orderbook_data[market_index][2],
        "epoch_volume": {
          "buy": epoch_volume_buy_data[market_index][0],
          "sell": epoch_volume_sell_data[market_index][0],
        },
        "max_adaptive_fee_bps": max_adaptive_fee_bps[0],
        "adaptive_fee_calculator": {
          "k1": k1[0],
          "k2": k2[0]
        }
      }

    return adaptive_fee_info

  def __get_maker_taker_fee_e8(self, market_indices: List[int]):

    maker_taker_fee_infos = {
      k: {
          "maker_fee_e8": 0,
          "taker_fee_e8": 0
      } for k in market_indices}

    contract_calls = [
      self.multicall_instance.create_call(
          self.config_storage_instance,
          "makerFeeE8ByMarketIndex", [market_index]
      ) for market_index in market_indices] + [
      self.multicall_instance.create_call(
          self.config_storage_instance,
          "takerFeeE8ByMarketIndex", [market_index]
      ) for market_index in market_indices]

    contract_data = self.multicall_instance.call(contract_calls)[1]

    maker_fee_raw = contract_data[0: len(
      market_indices)]
    del contract_data[0: len(market_indices)]

    taker_fee_raw = contract_data[0: len(
      market_indices)]
    del contract_data[0: len(market_indices)]

    for index, market_index in enumerate(market_indices):
      maker_taker_fee_infos[market_index] = {
        "maker_fee_e8": decode(['uint256'], maker_fee_raw[index])[0],
        "taker_fee_e8": decode(['uint256'], taker_fee_raw[index])[0]
      }

    return maker_taker_fee_infos

  def __get_trader_vault_state(self, account: str, sub_account_id: int):
    sub_account = get_sub_account(account, sub_account_id)

    trading_fee_call = self.multicall_instance.create_call(
      self.vault_storage_instance, "tradingFeeDebt", [sub_account])
    borrowing_fee_call = self.multicall_instance.create_call(
      self.vault_storage_instance, "borrowingFeeDebt", [sub_account])
    funding_fee_call = self.multicall_instance.create_call(
      self.vault_storage_instance, "fundingFeeDebt", [sub_account])
    loss_fee_call = self.multicall_instance.create_call(
      self.vault_storage_instance, "lossDebt", [sub_account])

    contract_calls = [trading_fee_call,
                      borrowing_fee_call,
                      funding_fee_call,
                      loss_fee_call]

    contract_raw_data = self.multicall_instance.call(contract_calls)[1]

    trading_fee = decode(['uint256'], contract_raw_data[0])[0]
    borrowing_fee = decode(['uint256'], contract_raw_data[1])[0]
    funding_fee = decode(['uint256'], contract_raw_data[2])[0]
    loss_fee = decode(['uint256'], contract_raw_data[3])[0]

    return {
      "trading_fee": trading_fee,
      "borrowing_fee": borrowing_fee,
      "funding_fee": funding_fee,
      "loss_fee": loss_fee
    }
