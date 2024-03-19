import os
import asyncio
from hmx2.hmx_client import Client
from hmx2.constants.markets import MARKET_ETH_USD
from hmx2.constants.common import ADDRESS_ZERO
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
  create_market_order = client.private.create_market_order(
    0, MARKET_ETH_USD, Action.BUY, 100, False, ADDRESS_ZERO
  )
  print(f'Create market order tx: {create_market_order["tx"].hex()}\n')
  await asyncio.sleep(2)

  create_order = client.private.create_trigger_order(
    0, MARKET_ETH_USD, Action.BUY, 100, 1800, True, False)
  print(f'Create order tx: {create_order["tx"].hex()}\n')
  await asyncio.sleep(2)

  update_order = client.private.update_trigger_order(
    0, create_order["order"]["orderIndex"], Action.SELL, 50, 1700, True, False, ADDRESS_ZERO)
  print(f'Update order tx: {update_order["tx"].hex()}\n')
  await asyncio.sleep(2)

  cancel_order = client.private.cancel_trigger_order(
    0, update_order["order"]["orderIndex"])
  print(f'Cancle order tx: {cancel_order["tx"].hex()}\n')
  await asyncio.sleep(2)

if __name__ == '__main__':
  asyncio.run(main())
