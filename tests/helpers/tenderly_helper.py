import requests
from urllib.parse import urljoin


class TenderlyHelper(object):
  def __init__(self, tenderly_api_base_url: str, access_token: str, project_slug: str):
    self.tenderly_api_base_url = tenderly_api_base_url
    self.access_token = access_token
    self.project_slug = project_slug

    self.fork_id = None
    self.rpc_url = None

  def create_fork(self, name: str, network_id: int, description: str, block_number: int):
    headers = {
      'X-Access-Key': self.access_token,
    }
    new_fork_payload = {
      "name": name,
      "networkId": str(network_id),
      "description": description,
      "blockNumber": str(block_number)
    }
    resp = requests.post(urljoin(self.tenderly_api_base_url, "/api/v2/project/{}/forks".format(self.project_slug)), headers=headers,
                         json=new_fork_payload)
    if resp.status_code != 200:
      raise Exception(resp.json())
    resp_json = resp.json()
    self.rpc_url = resp_json['fork']['json_rpc_url']
    self.fork_id = resp_json['fork']['id']
    return resp.json()

  def delete_fork(self):
    headers = {
      'X-Access-Key': self.access_token,
    }
    resp = requests.delete(urljoin(self.tenderly_api_base_url,
                           "/api/v2/project/{}/forks/{}".format(self.project_slug, self.fork_id)), headers=headers)
    if resp.status_code != 200:
      raise Exception(resp.json())
    self.rpc_url = None
    self.fork_id = None
    return resp.json()

  def set_balance(self, account: str, balance: float):
    balance_wei = int(balance * 10 ** 18)
    headers = {
      'Accept': '*/*',
      'Accept-Encoding': 'gzip, deflate',
      'Connection': 'keep-alive',
      'Content-Type': 'application/json',
      'User-Agent': 'python-requests/2.22.0'
    }
    set_balance_payload = {
      "jsonrpc": "2.0",
      "method": "tenderly_setBalance",
      "params": [[account], hex(balance_wei)],
      "id": 1
    }
    resp = requests.post(self.rpc_url, headers=headers,
                         json=set_balance_payload)
    if resp.status_code != 200:
      raise Exception(resp.json())
    return resp.json()
