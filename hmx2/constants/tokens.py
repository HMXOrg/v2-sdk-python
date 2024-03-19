from hmx2.constants.assets import (
  ASSET_ARB,
  ASSET_BTC,
  ASSET_DAI,
  ASSET_ETH,
  ASSET_GLP,
  ASSET_USDC,
  ASSET_USDT,
  ASSET_gmBTC,
  ASSET_gmETH,
  ASSET_wstETH
)

# Arbitrum One
COLLATERAL_USDCe = "0xB853c09b6d03098b841300daD57701ABcFA80228"
COLLATERAL_USDT = "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"
COLLATERAL_DAI = "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1"
COLLATERAL_WETH = "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1"
COLLATERAL_WBTC = "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f"
COLLATERAL_sGLP = "0x5402B5F40310bDED796c7D0F3FF6683f5C0cFfdf"
COLLATERAL_ARB = "0x912CE59144191C1204E64559FE8253a0e49E6548"
COLLATERAL_wstETH = "0x5979D7b546E38E414F7E9822514be443A4800529"
COLLATERAL_USDC = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"
COLLATERAL_gmBTC = "0x47c031236e19d024b42f8AE6780E44A573170703"
COLLATERAL_gmETH = "0x70d95587d40A2caf56bd97485aB3Eec10Bee6336"

# Blast Mainnet
COLLATERAL_ybETH = "0xb9d94A3490bA2482E2D4F21F0E76b92E5661Ded8"
COLLATERAL_ybUSDB = "0xCD732d21c1B23A3f84Bb386E9759b5b6A1BcBe39"

# ------ Token Profiles ------
TOKEN_PROFILE = {
  # Arbitrum One
  42161: {
    "USDC.e": {
      "symbol": "USDC.e",
      "address": "0xB853c09b6d03098b841300daD57701ABcFA80228",
      "asset": ASSET_USDC,
      "decimals": 6
    },
    "0xB853c09b6d03098b841300daD57701ABcFA80228": {
      "symbol": "USDC.e",
      "address": "0xB853c09b6d03098b841300daD57701ABcFA80228",
      "asset": ASSET_USDC,
      "decimals": 6
    },
    "USDT": {
      "symbol": "USDT",
      "address": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
      "asset": ASSET_USDT,
      "decimals": 6
    },
    "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9": {
      "symbol": "USDT",
      "address": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
      "asset": ASSET_USDT,
      "decimals": 6
    },
    "DAI": {
      "symbol": "DAI",
      "address": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
      "asset": ASSET_DAI,
      "decimals": 18
    },
    "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1": {
      "symbol": "DAI",
      "address": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
      "asset": ASSET_DAI,
      "decimals": 18
    },
    "WETH": {
      "symbol": "WETH",
      "address": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
      "asset": ASSET_ETH,
      "decimals": 18
    },
    "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1": {
      "symbol": "WETH",
      "address": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
      "asset": ASSET_ETH,
      "decimals": 18
    },
    "WBTC": {
      "symbol": "WBTC",
      "address": "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f",
      "asset": ASSET_BTC,
      "decimals": 8
    },
    "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f": {
      "symbol": "WBTC",
      "address": "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f",
      "asset": ASSET_BTC,
      "decimals": 8
    },
    "sGLP": {
      "symbol": "sGLP",
      "address": "0x5402B5F40310bDED796c7D0F3FF6683f5C0cFfdf",
      "asset": ASSET_GLP,
      "decimals": 18
    },
    "0x5402B5F40310bDED796c7D0F3FF6683f5C0cFfdf": {
      "symbol": "sGLP",
      "address": "0x5402B5F40310bDED796c7D0F3FF6683f5C0cFfdf",
      "asset": ASSET_GLP,
      "decimals": 18
    },
    "ARB": {
      "symbol": "ARB",
      "address": "0x912CE59144191C1204E64559FE8253a0e49E6548",
      "asset": ASSET_ARB,
      "decimals": 18
    },
    "0x912CE59144191C1204E64559FE8253a0e49E6548": {
      "symbol": "ARB",
      "address": "0x912CE59144191C1204E64559FE8253a0e49E6548",
      "asset": ASSET_ARB,
      "decimals": 18
    },
    "wstETH": {
      "symbol": "wstETH",
      "address": "0x5979D7b546E38E414F7E9822514be443A4800529",
      "asset": ASSET_wstETH,
      "decimals": 18
    },
    "0x5979D7b546E38E414F7E9822514be443A4800529": {
      "symbol": "wstETH",
      "address": "0x5979D7b546E38E414F7E9822514be443A4800529",
      "asset": ASSET_wstETH,
      "decimals": 18
    },
    "USDC": {
      "symbol": "USDC",
      "address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
      "asset": ASSET_USDC,
      "decimals": 6
    },
    "0xaf88d065e77c8cC2239327C5EDb3A432268e5831": {
      "symbol": "USDC",
      "address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
      "asset": ASSET_USDC,
      "decimals": 6
    },
    "gmBTC": {
      "symbol": "gmBTC",
      "address": "0x47c031236e19d024b42f8AE6780E44A573170703",
      "asset": ASSET_gmBTC,
      "decimals": 18
    },
    "0x47c031236e19d024b42f8AE6780E44A573170703": {
      "symbol": "gmBTC",
      "address": "0x47c031236e19d024b42f8AE6780E44A573170703",
      "asset": ASSET_gmBTC,
      "decimals": 18
    },
    "gmETH": {
      "symbol": "gmETH",
      "address": "0x70d95587d40A2caf56bd97485aB3Eec10Bee6336",
      "asset": ASSET_gmETH,
      "decimals": 18
    },
    "0x70d95587d40A2caf56bd97485aB3Eec10Bee6336": {
      "symbol": "gmETH",
      "address": "0x70d95587d40A2caf56bd97485aB3Eec10Bee6336",
      "asset": ASSET_gmETH,
      "decimals": 18
    },
  }
}
