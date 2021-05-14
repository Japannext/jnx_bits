from jnx_bits.itch.messages import ITCH_MSG_TYPES


def bytes_to_itch(bytes_):
    return ITCH_MSG_TYPES[bytes_[0]].from_bytes(bytes_)
