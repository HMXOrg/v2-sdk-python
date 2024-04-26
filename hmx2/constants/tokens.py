from hmx2.constants.assets import (
  ASSET_ARB,
  ASSET_BTC,
  ASSET_DAI,
  ASSET_ETH,
  ASSET_GLP,
  ASSET_USDC,
  ASSET_USDCe,
  ASSET_USDT,
  ASSET_gmBTC,
  ASSET_gmETH,
  ASSET_wstETH,
  ASSET_PYTH,
  ASSET_ybUSDB,
  ASSET_ybETH,
  ASSET_USDB
)

# Arbitrum Sepolia
# COLLATERAL_USDCe = "0xB853c09b6d03098b841300daD57701ABcFA80228"

# Arbitrum One
COLLATERAL_USDCe = "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8"
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
COLLATERAL_PYTH = "0xE4D5c6aE46ADFAF04313081e8C0052A30b6Dd724"

# Blast Sepolia
# BLAST_COLLATERAL_USDB = "0x4200000000000000000000000000000000000022"
# BLAST_COLLATERAL_ETH = "0x4200000000000000000000000000000000000023"

# Blast Mainnet
BLAST_COLLATERAL_ETH = "0x4300000000000000000000000000000000000004"
BLAST_COLLATERAL_USDB = "0x4300000000000000000000000000000000000003"

CHAIN_COLLATERAL = {
  42161: [
      COLLATERAL_USDCe,
      COLLATERAL_USDT,
      COLLATERAL_DAI,
      COLLATERAL_WETH,
      COLLATERAL_WBTC,
      COLLATERAL_sGLP,
      COLLATERAL_ARB,
      COLLATERAL_wstETH,
      COLLATERAL_USDC,
      COLLATERAL_gmBTC,
      COLLATERAL_gmETH,
      COLLATERAL_PYTH,
  ],
  81457: [
      BLAST_COLLATERAL_ETH,
      BLAST_COLLATERAL_USDB,
  ]}

# ------ Token Profiles ------
TOKEN_PROFILE = {
  # Arbitrum One
  42161: {
    "USDC.e": {
      "symbol": "USDC.e",
      "address": "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
      "asset": ASSET_USDCe,
      "decimals": 6
    },
      "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8": {
        "symbol": "USDC.e",
        "address": "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
        "asset": ASSET_USDCe,
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
      "PYTH": {
        "symbol": "PYTH",
        "address": "0xE4D5c6aE46ADFAF04313081e8C0052A30b6Dd724",
        "asset": ASSET_PYTH,
        "decimals": 18
    },
      "0xE4D5c6aE46ADFAF04313081e8C0052A30b6Dd724": {
        "symbol": "PYTH",
        "address": "0xE4D5c6aE46ADFAF04313081e8C0052A30b6Dd724",
        "asset": ASSET_PYTH,
        "decimals": 18
    },
  },
  # Arbitrum Sepolia
  421614: {
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
          "address": "0x20E58fC5E1ee3C596fb3ebD6de6040e7800e82E6",
          "asset": ASSET_USDT,
          "decimals": 6
      },
      "0x20E58fC5E1ee3C596fb3ebD6de6040e7800e82E6": {
          "symbol": "USDT",
          "address": "0x20E58fC5E1ee3C596fb3ebD6de6040e7800e82E6",
          "asset": ASSET_USDT,
          "decimals": 6
      },
      "DAI": {
          "symbol": "DAI",
          "address": "0x8D715a015aC0e064a3Cfb88DA755d346Aee65433",
          "asset": ASSET_DAI,
          "decimals": 18
      },
      "0x8D715a015aC0e064a3Cfb88DA755d346Aee65433": {
          "symbol": "DAI",
          "address": "0x8D715a015aC0e064a3Cfb88DA755d346Aee65433",
          "asset": ASSET_DAI,
          "decimals": 18
      },
      "WETH": {
          "symbol": "WETH",
          "address": "0xc88322Ec9526A7A98B7F58ff773b3B003C91ce71",
          "asset": ASSET_ETH,
          "decimals": 18
      },
      "0xc88322Ec9526A7A98B7F58ff773b3B003C91ce71": {
          "symbol": "WETH",
          "address": "0xc88322Ec9526A7A98B7F58ff773b3B003C91ce71",
          "asset": ASSET_ETH,
          "decimals": 18
      },
      "WBTC": {
          "symbol": "WBTC",
          "address": "0x4c08D11Bc95075AD992Bd7A5776D0D9813E264d5",
          "asset": ASSET_BTC,
          "decimals": 8
      },
      "0x4c08D11Bc95075AD992Bd7A5776D0D9813E264d5": {
          "symbol": "WBTC",
          "address": "0x4c08D11Bc95075AD992Bd7A5776D0D9813E264d5",
          "asset": ASSET_BTC,
          "decimals": 8
      },
      "sGLP": {
          "symbol": "sGLP",
          "address": "0x7AAF085e43f059105F7e1ECc525E8142fF962159",
          "asset": ASSET_GLP,
          "decimals": 18
      },
      "0x7AAF085e43f059105F7e1ECc525E8142fF962159": {
          "symbol": "sGLP",
          "address": "0x7AAF085e43f059105F7e1ECc525E8142fF962159",
          "asset": ASSET_GLP,
          "decimals": 18
      },
      "ARB": {
          "symbol": "ARB",
          "address": "0x4Dc3c929DDa7451012F408d1f376221621dD2a56",
          "asset": ASSET_ARB,
          "decimals": 18
      },
      "0x4Dc3c929DDa7451012F408d1f376221621dD2a56": {
          "symbol": "ARB",
          "address": "0x4Dc3c929DDa7451012F408d1f376221621dD2a56",
          "asset": ASSET_ARB,
          "decimals": 18
      },
      "wstETH": {
          "symbol": "wstETH",
          "address": "0xFc41505F4e24345E3797b6730a948a2B03a5eC5e",
          "asset": ASSET_wstETH,
          "decimals": 18
      },
      "0xFc41505F4e24345E3797b6730a948a2B03a5eC5e": {
          "symbol": "wstETH",
          "address": "0xFc41505F4e24345E3797b6730a948a2B03a5eC5e",
          "asset": ASSET_wstETH,
          "decimals": 18
      },
      "USDC": {
          "symbol": "USDC",
          "address": "0xEB27B05178515c7E6E51dEE159c8487A011ac030",
          "asset": ASSET_USDC,
          "decimals": 6
      },
      "0xEB27B05178515c7E6E51dEE159c8487A011ac030": {
          "symbol": "USDC",
          "address": "0xEB27B05178515c7E6E51dEE159c8487A011ac030",
          "asset": ASSET_USDC,
          "decimals": 6
      },
      "gmBTC": {
          "symbol": "gmBTC",
          "address": "0xC4605B61675654396f3b77F9D4c3bE661fa0d873",
          "asset": ASSET_gmBTC,
          "decimals": 18
      },
      "0xC4605B61675654396f3b77F9D4c3bE661fa0d873": {
          "symbol": "gmBTC",
          "address": "0xC4605B61675654396f3b77F9D4c3bE661fa0d873",
          "asset": ASSET_gmBTC,
          "decimals": 18
      },
      "gmETH": {
          "symbol": "gmETH",
          "address": "0x417B34E90990657BF6adC1Ecc2ac4B36069cc927",
          "asset": ASSET_gmETH,
          "decimals": 18
      },
      "0x417B34E90990657BF6adC1Ecc2ac4B36069cc927": {
          "symbol": "gmETH",
          "address": "0x417B34E90990657BF6adC1Ecc2ac4B36069cc927",
          "asset": ASSET_gmETH,
          "decimals": 18
      },
  },
  81457: {
      "ybUSDB": {
          "symbol": "USDB",
          "address": "0xCD732d21c1B23A3f84Bb386E9759b5b6A1BcBe39",
          "asset": ASSET_ybUSDB,
          "decimals": 18
      },
      "0xCD732d21c1B23A3f84Bb386E9759b5b6A1BcBe39": {
          "symbol": "USDB",
          "address": "0xCD732d21c1B23A3f84Bb386E9759b5b6A1BcBe39",
          "asset": ASSET_ybUSDB,
          "decimals": 18
      },
      "ybETH": {
          "symbol": "ETH",
          "address": "0xb9d94A3490bA2482E2D4F21F0E76b92E5661Ded8",
          "asset": ASSET_ybETH,
          "decimals": 18
      },
      "0xb9d94A3490bA2482E2D4F21F0E76b92E5661Ded8": {
          "symbol": "ETH",
          "address": "0xb9d94A3490bA2482E2D4F21F0E76b92E5661Ded8",
          "asset": ASSET_ybETH,
          "decimals": 18
      },
      "USDB": {
          "symbol": "USDB",
          "address": "0x4300000000000000000000000000000000000003",
          "asset": ASSET_USDB,
          "decimals": 18,
      },
      "0x4300000000000000000000000000000000000003": {
          "symbol": "USDB",
          "address": "0x4300000000000000000000000000000000000003",
          "asset": ASSET_USDB,
          "decimals": 18,
      },
      "WETH": {
          "symbol": "WETH",
          "address": "0x4300000000000000000000000000000000000004",
          "asset": ASSET_ETH,
          "decimals": 18
      },
      "0x4300000000000000000000000000000000000004": {
          "symbol": "WETH",
          "address": "0x4300000000000000000000000000000000000004",
          "asset": ASSET_ETH,
          "decimals": 18
      },
  },
  168587773: {
      "ybUSDB": {
          "symbol": "USDB",
          "address": "0x073315910A2B432F2f9482bCEAFe34420718c7Cc",
          "asset": ASSET_ybUSDB,
          "decimals": 18
      },
      "0x073315910A2B432F2f9482bCEAFe34420718c7Cc": {
          "symbol": "USDB",
          "address": "0x073315910A2B432F2f9482bCEAFe34420718c7Cc",
          "asset": ASSET_ybUSDB,
          "decimals": 18
      },
      "ybETH": {
          "symbol": "ETH",
          "address": "0x628eF5ADFf7da4980CeA33E05568d22772E87EB8",
          "asset": ASSET_ybETH,
          "decimals": 18
      },
      "0x628eF5ADFf7da4980CeA33E05568d22772E87EB8": {
          "symbol": "ETH",
          "address": "0x628eF5ADFf7da4980CeA33E05568d22772E87EB8",
          "asset": ASSET_ybETH,
          "decimals": 18
      },
      "USDB": {
          "symbol": "USDB",
          "address": "0x4200000000000000000000000000000000000022",
          "asset": ASSET_USDB,
          "decimals": 18,
      },
      "0x4200000000000000000000000000000000000022": {
          "symbol": "USDB",
          "address": "0x4200000000000000000000000000000000000022",
          "asset": ASSET_USDB,
          "decimals": 18,
      },
      "WETH": {
          "symbol": "WETH",
          "address": "0x4200000000000000000000000000000000000023",
          "asset": ASSET_ETH,
          "decimals": 18,
      },
      "0x4200000000000000000000000000000000000023": {
          "symbol": "WETH",
          "address": "0x4200000000000000000000000000000000000023",
          "asset": ASSET_ETH,
          "decimals": 18,
      },
  }
}
