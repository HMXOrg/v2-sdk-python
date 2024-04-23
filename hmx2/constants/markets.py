from hmx2.constants.assets import (
  ASSET_ETH,
  ASSET_BTC,
  ASSET_AAPL,
  ASSET_JPY,
  ASSET_XAU,
  ASSET_AMZN,
  ASSET_MSFT,
  ASSET_TSLA,
  ASSET_EUR,
  ASSET_XAG,
  ASSET_AUD,
  ASSET_GBP,
  ASSET_ADA,
  ASSET_MATIC,
  ASSET_SUI,
  ASSET_ARB,
  ASSET_OP,
  ASSET_LTC,
  ASSET_COIN,
  ASSET_GOOG,
  ASSET_BNB,
  ASSET_SOL,
  ASSET_QQQ,
  ASSET_XRP,
  ASSET_NVDA,
  ASSET_LINK,
  ASSET_CHF,
  ASSET_DOGE,
  ASSET_CAD,
  ASSET_SGD,
  ASSET_CNH,
  ASSET_HKD,
  ASSET_BCH,
  ASSET_MEME,
  ASSET_DIX,
  ASSET_JTO,
  ASSET_STX,
  ASSET_ORDI,
  ASSET_TIA,
  ASSET_AVAX,
  ASSET_INJ,
  ASSET_DOT,
  ASSET_SEI,
  ASSET_ATOM,
  ASSET_1000PEPE,
  ASSET_1000SHIB,
  ASSET_SEK,
  ASSET_ICP,
  ASSET_MANTA,
  ASSET_STRK,
  ASSET_PYTH,
  ASSET_PENDLE,
  ASSET_W,
  ASSET_ENA,
)


# ------ Market ------
MARKET_ETH_USD = 0
MARKET_BTC_USD = 1
MARKET_AAPL_USD = 2
MARKET_JPY_USD = 3
MARKET_XAU_USD = 4
MARKET_AMZN_USD = 5
MARKET_MSFT_USD = 6
MARKET_TSLA_USD = 7
MARKET_EUR_USD = 8
MARKET_XAG_USD = 9
MARKET_AUD_USD = 10
MARKET_GBP_USD = 11
MARKET_ADA_USD = 12
MARKET_MATIC_USD = 13
MARKET_SUI_USD = 14
MARKET_ARB_USD = 15
MARKET_OP_USD = 16
MARKET_LTC_USD = 17
MARKET_COIN_USD = 18
MARKET_GOOG_USD = 19
MARKET_BNB_USD = 20
MARKET_SOL_USD = 21
MARKET_QQQ_USD = 22
MARKET_XRP_USD = 23
MARKET_NVDA_USD = 24
MARKET_LINK_USD = 25
MARKET_USD_CHF = 26
MARKET_DOGE_USD = 27
MARKET_USD_CAD = 28
MARKET_USD_SGD = 29
MARKET_USD_CNH = 30
MARKET_USD_HKD = 31
MARKET_BCH_USD = 32
MARKET_MEME_USD = 33
MARKET_DIX_USD = 34
MARKET_JTO_USD = 35
MARKET_STX_USD = 36
MARKET_ORDI_USD = 37
MARKET_TIA_USD = 38
MARKET_AVAX_USD = 39
MARKET_INJ_USD = 40
MARKET_DOT_USD = 41
MARKET_SEI_USD = 42
MARKET_ATOM_USD = 43
MARKET_1000PEPE_USD = 44
MARKET_1000SHIB_USD = 45
MARKET_USD_SEK = 46
MARKET_ICP_USD = 47
MARKET_MANTA_USD = 48
MARKET_STRK_USD = 49
MARKET_PYTH_USD = 50
MARKET_PENDLE_USD = 51
MARKET_W_USD = 52
MARKET_ENA_USD = 53


DELISTED_MARKET = [
    MARKET_AAPL_USD,
    MARKET_AMZN_USD,
    MARKET_MSFT_USD,
    MARKET_TSLA_USD,
    MARKET_COIN_USD,
    MARKET_GOOG_USD,
    MARKET_QQQ_USD,
    MARKET_NVDA_USD
]

# ------ Market ----
MARKET_PROFILE = {
  MARKET_ETH_USD: {
    "name": "ETHUSD",
    "asset": ASSET_ETH,
    "display_decimal": 2,
  },
  MARKET_BTC_USD: {
    "name": "BTCUSD",
    "asset": ASSET_BTC,
    "display_decimal": 2,
  },
  MARKET_AAPL_USD: {
    "name": "AAPLUSD",
    "asset": ASSET_AAPL,
    "display_decimal": 2,
  },
  MARKET_JPY_USD: {
    "name": "JPYUSD",
    "asset": ASSET_JPY,
    "display_decimal": 8,
  },
  MARKET_XAU_USD: {
    "name": "XAUUSD",
    "asset": ASSET_XAU,
    "display_decimal": 2,
  },
  MARKET_AMZN_USD: {
    "name": "AMZNUSD",
    "asset": ASSET_AMZN,
    "display_decimal": 2,
  },
  MARKET_MSFT_USD: {
    "name": "MSFTUSD",
    "asset": ASSET_MSFT,
    "display_decimal": 2,
  },
  MARKET_TSLA_USD: {
    "name": "TSLAUSD",
    "asset": ASSET_TSLA,
    "display_decimal": 2,
  },
  MARKET_EUR_USD: {
    "name": "EURUSD",
    "asset": ASSET_EUR,
    "display_decimal": 5,
  },
  MARKET_XAG_USD: {
    "name": "XAGUSD",
    "asset": ASSET_XAG,
    "display_decimal": 3,
  },
  MARKET_AUD_USD: {
    "name": "AUDUSD",
    "asset": ASSET_AUD,
    "display_decimal": 5,
  },
  MARKET_GBP_USD: {
    "name": "GBPUSD",
    "asset": ASSET_GBP,
    "display_decimal": 5,
  },
  MARKET_ADA_USD: {
    "name": "ADAUSD",
    "asset": ASSET_ADA,
    "display_decimal": 4,
  },
  MARKET_MATIC_USD: {
    "name": "MATICUSD",
    "asset": ASSET_MATIC,
    "display_decimal": 4,
  },
  MARKET_SUI_USD: {
    "name": "SUIUSD",
    "asset": ASSET_SUI,
    "display_decimal": 4,
  },
  MARKET_ARB_USD: {
    "name": "ARBUSD",
    "asset": ASSET_ARB,
    "display_decimal": 4,
  },
  MARKET_OP_USD: {
    "name": "OPUSD",
    "asset": ASSET_OP,
    "display_decimal": 4,
  },
  MARKET_LTC_USD: {
    "name": "LTCUSD",
    "asset": ASSET_LTC,
    "display_decimal": 2,
  },
  MARKET_COIN_USD: {
    "name": "COINUSD",
    "asset": ASSET_COIN,
    "display_decimal": 2,
  },
  MARKET_GOOG_USD: {
    "name": "GOOGUSD",
    "asset": ASSET_GOOG,
    "display_decimal": 2,
  },
  MARKET_BNB_USD: {
    "name": "BNBUSD",
    "asset": ASSET_BNB,
    "display_decimal": 2,
  },
  MARKET_SOL_USD: {
    "name": "SOLUSD",
    "asset": ASSET_SOL,
    "display_decimal": 3,
  },
  MARKET_QQQ_USD: {
    "name": "QQQUSD",
    "asset": ASSET_QQQ,
    "display_decimal": 2,
  },
  MARKET_XRP_USD: {
    "name": "XRPUSD",
    "asset": ASSET_XRP,
    "display_decimal": 4,
  },
  MARKET_NVDA_USD: {
    "name": "NVDAUSD",
    "asset": ASSET_NVDA,
    "display_decimal": 2,
  },
  MARKET_LINK_USD: {
    "name": "LINKUSD",
    "asset": ASSET_LINK,
    "display_decimal": 3,
  },
  MARKET_USD_CHF: {
    "name": "USDCHF",
    "asset": ASSET_CHF,
    "display_decimal": 5,
  },
  MARKET_DOGE_USD: {
    "name": "DOGEUSD",
    "asset": ASSET_DOGE,
    "display_decimal": 5,
  },
  MARKET_USD_CAD: {
    "name": "USDCAD",
    "asset": ASSET_CAD,
    "display_decimal": 5,
  },
  MARKET_USD_SGD: {
    "name": "USDSGD",
    "asset": ASSET_SGD,
    "display_decimal": 5,
  },
  MARKET_USD_CNH: {
    "name": "USDCNH",
    "asset": ASSET_CNH,
    "display_decimal": 5,
  },
  MARKET_USD_HKD: {
    "name": "USDHKD",
    "asset": ASSET_HKD,
    "display_decimal": 5,
  },
  MARKET_BCH_USD: {
    "name": "BCHUSD",
    "asset": ASSET_BCH,
    "display_decimal": 2,
  },
  MARKET_MEME_USD: {
    "name": "MEMEUSD",
    "asset": ASSET_MEME,
    "display_decimal": 8,
  },
  MARKET_DIX_USD: {
    "name": "DIX",
    "asset": ASSET_DIX,
    "display_decimal": 4,
  },
  MARKET_JTO_USD: {
    "name": "JTOUSD",
    "asset": ASSET_JTO,
    "display_decimal": 4,
  },
  MARKET_STX_USD: {
    "name": "STXUSD",
    "asset": ASSET_STX,
    "display_decimal": 4,
  },
  MARKET_ORDI_USD: {
    "name": "ORDIUSD",
    "asset": ASSET_ORDI,
    "display_decimal": 3,
  },
  MARKET_TIA_USD: {
    "name": "TIAUSD",
    "asset": ASSET_TIA,
    "display_decimal": 4,
  },
  MARKET_AVAX_USD: {
    "name": "AVAXUSD",
    "asset": ASSET_AVAX,
    "display_decimal": 3,
  },
  MARKET_INJ_USD: {
    "name": "INJUSD",
    "asset": ASSET_INJ,
    "display_decimal": 3,
  },
  MARKET_DOT_USD: {
    "name": "DOTUSD",
    "asset": ASSET_DOT,
    "display_decimal": 3,
  },
  MARKET_SEI_USD: {
    "name": "SEIUSD",
    "asset": ASSET_SEI,
    "display_decimal": 4,
  },
  MARKET_ATOM_USD: {
    "name": "ATOMUSD",
    "asset": ASSET_ATOM,
    "display_decimal": 3,
  },
  MARKET_1000PEPE_USD: {
    "name": "1000PEPEUSD",
    "asset": ASSET_1000PEPE,
    "display_decimal": 8,
  },
  MARKET_1000SHIB_USD: {
    "name": "1000SHIBUSD",
    "asset": ASSET_1000SHIB,
    "display_decimal": 8,
  },
  MARKET_USD_SEK: {
    "name": "USDSEK",
    "asset": ASSET_SEK,
    "display_decimal": 5,
  },
  MARKET_ICP_USD: {
    "name": "ICPUSD",
    "asset": ASSET_ICP,
    "display_decimal": 3,
  },
  MARKET_MANTA_USD: {
    "name": "MANTAUSD",
    "asset": ASSET_MANTA,
    "display_decimal": 3,
  },
  MARKET_STRK_USD: {
    "name": "STRKUSD",
    "asset": ASSET_STRK,
    "display_decimal": 3,
  },
  MARKET_PYTH_USD: {
    "name": "PYTHUSD",
    "asset": ASSET_PYTH,
    "display_decimal": 4,
  },
  MARKET_PENDLE_USD: {
    "name": "PENDLEUSD",
    "asset": ASSET_PENDLE,
    "display_decimal": 4,
  },
  MARKET_W_USD: {
    "name": "WUSD",
    "asset": ASSET_W,
    "display_decimal": 3,
  },
  MARKET_ENA_USD: {
    "name": "ENAUSD",
    "asset": ASSET_ENA,
    "display_decimal": 3,
  },
}
