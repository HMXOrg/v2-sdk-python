import requests


class AnvilHelper(object):
  def __init__(self, rpc_url, fork_rpc_url, fork_block_number):
    self.rpc_url = rpc_url
    self.fork_rpc_url = fork_rpc_url
    self.fork_block_number = fork_block_number

  def reset_state(self):
    headers = {
      'Accept': '*/*',
      'Accept-Encoding': 'gzip, deflate',
      'Connection': 'keep-alive',
      'Content-Type': 'application/json',
      'User-Agent': 'python-requests/2.22.0'
    }
    anvil_reset_payload = {
      "jsonrpc": "2.0",
      "method": "anvil_reset",
      "params": [{"forking": {"jsonRpcUrl": self.fork_rpc_url, "blockNumber": self.fork_block_number}}],
      "id": 1
    }
    resp = requests.post(self.rpc_url, headers=headers,
                         json=anvil_reset_payload)
    if resp.status_code != 200:
      raise Exception(resp.json())
    return resp.json()
