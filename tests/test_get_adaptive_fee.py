from tests.helpers.tenderly_helper import TenderlyHelper
from tests.constants import TENDERY_API_BASE_URL
from tests.constants import TENDERY_ACCESS_TOKEN
from tests.constants import TENDERY_PROJECT_SLUG
from tests.constants import DEFAULT_CHAIN_ID
from tests.constants import DEFAULT_FORK_BLOCK
from tests.constants import DEFAULT_PUBLIC_ADDRESS
from tests.constants import DEFAULT_KEY
from hmx2.constants.markets import MARKET_SOL_USD
from hmx2.hmx_client import Client
import pytest


class TestCreateMarketOrder:
  @pytest.fixture(autouse=True)
  def setup_tenderly_helper(self):
    assert True
    # create new fork
    tenderly_helper = TenderlyHelper(
      TENDERY_API_BASE_URL, TENDERY_ACCESS_TOKEN, TENDERY_PROJECT_SLUG)
    tenderly_helper.create_fork(
      "test_get_adaptive_fee", DEFAULT_CHAIN_ID, "test get adaptive fee", DEFAULT_FORK_BLOCK)
    # set balances
    tenderly_helper.set_balance(DEFAULT_PUBLIC_ADDRESS, 10_000)
    yield tenderly_helper
    assert True
    # delete fork
    tenderly_helper.delete_fork()

  def test_get_adaptive_fee(self, setup_tenderly_helper):
    client = Client(
      eth_private_key=DEFAULT_KEY,
      rpc_url=setup_tenderly_helper.rpc_url,
    )
    fee = client.public.get_adaptive_fee(
      100000 * (10**30), MARKET_SOL_USD, True)
    assert True
