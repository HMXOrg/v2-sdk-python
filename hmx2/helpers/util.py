
from web3 import Web3


# Convert asset_name to hex (0x77~)
def convert_asset_to_byte32(asset_name):
  return Web3.to_hex(text=asset_name).ljust(66, '0')


def get_sub_account(account: str, sub_account_id: int):
  '''Get address of sub_account

    Args:
      account: account address
      sub_account_id: sub account number

    Returns:
      sub_account address
  '''
  return Web3.to_checksum_address(hex(int(account, 16) ^ sub_account_id))
