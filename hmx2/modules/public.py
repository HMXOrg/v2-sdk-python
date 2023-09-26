from web3 import Web3
from hmx2.constants import (
  TOKEN_PROFILE,
  MULTICALL_ADDRESS,
  VAULT_STORAGE_ADDRESS,
  PERP_STORAGE_ADDRESS,
  CONFIG_STORAGE_ADDRESS,
  VAULT_STORAGE_ABI_PATH,
  PERP_STORAGE_ABI_PATH,
  CONFIG_STORAGE_ABI_PATH,
  COLLATERALS,
  COLLATERAL_ASSET_ID_MAP,
  HOURS,
  DAYS,
  YEARS,
  MARKET_PROFILE
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

  def __get_hlp_tvl(self):
    calls = [
      self.multicall_instance.create_call(
        self.vault_storage_instance, "hlpLiquidity", [collateral])
      for collateral in COLLATERALS
    ]
    collateral_usd = [
      self.oracle_middleware.get_price(
        COLLATERAL_ASSET_ID_MAP[collateral]) * 10**10
      for collateral in COLLATERALS
    ]
    results = self.multicall_instance.call(calls)

    return sum(
      [
        int(results[1][index].hex(), 16) *
          collateral_usd[index] // 10 ** TOKEN_PROFILE[collateral]["decimals"]
          for index, collateral in enumerate(COLLATERALS)
      ]
    )

  def get_price(self, market_index: int, buy: bool, size: float):
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
      "price": oracle_price / 10**30,
      "adaptive_price": adaptive_price / 10**30,
      "price_impact": price_impact * 100 / 10**30,
    }

  def get_market_info(self, market_index: int):
    '''
    Get a market info

    :param market_index: requied
    :type market_index: int in list Market
    '''
    data = self.__multicall_market_data(market_index)
    block = self.__get_block()
    tvl = self.__get_hlp_tvl()

    price = self.oracle_middleware.get_price(
      MARKET_PROFILE[market_index]["asset"])

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
        "1H": borrowing_rate * HOURS / 10**18,
        "8H": borrowing_rate * 8 * HOURS / 10**18,
        "24H": borrowing_rate * DAYS / 10**18,
        "1Y": borrowing_rate * YEARS / 10**18,
      }
    }

  def get_sub_account(self, account: str, sub_account_id: int):
    return Web3.to_checksum_address(hex(int(account, 16) ^ sub_account_id))

  def get_position_id(self, account: str, sub_account_id: int, market_index: int):
    return Web3.solidity_keccak(
      ['address', 'uint256'],
      [self.get_sub_account(account, sub_account_id), market_index]
    )

  def get_position_info(self, account: str, sub_account_id: int, market_index: int):
    data = self.__multicall_market_data(market_index)
    position = self.__get_position(account, sub_account_id, market_index)
    block = self.__get_block()
    price = int(self.oracle_middleware.get_price(
        MARKET_PROFILE[market_index]["asset"]) * 10 ** 30)

    pnl = Calculator.get_pnl(
      position, data["market"], data["market_config"], data["trading_config"], price, block["timestamp"])

    current_funding_accrued = Calculator.get_next_funding_accrued(
      data["trading_config"], data["market_config"], data["market"], block["timestamp"])
    Calculator.get_fuding_fee(
      position["position_size_e30"], current_funding_accrued, position["last_funding_accrued"])

    return {
      "primary_account": position["primary_account"],
      "sub_account_id": position["sub_account_id"],
      "market": MARKET_PROFILE[market_index]["name"],
      "position_size": position["position_size_e30"] / 10**30,
      "avg_entry_price": position["avg_entry_price_e30"] / 10**30,
      "pnl": pnl / 10**30,
    }
