from hmx2.constants.tokens import TOKEN_PROFILE
from hmx2.constants.contracts import CONTRACT_ADDRESS


def get_collateral_address_asset_map(chain_id: int):
  return {key: value["asset"] for key, value in TOKEN_PROFILE[chain_id].items()}


def get_collateral_address_list(chain_id: int):
  return list(set(val["address"] for val in TOKEN_PROFILE[chain_id].values()))


def get_token_profile(chain_id: int):
  return TOKEN_PROFILE[chain_id]


def get_contract_address(chain_id: int):
  return CONTRACT_ADDRESS[chain_id]
