from eip712.messages import EIP712Message, EIP712Type
from eth_typing import Address

# Intent Trade API
INTENT_TRADE_API = "https://arbitrum-gapi.hmx.org"


class TradeOrder(EIP712Type):
  marketIndex: "int"
  sizeDelta: "int"
  triggerPrice: "int"
  acceptablePrice: "int"
  triggerAboveThreshold: "bool"
  reduceOnly: "int"
  tpToken: "Address"
  createdTimestamp: "int"
  expiryTimestamp: "int"
  account: "Address"
  subAccountId: "int"


class IntentTrade(EIP712Message):
  _name_ = "IntentHander"
  _chainId_ = 421614
  _version_ = '1.0.0'
  _verifyingContract_ = "0xdbdaCA3C5F52e3F287B48b08713De8a3639D0fE5"

  primaryType = 'TradeOrder'

  message: TradeOrder
