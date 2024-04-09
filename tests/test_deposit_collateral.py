from hmx2 import Client
from hmx2.constants.assets import (
  ASSET_USDC,
  ASSET_USDT,
  ASSET_DAI,
  ASSET_ETH,
  ASSET_BTC,
  ASSET_ARB
)
from hmx2.helpers.mapper import get_token_profile
from tests.constants import DEFAULT_PUBLIC_ADDRESS
from tests.constants import DEFAULT_KEY
from tests.constants import DEFAULT_CHAIN_ID
from tests.constants import DEFAULT_FORK_BLOCK
from tests.constants import UNISWAP_SWAP_ROUTER_02_ADDRESS
from tests.constants import TENDERY_API_BASE_URL
from tests.constants import TENDERY_ACCESS_TOKEN
from tests.constants import TENDERY_PROJECT_SLUG
from tests.helpers.pyth_price_service_helper import mock_pyth_price
from tests.helpers.action_helper import ActionHelper
from tests.helpers.tenderly_helper import TenderlyHelper
from urllib.parse import urljoin
import responses
import pytest


class TestDepositCollateral:
  @pytest.fixture(autouse=True)
  def setup_tenderly_helper(self):
    assert True
    # create new fork
    tenderly_helper = TenderlyHelper(
      TENDERY_API_BASE_URL, TENDERY_ACCESS_TOKEN, TENDERY_PROJECT_SLUG)
    tenderly_helper.create_fork(
      "test_deposit_collateral", DEFAULT_CHAIN_ID, "test deposit collateral", DEFAULT_FORK_BLOCK)
    # set balances
    tenderly_helper.set_balance(DEFAULT_PUBLIC_ADDRESS, 10_000)
    yield tenderly_helper
    assert True
    # delete fork
    tenderly_helper.delete_fork()

  def test_exception_when_bad_sub_account_id(self, setup_tenderly_helper: TenderlyHelper):
    client = Client(
      eth_private_key=DEFAULT_KEY,
      rpc_url=setup_tenderly_helper.rpc_url
    )
    asset_map = get_token_profile(DEFAULT_CHAIN_ID)
    with pytest.raises(Exception, match="Invalid sub account id"):
      client.private.deposit_erc20_collateral(-1,
                                              asset_map['USDC.e']['address'], 1000)
    with pytest.raises(Exception, match="Invalid sub account id"):
      client.private.deposit_erc20_collateral(
        256, asset_map['USDC.e']['address'], 1000)

  @responses.activate
  def test_correctness_when_deposit_eth_collateral(self, setup_tenderly_helper: TenderlyHelper):
    # mock pyth prices
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_USDC, 1)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_USDT, 1)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_DAI, 1)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_ETH, 1850)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_BTC, 29500)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_ARB, 1.15)
    responses.add_passthru(setup_tenderly_helper.rpc_url)

    client = Client(
      eth_private_key=DEFAULT_KEY,
      rpc_url=setup_tenderly_helper.rpc_url
    )
    client.private.deposit_eth_collateral(0, 10)
    my_collaterals = client.public.get_collaterals(
      client.private.get_public_address(), 0)
    assert my_collaterals["WETH"]["amount"] == 10
    assert my_collaterals["WETH"]["value_usd"] == 18500

  @responses.activate
  def test_correctness_when_deposit_weth_collateral_without_allowance(self, setup_tenderly_helper: TenderlyHelper):
    # mock pyth prices
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_USDC, 1)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_USDT, 1)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_DAI, 1)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_ETH, 1850)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_BTC, 29500)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_ARB, 1.15)
    # pass through requests to tenderly
    responses.add_passthru(setup_tenderly_helper.rpc_url)

    client = Client(
      eth_private_key=DEFAULT_KEY,
      rpc_url=setup_tenderly_helper.rpc_url
    )
    action_helper = ActionHelper(
      rpc_url=setup_tenderly_helper.rpc_url,
      eth_private_key=DEFAULT_KEY
    )
    asset_map = get_token_profile(DEFAULT_CHAIN_ID)
    action_helper.wrap_eth(10)
    client.private.deposit_erc20_collateral(0, asset_map['WETH']['address'], 10)
    my_collaterals = client.public.get_collaterals(
      client.private.get_public_address(), 0)
    assert my_collaterals["WETH"]["amount"] == 10
    assert my_collaterals["WETH"]["value_usd"] == 18500

  @responses.activate
  def test_correctness_when_deposit_erc20_collateral_without_allowance(self, setup_tenderly_helper: TenderlyHelper):
    # mock pyth prices
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_USDC, 1)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_USDT, 1)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_DAI, 1)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_ETH, 1850)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_BTC, 29500)
    mock_pyth_price(DEFAULT_CHAIN_ID, ASSET_ARB, 1.15)
    # pass through requests to tenderly
    responses.add_passthru(setup_tenderly_helper.rpc_url)

    client = Client(
      eth_private_key=DEFAULT_KEY,
      rpc_url=setup_tenderly_helper.rpc_url
    )
    action_helper = ActionHelper(
      rpc_url=setup_tenderly_helper.rpc_url,
      eth_private_key=DEFAULT_KEY
    )
    asset_map = get_token_profile(DEFAULT_CHAIN_ID)
    # buy USDC.e
    action_helper.wrap_eth(10)
    action_helper.approve(
      asset_map['WETH']['address'], UNISWAP_SWAP_ROUTER_02_ADDRESS, 10)
    action_helper.swapExactTokensForTokens(
      asset_map['WETH']['address'], asset_map['USDC.e']['address'], 500, 10)
    # deposit USDC.e as collateral
    client.private.deposit_erc20_collateral(
      0, asset_map['USDC.e']['address'], 1000)
    my_collaterals = client.public.get_collaterals(
      client.private.get_public_address(), 0)
    assert my_collaterals["USDC.e"]["amount"] == 1000
    assert my_collaterals["USDC.e"]["value_usd"] == 1000
