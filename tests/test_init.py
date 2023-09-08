from hmx2 import Client
from tests.constants import DEFAULT_KEY
from tests.constants import DEFAULT_PUBLIC_ADDRESS
from tests.constants import DEFAULT_CHAIN_ID
from tests.constants import DEFAULT_FORK_BLOCK
from tests.constants import TENDERY_API_BASE_URL
from tests.constants import TENDERY_ACCESS_TOKEN
from tests.constants import TENDERY_PROJECT_SLUG
from tests.helpers.tenderly_helper import TenderlyHelper
import pytest


class TestInit:
  @pytest.fixture(autouse=True)
  def setup_tenderly_helper(self):
    assert True
    # create new fork
    tenderly_helper = TenderlyHelper(
      TENDERY_API_BASE_URL, TENDERY_ACCESS_TOKEN, TENDERY_PROJECT_SLUG)
    tenderly_helper.create_fork(
      "test_init", DEFAULT_CHAIN_ID, "test initialized", DEFAULT_FORK_BLOCK)
    # set balances
    tenderly_helper.set_balance(DEFAULT_PUBLIC_ADDRESS, 10_000)
    yield tenderly_helper
    assert True
    # delete fork
    tenderly_helper.delete_fork()

  def test_when_provided_all_required_params(self, setup_tenderly_helper: TenderlyHelper):
    client = Client(
        eth_private_key=DEFAULT_KEY,
        rpc_url=setup_tenderly_helper.rpc_url,
    )
    assert client.private.get_public_address() == DEFAULT_PUBLIC_ADDRESS
