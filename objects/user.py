class User:
    def __init__(self, sid, name):
        self.sid = sid
        self.name = name

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.sid == other.sid
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.sid)
