
import math
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
  check_sub_account_id_param(sub_account_id)
  return Web3.to_checksum_address(hex(int(account, 16) ^ sub_account_id))


def check_sub_account_id_param(sub_account_id: int):
  if sub_account_id not in range(0, 256):
    raise Exception("Invalid sub account id")


def from_number_to_e30(n: float | int) -> int:
  return math.floor(n * 10 ** 8) * 10 ** 22


def from_e30_to_e8(n: float | int) -> int:
  return math.floor(n / 10 ** 22)


def is_blast_chain(chain_id: int) -> bool:
  return chain_id == 81457 or chain_id == 168587773
