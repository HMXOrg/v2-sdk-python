import responses
from hmx2.constants.pricefeed import (
  PRICE_FEED_IDS,
  DEFAULT_PYTH_PRICE_SERVICE_URL,
  GET_LATEST_PRICE_FEEDS_ENDPOINT
)
from urllib.parse import urljoin


def mock_pyth_price(chain_id, asset_id, price):
  responses.add(responses.GET, "{}?ids[]={}".format(urljoin(DEFAULT_PYTH_PRICE_SERVICE_URL,
                                                            GET_LATEST_PRICE_FEEDS_ENDPOINT), PRICE_FEED_IDS[chain_id][asset_id]),
                json=[{'price': {'price': price * 10 ** 8, 'expo': -8}}], status=200)
