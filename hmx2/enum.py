from enum import Enum


class Cmd:
  CREATE = 0
  UPDATE = 1
  CANCEL = 2


class Action:
  BUY = True
  SELL = False


class IntentOrderStatus:
  Success = 'success'
  Pending = 'pending'
  Cancelled = 'cancelled'
  Expired = 'expired'
