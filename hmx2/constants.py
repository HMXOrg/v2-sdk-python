# ------ Pyth Network ------
DEFAULT_PYTH_PRICE_SERVICE_URL = "https://hermes.pyth.network"

# ------ Contract Address ------
MULTICALL_ADDRESS = "0xcA11bde05977b3631167028862bE2a173976CA11"
CROSS_MARGIN_HANDLER_ADDRESS = "0xB189532c581afB4Fbe69aF6dC3CD36769525d446"
LIMIT_TRADE_HANDLER_ADDRESS = "0xeE116128b9AAAdBcd1f7C18608C5114f594cf5D6"
VAULT_STORAGE_ADDRESS = "0x56CC5A9c0788e674f17F7555dC8D3e2F1C0313C0"
GLP_MANAGER_ADDRESS = "0x3963FfC9dff443c2A94f21b129D429891E32ec18"
PERP_STORAGE_ADDRESS = "0x97e94BdA44a2Df784Ab6535aaE2D62EFC6D2e303"
CONFIG_STORAGE_ADDRESS = "0xF4F7123fFe42c4C90A4bCDD2317D397E0B7d7cc0"
DIX_PRICE_ADAPTER_ADDRESS = "0x222918d230c5A29F334fFb3020aD57b8CeBD1B82"
GM_BTC_PRICE_ADAPTER_ADDRESS = "0x85680bba8a94c9be1DDd7Be802885DFCe95F8164"
GM_ETH_PRICE_ADAPTER_ADDRESS = "0x700083c72eBc86CbFc865830F5706a2DbC392f26"
TRADE_HELPER_ADDRESS = "0x963Cbe4cFcDC58795869be74b80A328b022DE00C"
ONCHAIN_PRICELENS_ADDRESS = "0x7D8eAa8dF02526c711F4ff1f97F6c5324212DBBa"
CALCULATOR_ADDRESS = "0x0FdE910552977041Dc8c7ef652b5a07B40B9e006"

# ------ ABI Path ------
ERC20_ABI_PATH = "abis/ERC20.json"
CROSS_MARGIN_HANDLER_ABI_PATH = "abis/CrossMarginHandler.json"
LIMIT_TRADE_HANDLER_ABI_PATH = "abis/LimitTradeHandler.json"
VAULT_STORAGE_ABI_PATH = "abis/VaultStorage.json"
GLP_MANAGER_ABI_PATH = "abis/GlpManager.json"
PERP_STORAGE_ABI_PATH = "abis/PerpStorage.json"
CONFIG_STORAGE_ABI_PATH = "abis/ConfigStorage.json"
CIX_PRICE_ADAPTER_ABI_PATH = "abis/CIXPriceAdapter.json"
GM_PRICE_ADAPTER_ABI_PATH = "abis/GMPriceAdapter.json"
TRADE_HELPER_ABI_PATH = "abis/TradeHelper.json"
ONCHAIN_PRICELENS_ABI_PATH = "abis/OnchainPricelens.json"
CALCULATOR_ABI_PATH = "abis/Calculator.json"

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

# ------ Token Profiles ------
TOKEN_PROFILE = {
  "USDC.e": {
    "symbol": "USDC.e",
    "address": "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
    "decimals": 6
  },
  "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8": {
    "symbol": "USDC.e",
    "address": "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
    "decimals": 6
  },
  "USDT": {
    "symbol": "USDT",
    "address": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
    "decimals": 6
  },
  "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9": {
    "symbol": "USDT",
    "address": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
    "decimals": 6
  },
  "DAI": {
    "symbol": "DAI",
    "address": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
    "decimals": 18
  },
  "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1": {
    "symbol": "DAI",
    "address": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
    "decimals": 18
  },
  "WETH": {
    "symbol": "WETH",
    "address": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
    "decimals": 18
  },
  "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1": {
    "symbol": "WETH",
    "address": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
    "decimals": 18
  },
  "WBTC": {
    "symbol": "WBTC",
    "address": "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f",
    "decimals": 8
  },
  "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f": {
    "symbol": "WBTC",
    "address": "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f",
    "decimals": 8
  },
  "sGLP": {
    "symbol": "sGLP",
    "address": "0x5402B5F40310bDED796c7D0F3FF6683f5C0cFfdf",
    "decimals": 18
  },
  "0x5402B5F40310bDED796c7D0F3FF6683f5C0cFfdf": {
    "symbol": "sGLP",
    "address": "0x5402B5F40310bDED796c7D0F3FF6683f5C0cFfdf",
    "decimals": 18
  },
  "ARB": {
    "symbol": "ARB",
    "address": "0x912CE59144191C1204E64559FE8253a0e49E6548",
    "decimals": 18
  },
  "0x912CE59144191C1204E64559FE8253a0e49E6548": {
    "symbol": "ARB",
    "address": "0x912CE59144191C1204E64559FE8253a0e49E6548",
    "decimals": 18
  },
  "wstETH": {
    "symbol": "wstETH",
    "address": "0x5979D7b546E38E414F7E9822514be443A4800529",
    "decimals": 18
  },
  "0x5979D7b546E38E414F7E9822514be443A4800529": {
    "symbol": "wstETH",
    "address": "0x5979D7b546E38E414F7E9822514be443A4800529",
    "decimals": 18
  },
  "USDC": {
    "symbol": "USDC",
    "address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    "decimals": 6
  },
  "0xaf88d065e77c8cC2239327C5EDb3A432268e5831": {
    "symbol": "USDC",
    "address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    "decimals": 6
  },
  "gmBTC": {
    "symbol": "gmBTC",
    "address": "0x47c031236e19d024b42f8AE6780E44A573170703",
    "decimals": 18
  },
  "0x47c031236e19d024b42f8AE6780E44A573170703": {
    "symbol": "gmBTC",
    "address": "0x47c031236e19d024b42f8AE6780E44A573170703",
    "decimals": 18
  },
  "gmETH": {
    "symbol": "gmETH",
    "address": "0x70d95587d40A2caf56bd97485aB3Eec10Bee6336",
    "decimals": 18
  },
  "0x70d95587d40A2caf56bd97485aB3Eec10Bee6336": {
    "symbol": "gmETH",
    "address": "0x70d95587d40A2caf56bd97485aB3Eec10Bee6336",
    "decimals": 18
  },
}

# ------ Collaterals ------
COLLATERAL_USDCe = TOKEN_PROFILE["USDC.e"]["address"]
COLLATERAL_USDT = TOKEN_PROFILE["USDT"]["address"]
COLLATERAL_DAI = TOKEN_PROFILE["DAI"]["address"]
COLLATERAL_WETH = TOKEN_PROFILE["WETH"]["address"]
COLLATERAL_WBTC = TOKEN_PROFILE["WBTC"]["address"]
COLLATERAL_sGLP = TOKEN_PROFILE["sGLP"]["address"]
COLLATERAL_ARB = TOKEN_PROFILE["ARB"]["address"]
COLLATERAL_wstETH = TOKEN_PROFILE["wstETH"]["address"]
COLLATERAL_USDC = TOKEN_PROFILE["USDC"]["address"]
COLLATERAL_gmBTC = TOKEN_PROFILE["gmBTC"]["address"]
COLLATERAL_gmETH = TOKEN_PROFILE["gmETH"]["address"]

COLLATERALS = [COLLATERAL_USDCe, COLLATERAL_USDT, COLLATERAL_DAI,
               COLLATERAL_WETH, COLLATERAL_WBTC, COLLATERAL_sGLP, COLLATERAL_ARB,
               COLLATERAL_wstETH, COLLATERAL_USDC, COLLATERAL_gmBTC, COLLATERAL_gmETH]

# ------ Assets ------
ASSET_ETH = "ETH"
ASSET_BTC = "BTC"
ASSET_AAPL = "AAPL"
ASSET_JPY = "JPY"
ASSET_XAU = "XAU"
ASSET_AMZN = "AMZN"
ASSET_MSFT = "MSFT"
ASSET_TSLA = "TSLA"
ASSET_EUR = "EUR"
ASSET_XAG = "XAG"
ASSET_AUD = "AUD"
ASSET_GBP = "GBP"
ASSET_ADA = "ADA"
ASSET_MATIC = "MATIC"
ASSET_SUI = "SUI"
ASSET_ARB = "ARB"
ASSET_OP = "OP"
ASSET_LTC = "LTC"
ASSET_COIN = "COIN"
ASSET_GOOG = "GOOG"
ASSET_BNB = "BNB"
ASSET_SOL = "SOL"
ASSET_QQQ = "QQQ"
ASSET_XRP = "XRP"
ASSET_USDC = "USDC"
ASSET_USDT = "USDT"
ASSET_DAI = "DAI"
ASSET_GLP = "GLP"
ASSET_NVDA = "NVDA"
ASSET_LINK = "LINK"
ASSET_CHF = "CHF"
ASSET_DOGE = "DOGE"
ASSET_CAD = "CAD"
ASSET_SGD = "SGD"
ASSET_CNH = "CNH"
ASSET_wstETH = "wstETH"
ASSET_HKD = "HKD"
ASSET_BCH = "BCH"
ASSET_MEME = "MEME"
ASSET_gmBTC = "gmBTC"
ASSET_gmETH = "gmETH"
ASSET_SEK = "SEK"
ASSET_DIX = "DIX"
ASSET_JTO = "JTO"
ASSET_STX = "STX"
ASSET_ORDI = "ORDI"
ASSET_TIA = "TIA"
ASSET_AVAX = "AVAX"
ASSET_INJ = "INJ"
ASSET_DOT = "DOT"
ASSET_SEI = "SEI"
ASSET_ATOM = "ATOM"
ASSET_1000SHIB = "1000SHIB"
ASSET_1000PEPE = "1000PEPE"
ASSET_ICP = "ICP"
ASSET_MANTA = "MANTA"

ASSETS = [ASSET_ETH, ASSET_BTC, ASSET_AAPL, ASSET_JPY, ASSET_XAU, ASSET_AMZN,
          ASSET_MSFT, ASSET_TSLA, ASSET_EUR, ASSET_XAG, ASSET_AUD, ASSET_GBP,
          ASSET_ADA, ASSET_MATIC, ASSET_SUI, ASSET_ARB, ASSET_OP, ASSET_LTC,
          ASSET_COIN, ASSET_GOOG, ASSET_BNB, ASSET_SOL, ASSET_QQQ, ASSET_XRP,
          ASSET_USDC, ASSET_USDT, ASSET_DAI, ASSET_GLP, ASSET_NVDA, ASSET_LINK,
          ASSET_CHF, ASSET_DOGE, ASSET_CAD, ASSET_SGD, ASSET_CNH, ASSET_wstETH,
          ASSET_HKD, ASSET_BCH, ASSET_MEME, ASSET_gmBTC, ASSET_gmETH, ASSET_SEK,
          ASSET_DIX, ASSET_JTO, ASSET_STX, ASSET_ORDI, ASSET_TIA, ASSET_AVAX,
          ASSET_INJ, ASSET_DOT, ASSET_SEI, ASSET_ATOM, ASSET_1000SHIB, ASSET_1000PEPE,
          ASSET_ICP, ASSET_MANTA]

# ------ Asset IDs Map ----
COLLATERAL_ASSET_ID_MAP = {
  COLLATERAL_USDCe: ASSET_USDC,
  COLLATERAL_USDT: ASSET_USDT,
  COLLATERAL_DAI: ASSET_DAI,
  COLLATERAL_WETH: ASSET_ETH,
  COLLATERAL_WBTC: ASSET_BTC,
  COLLATERAL_sGLP: ASSET_GLP,
  COLLATERAL_ARB: ASSET_ARB,
  COLLATERAL_wstETH: ASSET_wstETH,
  COLLATERAL_USDC: ASSET_USDC,
  COLLATERAL_gmBTC: ASSET_gmBTC,
  COLLATERAL_gmETH: ASSET_gmETH,
}

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
    "name": "DIXUSD",
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
}

# Address
ADDRESS_ZERO = "0x0000000000000000000000000000000000000000"

# Math
MAX_UINT = 2 ** 256 - 1
BPS = 10000

EXECUTION_FEE = 3 * 10 ** 14

SECONDS = 1
MINUTES = 60
HOURS = 3600
DAYS = 86400
YEARS = 31536000
