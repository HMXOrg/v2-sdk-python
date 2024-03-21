import os
import asyncio
from hmx2.hmx_client import Client
from hmx2.constants.tokens import COLLATERAL_USDCe, COLLATERAL_WETH
from dotenv import load_dotenv
from time import sleep

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")


async def main():
  client = Client(
     eth_private_key=PRIVATE_KEY,
     rpc_url=RPC_URL,
   )
  # Deposit ETH as collateral
  client.private.deposit_eth_collateral(sub_account_id=0, amount=0.1)
  sleep(5)

  # Deposit ERC20 as collateral. This function will automatically
  # approve CrossMarginHandler if needed.
  client.private.deposit_erc20_collateral(
    sub_account_id=0, token_address=COLLATERAL_USDCe, amount=100.10)

  sleep(5)

  # Withdraw ETH as collateral
  # Can wrap if wanted
  client.private.withdraw_collateral(
    sub_account_id=0, token_address=COLLATERAL_WETH, amount=0.1, wrap=False)

  sleep(5)

  # Withdraw ERC20 as collateral. This function will automatically
  client.private.withdraw_collateral(
    sub_account_id=0, token_address=COLLATERAL_USDCe, amount=100.10)

if __name__ == '__main__':
  asyncio.run(main())
