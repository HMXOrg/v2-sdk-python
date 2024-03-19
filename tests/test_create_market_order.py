from tests.helpers.tenderly_helper import TenderlyHelper
from tests.helpers.action_helper import ActionHelper
from tests.helpers.pyth_price_service_helper import mock_pyth_price
from tests.helpers.order_execution_helper import OrderExecutionHelper
from tests.constants import TENDERY_API_BASE_URL
from tests.constants import TENDERY_ACCESS_TOKEN
from tests.constants import TENDERY_PROJECT_SLUG
from tests.constants import DEFAULT_CHAIN_ID
from tests.constants import DEFAULT_FORK_BLOCK
from tests.constants import DEFAULT_PUBLIC_ADDRESS
from tests.constants import DEFAULT_KEY
from tests.constants import UNISWAP_SWAP_ROUTER_02_ADDRESS
from hmx2.constants.assets import (
  ASSET_USDC,
  ASSET_USDT,
  ASSET_DAI,
  ASSET_ETH,
  ASSET_BTC,
  ASSET_ARB
)
from hmx2.constants.markets import MARKET_ETH_USD
from hmx2.helpers.mapper import get_token_profile
from hmx2.hmx_client import Client
import responses
import pytest


class TestCreateMarketOrder:
  @pytest.fixture(autouse=True)
  def setup_tenderly_helper(self):
    assert True
    # create new fork
    tenderly_helper = TenderlyHelper(
      TENDERY_API_BASE_URL, TENDERY_ACCESS_TOKEN, TENDERY_PROJECT_SLUG)
    tenderly_helper.create_fork(
      "test_create_market_order", DEFAULT_CHAIN_ID, "test create market order", DEFAULT_FORK_BLOCK)
    # set balances
    tenderly_helper.set_balance(DEFAULT_PUBLIC_ADDRESS, 10_000)
    yield tenderly_helper
    assert True
    # delete fork
    tenderly_helper.delete_fork()

  def test_when_create_long_market_order(self, setup_tenderly_helper):
    client = Client(
      eth_private_key=DEFAULT_KEY,
      rpc_url=setup_tenderly_helper.rpc_url
    )
    asset_map = get_token_profile(DEFAULT_CHAIN_ID)
    # mock pyth prices
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_USDC, 1)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_USDT, 1)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_DAI, 1)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_ETH, 1850)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_BTC, 29500)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_ARB, 1.15)
    # pass through requests to tenderly
    responses.add_passthru(setup_tenderly_helper.rpc_url)

    # initialized objects
    client = Client(
      eth_private_key=DEFAULT_KEY,
      rpc_url=setup_tenderly_helper.rpc_url
    )
    action_helper = ActionHelper(
      rpc_url=setup_tenderly_helper.rpc_url,
      eth_private_key=DEFAULT_KEY
    )
    order_execution_helper = OrderExecutionHelper(
      rpc_url=setup_tenderly_helper.rpc_url)
    # buy USDC.e
    action_helper.wrap_eth(10)
    action_helper.approve(
      asset_map['WETH']['address'], UNISWAP_SWAP_ROUTER_02_ADDRESS, 10)
    action_helper.swapExactTokensForTokens(
      asset_map['WETH']['address'], asset_map['USDC.e']['address'], 500, 10)
    # deposit USDC.e as collateral
    client.private.deposit_erc20_collateral(
      0, asset_map['USDC.e']['address'], 1000)
    # create long market order
    client.private.create_market_order(0, MARKET_ETH_USD, True, 1000, False)
    # execute the order
    order_execution_helper.execute_orders(
      [DEFAULT_PUBLIC_ADDRESS], [0], [0], True)
