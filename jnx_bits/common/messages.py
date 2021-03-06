#
# Copyright: Japannext Co., Ltd. <https://www.japannext.co.jp/>
# SPDX-License-Identifier: Apache-2.0
#

import json
class ApplicationMessageMixin:
    @classmethod
    def from_bytes(cls, bytes_):
        fields = (
            f.decode('UTF-8') if isinstance(f, (bytes, bytearray)) else f
            for f in cls.msg_struct.unpack(bytes_)
        )
        return cls(*fields)

    def __post_init__(self):
        self.hook()

    def hook(self):
        """Overwrite this to trigger actions when messages are received."""
        pass

    def to_json(self):
        return json.dumps( { "msg_type_name": self.__class__.__name__, **vars(self) }, default = lambda o: o.__dict__)
