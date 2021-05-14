from jnx_bits.ouch.messages import OUCH_OUTGOING_MSG_TYPES, OUCH_INCOMING_MSG_TYPES


def bytes_to_outgoing_ouch(bytes_):
    return OUCH_OUTGOING_MSG_TYPES[bytes_[0]].from_bytes(bytes_)


def bytes_to_incoming_ouch(bytes_):
    return OUCH_INCOMING_MSG_TYPES[bytes_[0]].from_bytes(bytes_)


def bytes_to_ouch(bytes_):
    if bytes_[0] in (ord('O'), ord('X')):
        return bytes_to_outgoing_ouch(bytes_)
    if bytes_[0] in (ord('S'), ord('A'), ord('C'), ord('D'), ord('E'), ord('J')):
        return bytes_to_incoming_ouch(bytes_)
    if bytes_[0] == ord('U'):
        if len(bytes_) == 26:
            return bytes_to_outgoing_ouch(bytes_)
        else:
            return bytes_to_incoming_ouch(bytes_)
