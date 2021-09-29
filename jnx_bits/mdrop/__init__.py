#
# Copyright: Japannext Co., Ltd. <https://www.japannext.co.jp/>
# SPDX-License-Identifier: Apache-2.0
#

from jnx_bits.mdrop.messages import MDROP_MSG_TYPES

_msg_types = MDROP_MSG_TYPES.copy()


class IgnoredMessage:
    @classmethod
    def from_bytes(self, _):
        pass


def cherrypick(*classes):
    global _msg_types
    _msg_types = {k: v if v in classes else IgnoredMessage for k, v in MDROP_MSG_TYPES.items()}


def bytes_to_mdrop(bytes_):
    return _msg_types[bytes_[-1]].from_bytes(bytes_)
