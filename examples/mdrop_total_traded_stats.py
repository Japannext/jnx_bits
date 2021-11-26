#
# Copyright: Japannext Co., Ltd. <https://www.japannext.co.jp/>
# SPDX-License-Identifier: Apache-2.0
#

import sys
from jnx_bits.soupbin.file import SoupBinFile
from jnx_bits.mdrop import bytes_to_mdrop, cherrypick
from jnx_bits.mdrop.messages import MdTradeReport

global total_traded_value
total_traded_value = 0

global total_trades
total_trades = 0

global fix_total_value
fix_total_value = 0


# Process only MdTradeReport messages
cherrypick(MdTradeReport)


# Hooks run on every instance initialised
def trade_report_hook(self):
    value = (self.qty * self.price) / 10
    global total_traded_value
    total_traded_value += value

    global total_trades
    total_trades += 1

    global fix_total_value
    if self.trade_details_field.buy_is_fix:
        fix_total_value += value
    if self.trade_details_field.sell_is_fix:
        fix_total_value += value


MdTradeReport.hook = trade_report_hook

if len(sys.argv) <= 1:
    print(f"Usage: {sys.argv[0]} MDROP.log", file=sys.stderr)
    print(f"", file=sys.stderr)
    print(f"Where MDROP.log is the binary MDROP log file", file=sys.stderr)
    sys.exit(0)

with SoupBinFile(sys.argv[1]) as soupbin:
    for msg in soupbin:
        bytes_to_mdrop(msg)


print(f"Total traded value (single counted): {total_traded_value}")
print(f"Total trades: {total_trades}")
print(f"Total FIX traded value: {fix_total_value}")
print(f"Total OUCH traded value: {(total_traded_value * 2) - fix_total_value}")
