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
  eth_market_info = client.private.get_market_info(MARKET_ETH_USD)
  print('MARKET ETHUSD')
  print('Long: {0:.2f}'.format(
    (eth_market_info["market"]["long_position_size"] / 1e30)))
  print('Short: {0:.2f}'.format(
    (eth_market_info["market"]["short_position_size"] / 1e30)))
  print('Funding fee per hour: {0:.6f}%'.format(
    (eth_market_info["funding_rate"] * HOURS / DAYS * 100 / 1e18)))
  print('Borrowing fee per hour: {0:.6f}%'.format(
    (eth_market_info["borrowing_rate"] * HOURS / 1e18)))

  # BTC
  btc_market_info = client.private.get_market_info(MARKET_BTC_USD)
  print('MARKET BTCUSD')
  print('Long: {0:.2f}'.format(
    (btc_market_info["market"]["long_position_size"] / 1e30)))
  print('Short: {0:.2f}'.format(
    (btc_market_info["market"]["short_position_size"] / 1e30)))
  print('Funding fee per hour: {0:.6f}%'.format(
    (btc_market_info["funding_rate"] * HOURS / DAYS * 100 / 1e18)))
  print('Borrowing fee per hour: {0:.6f}%'.format(
    (btc_market_info["borrowing_rate"] * HOURS / 1e18)))

if __name__ == '__main__':
  asyncio.run(main())
