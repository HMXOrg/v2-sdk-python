import os
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
  ASSET_GLP,
  ASSET_AUD,
  ASSET_GBP,
  ASSET_ADA,
  ASSET_MATIC,
  ASSET_USDC,
  ASSET_USDT,
  ASSET_DAI,
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
)

DEFAULT_FORK_BLOCK = 161496259
DEFAULT_PUBLIC_ADDRESS = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
DEFAULT_KEY = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'
DEFAULT_CHAIN_ID = 42161

UNISWAP_SWAP_ROUTER_02_ADDRESS = '0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45'
MARKET_ORDER_EXECUTIONER_ADDRESS = '0x7FDD623c90a0097465170EdD352Be27A9f3ad817'
ECOPYTH_CALLDATA_BUILDER_ADDRESS = '0xa3187B97CEC0854A5ed3B11ffEeD50E5a1A1593f'

TENDERY_API_BASE_URL = os.getenv("TENDERLY_API_BASE_URL")
TENDERY_ACCESS_TOKEN = os.getenv("TENDERLY_ACCESS_TOKEN")
TENDERY_PROJECT_SLUG = os.getenv("TENDERLY_PROJECT_SLUG")


def get_default_price_data(publish_timestamp, override_price_data):
  default_price_data = [
    {
        'assetId': ASSET_ETH.encode('utf-8'),
        'priceE8': 182828452899,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_BTC.encode('utf-8'),
        'priceE8': 2920914900000,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_USDC.encode('utf-8'),
        'priceE8': 100039949,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_USDT.encode('utf-8'),
        'priceE8': 99835040,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_DAI.encode('utf-8'),
        'priceE8': 100015499,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_AAPL.encode('utf-8'),
        'priceE8': 1774750100,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_JPY.encode('utf-8'),
        'priceE8': 1455940000,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_XAU.encode('utf-8'),
        'priceE8': 19032400000,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_AMZN.encode('utf-8'),
        'priceE8': 1377100000,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_MSFT.encode('utf-8'),
        'priceE8': 3218600000,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_TSLA.encode('utf-8'),
        'priceE8': 2329310000,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_EUR.encode('utf-8'),
        'priceE8': 109077000,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_XAG.encode('utf-8'),
        'priceE8': 2258350000,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_GLP.encode('utf-8'),
        'priceE8': 0,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_AUD.encode('utf-8'),
        'priceE8': 64400000,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_GBP.encode('utf-8'),
        'priceE8': 126972000,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_ADA.encode('utf-8'),
        'priceE8': 29239825,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_MATIC.encode('utf-8'),
        'priceE8': 66939568,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_SUI.encode('utf-8'),
        'priceE8': 66939568,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_ARB.encode('utf-8'),
        'priceE8': 113043042,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_OP.encode('utf-8'),
        'priceE8': 147425000,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_LTC.encode('utf-8'),
        'priceE8': 7929548727,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_COIN.encode('utf-8'),
        'priceE8': 7937380000,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_GOOG.encode('utf-8'),
        'priceE8': 13027000000,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_BNB.encode('utf-8'),
        'priceE8': 23665172637,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_SOL.encode('utf-8'),
        'priceE8': 2392066063,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_QQQ.encode('utf-8'),
        'priceE8': 36653000000,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    },
    {
        'assetId': ASSET_XRP.encode('utf-8'),
        'priceE8': 60739806,
        'publishTime': publish_timestamp,
        'maxDiffBps': 150000
    }
  ]
  # override price data if needed
  if override_price_data is not None:
    for opd in override_price_data:
      for dpd in default_price_data:
        if opd["assetId"].encode('utf-8') == dpd["assetId"]:
          dpd["priceE8"] = opd["priceE8"]
          break
  return default_price_data
