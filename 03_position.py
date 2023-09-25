import os
import asyncio
from hmx2.hmx_client import Client
from hmx2.constants import MARKET_ETH_USD, MARKET_BTC_USD, HOURS, DAYS, MARKET_XAU_USD
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")


async def main():
  client = Client(
     eth_private_key=PRIVATE_KEY,
     rpc_url=RPC_URL
   )

  position = client.private.get_position_info(
    "0x6629eC35c8Aa279BA45Dbfb575c728d3812aE31a", 1, MARKET_XAU_USD)
  print(
    f'Position: {position["primary_account"]}-{position["sub_account_id"]}-{position["market_index"]}')
  print('Size: {0:.4f}'.format(position["position_size_e30"] / 10 ** 30))
  print('Entry price: {0:.6f}'.format(
    position["avg_entry_priceE30"] / 10 ** 30))
  print('Pnl: {0:.4f}'.format(position["pnl"] / 10 ** 30))

if __name__ == '__main__':
  asyncio.run(main())
