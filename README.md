# Python SDK for HMXv2

This library is tested against Python versions 2.7, 3.4, 3.5, 3.9, and 3.11.

## Installation

This package is available on PyPI. To install run the command below:

```
$ pip install hmx-v2-python
```

## Getting Started

The `Client` object contains two major attributes: Public and Private. As the names suggest, Public is for public functions that don't require an Ethereum private key, and Private is for functions specifically for the given key. For more comprehensive examples, please refer to the [examples](https://github.com/HMXOrg/v2-sdk-python/tree/main/examples) directory as well as the [tests](https://github.com/HMXOrg/v2-sdk-python/tree/main/tests).

### Public functions

```python
from hmx2.hmx_client import Client
from hmx2.constants.markets import MARKET_ETH_USD
from hmx2.enum import Action

#
# Using publicly access functions
#
hmx_client = Client(
    rpc_url=RPC_URL
)
# Get oracle price, adaptive price, and price impact of a new position
hmx_client.public.get_price(MARKET_ETH_USD, Action.SELL, 1000)
# Get market information
hmx_client.public.get_market_info(MARKET_ETH_USD)
# Get sub account in address format
hmx_client.public.get_sub_account(1)
# Get position ID
hmx_client.public.get_position_id(some_account, some_sub_account_id, MARKET_ETH_USD)
# Get position info
hmx_client.public.get_position_info(some_account, some_sub_account_id, MARKET_ETH_USD)
```

### Private function

```python
from hmx2.hmx_client import Client
from hmx2.constants.markets import MARKET_ETH_USD
from hmx2.constants.tokens import COLLATERAL_USDCe
from hmx2.enum import Action

#
# Initailized client with private key
#
hmx_client = Client(
    eth_private_key=PRIVATE_KEY,
    rpc_url=RPC_URL
)
# Get public address of the ethereum key
hmx_client.private.get_public_address()
# Deposit ETH as collateral
hmx_client.private.deposit_eth_collateral(sub_account_id=0, amount=10.123)
# Deposit ERC20 as collateral. This function will automatically
# approve CrossMarginHandler if needed.
hmx_client.private.deposit_erc20_collateral(sub_account_id=0, token_address=COLLATERAL_USDCe, amount=100.10)
# Create a market order
create_market_order = hmx_client.private.create_market_order(
  sub_account_id=0, market_index=MARKET_ETH_USD, buy=Action.BUY, size=100, reduce_only=False
)
print(create_market_order)
# Create a trigger order
# trigger_above_threshold = The current price must go above (if True) or below (if False)
# the trigger price in order for the order to be executed
create_order = hmx_client.private.create_trigger_order(
  sub_account_id=0,
  market_index=MARKET_ETH_USD,
  buy=Action.BUY,
  size=100,
  trigger_price=1800,
  trigger_above_threshold=True,
  reduce_only=False)
print(create_order)
# Update the order
update_order = hmx_client.private.update_trigger_order(
  0, create_order["order"]["orderIndex"], Action.SELL, 50, 1700, True, False)
print(update_order)
# Cancel the order
cancel_order = hmx_client.private.cancel_trigger_order(
  0, update_order["order"]["orderIndex"])
```

## Running Tests

To run tests, you will need have to clone the repo, update .env, and run:

```
$ make test
```

Please note that to run tests, Tenderly account is required.

## License

The primary license for HMXOrg/v2-sdk-python is the MIT License, see [here](https://github.com/HMXOrg/v2-sdk-python/blob/main/LICENSE).
