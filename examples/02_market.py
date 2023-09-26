import os
import asyncio
from hmx2.hmx_client import Client
from hmx2.constants import MARKET_ETH_USD, MARKET_BTC_USD, HOURS, DAYS
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")


async def main():
  client = Client(
     eth_private_key=PRIVATE_KEY,
     rpc_url=RPC_URL
   )

  # ETH
  eth_market_info = client.public.get_market_info(MARKET_ETH_USD)
  print('Market {0}'.format(eth_market_info["market"]))
  print('Price: {0:.4f}'.format(eth_market_info["price"]))
  print('Long: {0:.2f}'.format((eth_market_info["long_size"])))
  print('Short: {0:.2f}'.format((eth_market_info["short_size"])))
  print('Funding rate 1H: {0:.6f}%'.format(
    (eth_market_info["funding_rate"]["1H"])))
  print('Funding rate 8H: {0:.6f}%'.format(
    (eth_market_info["funding_rate"]["8H"])))
  print('Funding rate 24H: {0:.6f}%'.format(
    (eth_market_info["funding_rate"]["24H"])))
  print('Funding rate 1Y: {0:.6f}%'.format(
    (eth_market_info["funding_rate"]["1Y"])))
  print('Borrowing rate 1H: {0:.6f}%'.format(
    (eth_market_info["borrowing_rate"]["1H"])))
  print('Borrowing rate 8H: {0:.6f}%'.format(
    (eth_market_info["borrowing_rate"]["8H"])))
  print('Borrowing rate 24H: {0:.6f}%'.format(
    (eth_market_info["borrowing_rate"]["24H"])))
  print('Borrowing rate 1Y: {0:.6f}%'.format(
    (eth_market_info["borrowing_rate"]["1Y"])))

  # BTC
  btc_market_info = client.public.get_market_info(MARKET_BTC_USD)
  print('Market {0}'.format(btc_market_info["market"]))
  print('Price: {0:.4f}'.format(btc_market_info["price"]))
  print('Long: {0:.2f}'.format((btc_market_info["long_size"])))
  print('Short: {0:.2f}'.format((btc_market_info["short_size"])))
  print('Funding rate 1H: {0:.6f}%'.format(
    (btc_market_info["funding_rate"]["1H"])))
  print('Funding rate 8H: {0:.6f}%'.format(
    (btc_market_info["funding_rate"]["8H"])))
  print('Funding rate 24H: {0:.6f}%'.format(
    (btc_market_info["funding_rate"]["24H"])))
  print('Funding rate 1Y: {0:.6f}%'.format(
    (btc_market_info["funding_rate"]["1Y"])))
  print('Borrowing rate 1H: {0:.6f}%'.format(
    (btc_market_info["borrowing_rate"]["1H"])))
  print('Borrowing rate 8H: {0:.6f}%'.format(
    (btc_market_info["borrowing_rate"]["8H"])))
  print('Borrowing rate 24H: {0:.6f}%'.format(
    (btc_market_info["borrowing_rate"]["24H"])))
  print('Borrowing rate 1Y: {0:.6f}%'.format(
    (btc_market_info["borrowing_rate"]["1Y"])))

if __name__ == '__main__':
  asyncio.run(main())
