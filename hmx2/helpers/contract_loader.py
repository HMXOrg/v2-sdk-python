import json
import os
from web3 import Web3
from web3.contract import Contract


def load_contract(w3: Web3, address, abi_path) -> Contract:
  hmx2_folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..',
  )
  return w3.eth.contract(
    address=address,
    abi=json.load(open(os.path.join(hmx2_folder, abi_path), 'r')))
