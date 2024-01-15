import os
import asyncio
from hmx2.hmx_client import Client
from hmx2.constants import MARKET_DIX_USD
from hmx2.enum import Action
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")


async def main():
  client = Client(
     eth_private_key=PRIVATE_KEY,
     rpc_url=RPC_URL
   )

  eth_price = client.public.get_price(MARKET_DIX_USD)
  print('Case: Query raw price ')
  print('Market {0}'.format(eth_price["market"]))
  print('Price: {0:.4f}'.format(eth_price["price"]))

  eth_price = client.public.get_price(MARKET_DIX_USD, Action.SELL, 1000)
  print('Case: Including adaptive price ')
  print('Market {0}'.format(eth_price["market"]))
  print('Price: {0:.4f}'.format(eth_price["price"]))
  print('Adaptive price {0:.4f}'.format(eth_price["adaptive_price"]))
  print('Price impact {0:.4f}%'.format(eth_price["price_impact"]))


if __name__ == '__main__':
  asyncio.run(main())
