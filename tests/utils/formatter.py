from web3 import Web3


def format_bytes32(str):
  web3 = Web3()
  # Convert the value to bytes
  str_bytes = web3.to_bytes(hexstr=str)

  # Pad the bytes to 32 bytes length
  padded_bytes = str_bytes.rjust(32, b'\x00')

  # Convert the padded bytes to a hex string
  hex_string = web3.toHex(padded_bytes)

  return hex_string
