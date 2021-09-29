#
# Copyright: Japannext Co., Ltd. <https://www.japannext.co.jp/>
# SPDX-License-Identifier: Apache-2.0
#

import struct


class EndOfFile(Exception):
    pass


class SoupBinFile:
    def __init__(self, file_):
        self.file_ = file_
        self.filehandle = None

    def __enter__(self):
        self.filehandle = open(self.file_, 'rb')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.filehandle.close()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.read_message()
        except EndOfFile:
            raise StopIteration

    def read_message(self):
        return self.filehandle.read(self.__msg_length())

    def __msg_length(self):
        try:
            return struct.unpack('>H', self.filehandle.read(2))[0]
        except struct.error:
            raise EndOfFile
