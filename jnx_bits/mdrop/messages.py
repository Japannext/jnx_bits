# pylint: disable=too-many-instance-attributes, too-few-public-methods

from dataclasses import dataclass
from struct import Struct
from jnx_bits.common.messages import ApplicationMessageMixin
from jnx_bits.mdrop.bitfields import (
    MdOrderDetailsField,
    MdTradeDetailsField,
    MdStpdReportDetailsField,
)


class MdropMessageMixin(ApplicationMessageMixin):
    def real_timestamp(self):
        return (MdSeconds.last_second * 1_000_000_000) + self.timestamp


@dataclass
class MdTransactionDelimiter(MdropMessageMixin):
    msg_struct = Struct('<Ic')
    timestamp: int
    msg_type: str


@dataclass
class MdOrderDetails:
    msg_struct = Struct('<iiQIQIIc')
    price: int
    entry_price: int
    qty: int
    order_no: int
    min_qty: int
    user_id: int
    time_in_force: int
    order_details_field: int

    @classmethod
    def from_bytes(cls, bytes_):
        (
            price,
            entry_price,
            qty,
            order_no,
            min_qty,
            user_id,
            time_in_force,
            order_details_field,
        ) = cls.msg_struct.unpack(bytes_)
        return cls(
            price,
            entry_price,
            qty,
            order_no,
            min_qty,
            user_id,
            time_in_force,
            MdOrderDetailsField.from_bytes(order_details_field),
        )


@dataclass
class MdFixOrderAccepted(MdropMessageMixin):
    msg_struct = Struct('<II32sIQ37s16s3c')
    timestamp: int
    sec_board_idx: int
    external_order_id: str
    mpid: int
    visible_qty: int
    order_details: bytes
    client_ref: str
    hft_flag: str
    margin_flag: str
    msg_type: str

    @classmethod
    def from_bytes(cls, bytes_):
        (
            timestamp,
            sec_board_idx,
            external_order_id,
            mpid,
            visible_qty,
            order_details,
            client_ref,
            hft_flag,
            margin_flag,
            msg_type,
        ) = cls.msg_struct.unpack(bytes_)
        return cls(
            timestamp,
            sec_board_idx,
            external_order_id.decode(),
            mpid,
            visible_qty,
            MdOrderDetails.from_bytes(order_details),
            client_ref.decode(),
            hft_flag.decode(),
            margin_flag.decode(),
            msg_type.decode(),
        )


@dataclass
class MdOuchOrderAccepted(MdropMessageMixin):
    msg_struct = Struct('<IIII37s10sccc')
    timestamp: int
    sec_board_idx: int
    token: int
    mpid: int
    order_details: MdOrderDetails
    client_ref: str
    hft_flag: str
    margin_flag: str
    msg_type: str

    @classmethod
    def from_bytes(cls, bytes_):
        (
            timestamp,
            sec_board_idx,
            token,
            mpid,
            order_details,
            client_ref,
            hft_flag,
            margin_flag,
            msg_type,
        ) = cls.msg_struct.unpack(bytes_)
        return cls(
            timestamp,
            sec_board_idx,
            token,
            mpid,
            MdOrderDetails.from_bytes(order_details),
            client_ref.decode(),
            hft_flag.decode(),
            margin_flag.decode(),
            msg_type.decode(),
        )


@dataclass
class MdFixOrderReplaced(MdropMessageMixin):
    msg_struct = Struct('<II32sQI37sc')
    timestamp: int
    sec_board_idx: int
    external_order_id: str
    visible_qty: int
    orig_order_no: int
    order_details: MdOrderDetails
    msg_type: str

    @classmethod
    def from_bytes(cls, bytes_):
        (
            timestamp,
            sec_board_idx,
            external_order_id,
            visible_qty,
            orig_order_no,
            order_details,
            msg_type,
        ) = cls.msg_struct.unpack(bytes_)
        return cls(
            timestamp,
            sec_board_idx,
            external_order_id.decode(),
            visible_qty,
            orig_order_no,
            MdOrderDetails.from_bytes(order_details),
            msg_type.decode(),
        )


@dataclass
class MdOuchOrderReplaced(MdropMessageMixin):
    msg_struct = Struct('<IIII37sc')
    timestamp: int
    sec_board_idx: int
    token: int
    orig_order_no: int
    order_details: MdOrderDetails
    msg_type: str

    @classmethod
    def from_bytes(cls, bytes_):
        (
            timestamp,
            sec_board_idx,
            token,
            orig_order_no,
            order_details,
            msg_type,
        ) = cls.msg_struct.unpack(bytes_)
        return cls(
            timestamp,
            sec_board_idx,
            token,
            orig_order_no,
            MdOrderDetails.from_bytes(order_details),
            msg_type.decode(),
        )


@dataclass
class MdFixOrderCancelled(MdropMessageMixin):
    msg_struct = Struct('<II32sIIIcc')
    timestamp: int
    sec_board_idx: int
    external_order_id: str
    order_no: int
    user_id: int
    operator_id: int
    reason: str
    msg_type: str


@dataclass
class MdOuchOrderCancelled(MdropMessageMixin):
    msg_struct = Struct('<IIIIIcc')
    timestamp: int
    sec_board_idx: int
    order_no: int
    user_id: int
    operator_id: int
    reason: str
    msg_type: str


@dataclass
class MdTradeReport(MdropMessageMixin):
    msg_struct = Struct('<IIIIQIIIIIIcc')
    timestamp: int
    sec_board_idx: int
    trade_no: int
    price: int
    qty: int
    buy_orig_order_no: int
    buy_order_no: int
    buy_user_id: int
    sell_orig_order_no: int
    sell_order_no: int
    sell_user_id: int
    trade_details_field: MdTradeDetailsField
    msg_type: str

    @classmethod
    def from_bytes(cls, bytes_):
        (
            timestamp,
            sec_board_idx,
            trade_no,
            price,
            qty,
            buy_orig_order_no,
            buy_order_no,
            buy_user_id,
            sell_orig_order_no,
            sell_order_no,
            sell_user_id,
            trade_details_field,
            msg_type,
        ) = cls.msg_struct.unpack(bytes_)
        return cls(
            timestamp,
            sec_board_idx,
            trade_no,
            price,
            qty,
            buy_orig_order_no,
            buy_order_no,
            buy_user_id,
            sell_orig_order_no,
            sell_order_no,
            sell_user_id,
            MdTradeDetailsField.from_bytes(trade_details_field),
            msg_type.decode(),
        )


@dataclass
class MdStpReport(MdropMessageMixin):  # not yet tested
    msg_struct = Struct('<IIIQIIIIcc')
    timestamp: int
    sec_board_idx: int
    price: int
    qty: int
    buy_order_no: int
    buy_user_id: int
    sell_order_no: int
    sell_user_id: int
    stpd_report_details_field: MdStpdReportDetailsField
    msg_type: str

    @classmethod
    def from_bytes(cls, bytes_):
        (
            timestamp,
            sec_board_idx,
            price,
            qty,
            buy_order_no,
            buy_user_id,
            sell_order_no,
            sell_order_id,
            stpd_report_details_field,
            msg_type,
        ) = cls.msg_struct.unpack(bytes_)
        return cls(
            timestamp,
            sec_board_idx,
            price,
            qty,
            buy_order_no,
            buy_user_id,
            sell_order_no,
            sell_order_id,
            MdStpdReportDetailsField.from_bytes(stpd_report_details_field),
            msg_type.decode(),
        )


@dataclass
class MdFixOrderRejected(MdropMessageMixin):
    msg_struct = Struct('<II32sIQ37s16sHc')
    timestamp: int
    sec_board_idx: int
    external_order_id: str
    mpid: int
    visible_qty: int
    order_details: MdOrderDetails
    client_ref: str
    reject_code: int
    msg_type: str

    @classmethod
    def from_bytes(cls, bytes_):
        (
            timestamp,
            sec_board_idx,
            external_order_id,
            mpid,
            visible_qty,
            order_details,
            client_ref,
            reject_code,
            msg_type,
        ) = cls.msg_struct.unpack(bytes_)
        return cls(
            timestamp,
            sec_board_idx,
            external_order_id.decode(),
            mpid,
            visible_qty,
            MdOrderDetails.from_bytes(order_details),
            client_ref.decode(),
            reject_code,
            msg_type.decode(),
        )


@dataclass
class MdFixOrderReplaceRejected(MdropMessageMixin):
    msg_struct = Struct('<II32s32sIIIHc')
    timestamp: int
    sec_board_idx: int
    external_order_id: str
    orig_external_order_id: str
    order_no: int
    user_id: int
    operator_id: int
    reject_code: int
    msg_type: str


@dataclass
class MdFixOrderCancelRejected(MdropMessageMixin):
    msg_struct = Struct('<II32s32sIIIHc')
    timestamp: int
    sec_board_idx: int
    external_order_id: str
    orig_external_order_id: str
    order_no: int
    user_id: int
    operator_id: int
    reject_code: int
    msg_type: str


@dataclass
class MdOuchOrderRejected(MdropMessageMixin):
    msg_struct = Struct('<IIIIIcc')
    timestamp: int
    sec_board_idx: int
    token: int
    user_id: int
    operator_id: int
    reason: str
    msg_type: str


@dataclass
class MdFixReliableSequencedMessageChannelMessagePayload(MdropMessageMixin):
    msg_struct = Struct('<II55sc')
    timestamp: int
    user_id: int
    data: str
    msg_type: str


@dataclass
class MdDate(MdropMessageMixin):
    msg_struct = Struct('<Ic')
    date: int
    msg_type: str


@dataclass
class MdSeconds(MdropMessageMixin):
    last_second = None
    msg_struct = Struct('<Qc')
    seconds: int
    msg_type: str

    def __post_init__(self):
        type(self).last_second = self.seconds
        super().__post_init__()


@dataclass
class MdQtyTickTable(MdropMessageMixin):
    msg_struct = Struct('<IIQQc')
    timestamp: int
    table_idx: int
    tick_size: int
    start_value: int
    msg_type: str


@dataclass
class MdPriceTickTable(MdropMessageMixin):
    msg_struct = Struct('<IIIIc')
    timestamp: int
    table_idx: int
    tick_size: int
    start_value: int
    msg_type: str


@dataclass
class MdSecboardTable(MdropMessageMixin):
    msg_struct = Struct('<III4s12sQIIIIIIc')
    timestamp: int
    sec_board_idx: int
    orderbook_id: int
    board_id: str
    isin: str
    min_qty_step: int
    qty_decimals: int
    price_tick_table_idx: int
    price_decimals: int
    reference_price: int
    upper_price_limit: int
    lower_price_limit: int
    msg_type: str


@dataclass
class MdFirmTable(MdropMessageMixin):
    msg_struct = Struct('<III12sccc')
    timestamp: int
    firm_idx: int
    firm_id: int
    firm_code: str
    firm_class: str
    state: str
    msg_type: str


@dataclass
class MdUserTable(MdropMessageMixin):
    msg_struct = Struct('<IIII12s20scc')
    timestamp: int
    firm_idx: int
    user_id: int
    user_idx: int
    user_code: str
    role: str
    state: str
    msg_type: str


@dataclass
class MdUserEvent(MdropMessageMixin):
    msg_struct = Struct('<IIIIIIHHHcc')
    timestamp: int
    user_id: int
    domain_id: int
    server_user_id: int
    connection_id: int
    client_ip_address: int
    active_user_connections: int
    server_port: int
    client_port: int
    user_event_type: str
    msg_type: str


@dataclass
class MdTradeEvent(MdropMessageMixin):
    msg_struct = Struct('<IIIIQQ4s12scc')
    timestamp: int
    trade_event_idx: int
    sec_board_idx: int
    priority: int
    event_time: int
    actual_event_time: int
    board_id: str
    transition_name: str
    state: str
    msg_type: str


@dataclass
class MdMpidTable(MdropMessageMixin):
    msg_struct = Struct('<IIcc')
    timestamp: int
    mpid: int
    self_cross_action: str
    msg_type: str


@dataclass
class MdUserMpidTable(MdropMessageMixin):
    msg_struct = Struct('<IIIc')
    timestamp: int
    mpid: int
    user_id: int
    msg_type: str


@dataclass
class MdTeState(MdropMessageMixin):
    msg_struct = Struct('<Icc')
    timestamp: int
    state: str
    msg_type: str


@dataclass
class MdBoardTradingState(MdropMessageMixin):
    msg_struct = Struct('<I4scc')
    timestamp: int
    board_id: int
    state: str
    msg_type: str


@dataclass
class MdSecboardTradingState(MdropMessageMixin):
    msg_struct = Struct('<IIcc')
    timestamp: int
    sec_board_idx: int
    state: str
    msg_type: str


@dataclass
class MdFirmState(MdropMessageMixin):
    msg_struct = Struct('<IIcc')
    timestamp: int
    firm_idx: int
    state: str
    msg_type: str


@dataclass
class MdUserState(MdropMessageMixin):
    msg_struct = Struct('<IIcc')
    timestamp: int
    user_id: int
    state: str
    msg_type: str


@dataclass
class MdShortsellRestriction(MdropMessageMixin):
    msg_struct = Struct('<IIcc')
    timestamp: int
    sec_board_idx: int
    price_restriction_status: str
    msg_type: str


MDROP_MSG_TYPES = {
    ord('#'): MdTransactionDelimiter,
    ord('a'): MdFixOrderAccepted,
    ord('A'): MdOuchOrderAccepted,
    ord('u'): MdFixOrderReplaced,
    ord('U'): MdOuchOrderReplaced,
    ord('d'): MdFixOrderCancelled,
    ord('D'): MdOuchOrderCancelled,
    ord('E'): MdTradeReport,
    ord('e'): MdStpReport,
    ord('j'): MdFixOrderRejected,
    ord('k'): MdFixOrderReplaceRejected,
    ord('l'): MdFixOrderCancelRejected,
    ord('J'): MdOuchOrderRejected,
    ord('%'): MdFixReliableSequencedMessageChannelMessagePayload,
    ord('C'): MdDate,
    ord('T'): MdSeconds,
    ord('M'): MdQtyTickTable,
    ord('L'): MdPriceTickTable,
    ord('R'): MdSecboardTable,
    ord('F'): MdFirmTable,
    ord('P'): MdUserTable,
    ord('$'): MdUserEvent,
    ord('S'): MdTradeEvent,
    ord('Q'): MdMpidTable,
    ord('q'): MdUserMpidTable,
    ord('!'): MdTeState,
    ord('H'): MdBoardTradingState,
    ord('h'): MdSecboardTradingState,
    ord('f'): MdFirmState,
    ord('p'): MdUserState,
    ord('Y'): MdShortsellRestriction,
}
