import responses
from hmx2.constants.pricefeed import DEFAULT_PYTH_PRICE_SERVICE_URL
from hmx2.modules.oracle.pyth_oracle.constants import GET_LATEST_PRICE_FEEDS_ENDPOINT
from hmx2.modules.oracle.pyth_oracle.constants import PRICE_FEED_IDS
from urllib.parse import urljoin


def mock_pyth_price(chain_id, asset_id, price):
  responses.add(responses.GET, "{}?ids[]={}".format(urljoin(DEFAULT_PYTH_PRICE_SERVICE_URL,
                                                            GET_LATEST_PRICE_FEEDS_ENDPOINT), PRICE_FEED_IDS[chain_id][asset_id]),
                json=[{'price': {'price': price * 10 ** 8, 'expo': -8}}], status=200)
