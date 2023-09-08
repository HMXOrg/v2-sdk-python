import os
import asyncio
from hmx2.hmx_client import Client
from hmx2.constants import MARKET_ETH_USD
from hmx2.constants import COLLATERAL_USDCe
from hmx2.enum import Action
from web3 import Web3, Account
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
    0, MARKET_ETH_USD, Action.BUY, 100, False, "0x0000000000000000000000000000000000000000"
  )
  print(f'Create market order tx: {create_market_order.hex()}\n')

  create_order = client.private.create_trigger_order(
    0, MARKET_ETH_USD, Action.BUY, 100, 1800, True, False)
  print(f'Create order tx: {create_order.hex()}\n')

  update_order = client.private.update_trigger_order(
    0, 128, Action.SELL, 50, 1700, True, False, "0x0000000000000000000000000000000000000000")
  print(f'Update order tx: {update_order.hex()}\n')

  cancel_order = client.private.cancel_trigger_order(0, 127)
  print(f'Cancle order tx: {cancel_order.hex()}\n')

if __name__ == '__main__':
  asyncio.run(main())
