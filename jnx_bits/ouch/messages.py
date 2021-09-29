#
# Copyright: Japannext Co., Ltd. <https://www.japannext.co.jp/>
# SPDX-License-Identifier: Apache-2.0
#

# pylint: disable=too-many-instance-attributes, too-few-public-methods

from struct import Struct
from dataclasses import dataclass
from jnx_bits.common.messages import ApplicationMessageMixin


@dataclass
class OuchEnterOrder(ApplicationMessageMixin):
    msg_struct = Struct('>cI10scII4sIIIccIcc')
    message_type: str
    token: int
    client_ref: str
    side: str
    quantity: int
    orderbook_id: int
    group: str
    price: int
    time_in_force: int
    firm_id: int
    display: str
    capacity: str
    minqty: int
    order_classification: str
    cash_margin_type: str


@dataclass
class OuchReplaceOrder(ApplicationMessageMixin):
    msg_struct = Struct('>cIIIIIcI')
    message_type: str
    orig_token: int
    new_token: int
    quantity: int
    price: int
    time_in_force: int
    display: str
    minqty: int


@dataclass
class OuchCancelOrder(ApplicationMessageMixin):
    msg_struct = Struct('>cII')
    message_type: str
    token: int
    quantity: int


@dataclass
class OuchSystemEvent(ApplicationMessageMixin):
    msg_struct = Struct('>cQc')
    message_type: str
    timestamp: int
    system_event: str


@dataclass
class OuchOrderAccepted(ApplicationMessageMixin):
    msg_struct = Struct('>cQI10scII4sIIIccQIccc')
    message_type: str
    timestamp: int
    token: int
    client_ref: str
    side: str
    quantity: int
    orderbook_id: int
    group: str
    price: int
    time_in_force: int
    firm_id: int
    display: str
    capacity: str
    order_no: int
    minqty: int
    order_state: str
    order_classification: str
    cash_margin_type: str


@dataclass
class OuchOrderReplaced(ApplicationMessageMixin):
    msg_struct = Struct('>cQIcII4sIIcQIcI')
    message_type: str
    timestamp: int
    new_token: int
    side: str
    quantity: int
    orderbook_id: int
    group: str
    price: int
    time_in_force: int
    display: str
    order_no: int
    minqty: int
    order_state: str
    orig_token: int


@dataclass
class OuchOrderCanceled(ApplicationMessageMixin):
    msg_struct = Struct('>cQIIc')
    message_type: str
    timestamp: int
    token: int
    decrement_qty: int
    reason: str


@dataclass
class OuchOrderAIQCanceled(ApplicationMessageMixin):
    msg_struct = Struct('>cQIIcIIc')
    message_type: str
    timestamp: int
    token: int
    decrement_qty: int
    reason: str
    qty_prevented_from_trading: int
    execution_price: int
    liquidity_indicator: str


@dataclass
class OuchOrderExecuted(ApplicationMessageMixin):
    msg_struct = Struct('>cQIIIcQ')
    message_type: str
    timestamp: int
    token: int
    executed_qty: int
    execution_price: int
    liquidity_indicator: str
    match_no: int


@dataclass
class OuchOrderRejected(ApplicationMessageMixin):
    msg_struct = Struct('>cQIc')
    message_type: str
    timestamp: int
    token: int
    reason: str


OUCH_OUTGOING_MSG_TYPES = {
    ord('O'): OuchEnterOrder,
    ord('U'): OuchReplaceOrder,
    ord('X'): OuchCancelOrder,
}

OUCH_INCOMING_MSG_TYPES = {
    ord('S'): OuchSystemEvent,
    ord('A'): OuchOrderAccepted,
    ord('U'): OuchOrderReplaced,
    ord('C'): OuchOrderCanceled,
    ord('D'): OuchOrderAIQCanceled,
    ord('E'): OuchOrderExecuted,
    ord('J'): OuchOrderRejected,
}
