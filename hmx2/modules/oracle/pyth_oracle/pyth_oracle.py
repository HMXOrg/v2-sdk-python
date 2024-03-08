from typing import List
from hmx2.constants.pricefeed import (
  PRICE_FEED_IDS,
  GET_LATEST_PRICE_FEEDS_ENDPOINT
)
import requests
from urllib.parse import urljoin


class PythOracle(object):
  def __init__(self, chain_id: int, price_service_endpoint: str):
    self.price_feed_ids = PRICE_FEED_IDS[chain_id]
    self.price_service_endpoint = price_service_endpoint

  def get_price(self, asset_id: str):
    params = {
      'ids[]': self.price_feed_ids[asset_id]
    }
    try:
      response = requests.get(
        urljoin(self.price_service_endpoint, GET_LATEST_PRICE_FEEDS_ENDPOINT), params)
      price_data = response.json()[0]['price']
      return float(price_data['price']) * 10 ** price_data['expo']
    except Exception as e:
      return None

  def get_multiple_price(self, asset_ids: List[str]):
    params = {
      'ids[]': list(map(lambda asset_id: self.price_feed_ids[asset_id], asset_ids))
    }
    try:
      response = requests.get(
        urljoin(self.price_service_endpoint, GET_LATEST_PRICE_FEEDS_ENDPOINT), params)
      price_datas = response.json()
      return_data = list(map(lambda price_data: float(
        price_data['price']['price']) * 10 ** price_data['price']['expo'], list(price_datas)))
      return return_data
    except Exception as e:
      return None
