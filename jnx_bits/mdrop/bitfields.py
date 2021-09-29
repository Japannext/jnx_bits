#
# Copyright: Japannext Co., Ltd. <https://www.japannext.co.jp/>
# SPDX-License-Identifier: Apache-2.0
#

# TODO: check whether it's faster with BitStream.

from dataclasses import dataclass

ORDER_VERB = {
    '00': 'B',
    '01': 'S',
    '10': 'T',
    '11': 'E',
}

STR_TO_BOOL = {  # Override non empty strings being truey in python.
    '0': False,
    '1': True,
}

DISPLAY = {
    '0': '',
    '1': 'P',
}

CAPACITY = {
    '0': 'P',
    '1': 'A',
}

AGGRESSOR = {
    '0': 'S',
    '1': 'B',
}


@dataclass
class MdOrderDetailsField:
    expired_on_entry: bool
    display: str
    capacity: str
    reserved: str
    order_verb: str

    @classmethod
    def from_bytes(cls, bytes_):
        bitstr = format(ord(bytes_), '08b')
        return cls(
            STR_TO_BOOL[bitstr[0]],
            DISPLAY[bitstr[1]],
            CAPACITY[bitstr[2]],
            bitstr[3:6],
            ORDER_VERB[bitstr[6:]],
        )


@dataclass
class MdTradeDetailsField:
    aggressor: str
    reserved: str
    sell_is_fix: bool
    buy_is_fix: bool

    @classmethod
    def from_bytes(cls, bytes_):
        bitstr = format(ord(bytes_), '08b')
        return cls(
            AGGRESSOR[bitstr[0]],
            bitstr[1:6],
            STR_TO_BOOL[bitstr[6]],
            STR_TO_BOOL[bitstr[7]],
        )


class MdStpdReportDetailsField(MdTradeDetailsField):
    pass
