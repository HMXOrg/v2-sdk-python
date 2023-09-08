import json
import os


def load_contract(w3, address, abi_path):
  hmx2_folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..',
  )
  return w3.eth.contract(
    address=address,
    abi=json.load(open(os.path.join(hmx2_folder, abi_path), 'r')))
