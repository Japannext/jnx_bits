# jnx_bits

A module to decode the "bits" of the binary protocols used in the Japannext PTS.

It can be used to easily translate the binary files into readable JSON for example.

# Quick start

    python3 -mvenv env
    ./env/bin/pip install --upgrade pip
    ./env/bin/python -mdataclasses &>/dev/null || ./env/bin/pip install dataclasses # No need to install in Python > 3.6
    ./env/bin/pip install .
    ./env/bin/python examples/...
