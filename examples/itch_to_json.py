#
# Copyright: Japannext Co., Ltd. <https://www.japannext.co.jp/>
# SPDX-License-Identifier: Apache-2.0
#

import sys
import jnx_bits.soupbin.file
import jnx_bits.itch
from datetime import datetime
import json

if len(sys.argv) <= 1:
    print(f"Usage: {sys.argv[0]} ITCHTV.log", file=sys.stderr)
    print(f"", file=sys.stderr)
    print(f"Where ITCHTV.log is the binary ITCH log file", file=sys.stderr)
    sys.exit(0)

with jnx_bits.soupbin.file.SoupBinFile(sys.argv[1]) as soupbin:
    for msg in soupbin:
        if msg:
            msg = jnx_bits.itch.bytes_to_itch(msg)
            print( json.dumps( { "type": msg.__class__.__name__, **(vars(msg)) }))
