from dataclasses import dataclass
from os import environ
from struct import Struct
from datetime import datetime
from jnx_bits.common.messages import ApplicationMessageMixin


FEED_DATE = datetime.strptime(environ['FEED_DATE'], '%Y%m%d') if environ.get('FEED_DATE') else datetime.now()


def last_midnight_to_datetime():
    return datetime(FEED_DATE.year, FEED_DATE.month, FEED_DATE.day, 0, 0)


class ItchMessageMixin(ApplicationMessageMixin):
    last_midnight = last_midnight_to_datetime()
    last_midnight_unix = int(last_midnight.timestamp())

    def real_timestamp(self):
        return (ItchTimestamp.last_timestamp * 1_000_000) + self.timestamp

    def unix_timestamp(self):
        return (ItchMessageMixin.last_midnight_unix + ItchTimestamp.last_timestamp) * 1_000_000_000 + self.timestamp


@dataclass
class ItchTimestamp(ItchMessageMixin):
    last_timestamp = None
    msg_struct = Struct('>cI')
    message_type: str
    timestamp: int

    def __post_init__(self):
        type(self).last_timestamp = self.timestamp
        super().__post_init__()

    def real_timestamp(self):
        return self.timestamp * 1_000_000_000


@dataclass
class ItchSystemEvent(ItchMessageMixin):
    msg_struct = Struct('>cI4sc')
    message_type: str
    timestamp: int
    group: str
    system_event: str


@dataclass
class ItchPriceTickSize(ItchMessageMixin):
    msg_struct = Struct('>cIIII')
    message_type: str
    timestamp: int
    price_tick_size_table_id: int
    tick_size: int
    price_start: int


@dataclass
class ItchOrderbookDirectory(ItchMessageMixin):
    msg_struct = Struct('>cII12s4sIIIII')
    message_type: str
    timestamp: int
    orderbook_id: int
    orderbook_code: str
    group: str
    round_lot_size: int
    price_tick_size_table_id: int
    price_decimals: int
    upper_price_limit: int
    lower_price_limit: int


@dataclass
class ItchTradingState(ItchMessageMixin):
    msg_struct = Struct('>cII4sc')
    message_type: str
    timestamp: int
    orderbook_id: int
    group: str
    trading_state: str


@dataclass
class ItchShortSellingPriceRestriction(ItchMessageMixin):
    msg_struct = Struct('>cII4sc')
    message_type: str
    timestamp: int
    orderbook_id: int
    group: str
    short_selling_state: str


@dataclass
class ItchOrderAdded(ItchMessageMixin):
    msg_struct = Struct('>cIQcII4sI')
    message_type: str
    timestamp: int
    order_number: int
    side: str
    quantity: int
    orderbook_id: int
    group: str
    price: int


@dataclass
class ItchOrderAddedWithAttr(ItchMessageMixin):
    msg_struct = Struct('>cIQcII4sI4sc')
    message_type: str
    timestamp: int
    order_number: int
    side: str
    quantity: int
    orderbook_id: int
    group: str
    price: int
    attribution: str
    order_type: str


@dataclass
class ItchOrderExecuted(ItchMessageMixin):
    msg_struct = Struct('>cIQIQ')
    message_type: str
    timestamp: int
    order_number: int
    executed_quantity: int
    match_number: int


@dataclass
class ItchOrderDeleted(ItchMessageMixin):
    msg_struct = Struct('>cIQ')
    message_type: str
    timestamp: int
    order_number: int


@dataclass
class ItchOrderReplaced(ItchMessageMixin):
    msg_struct = Struct('>cIQQII')
    message_type: str
    timestamp: int
    orig_order_number: int
    new_order_number: int
    quantity: int
    price: int


@dataclass
class ItchEndOfSnapshot(ItchMessageMixin):
    msg_struct = Struct('>cQ')
    message_type: str
    sequence_number: int


ITCH_MSG_TYPES = {
    ord('T'): ItchTimestamp,
    ord('S'): ItchSystemEvent,
    ord('L'): ItchPriceTickSize,
    ord('R'): ItchOrderbookDirectory,
    ord('H'): ItchTradingState,
    ord('Y'): ItchShortSellingPriceRestriction,
    ord('A'): ItchOrderAdded,
    ord('F'): ItchOrderAddedWithAttr,
    ord('E'): ItchOrderExecuted,
    ord('D'): ItchOrderDeleted,
    ord('U'): ItchOrderReplaced,
    ord('G'): ItchEndOfSnapshot,
}
