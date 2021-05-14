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
        return str(vars(self))
