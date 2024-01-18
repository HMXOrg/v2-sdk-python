
from web3 import Web3


# Convert asset_name to hex (0x77~)
def convert_asset_to_byte32(asset_name):
    return Web3.to_hex(text=asset_name).ljust(66, '0')