#
# Copyright: Japannext Co., Ltd. <https://www.japannext.co.jp/>
# SPDX-License-Identifier: Apache-2.0
#

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
