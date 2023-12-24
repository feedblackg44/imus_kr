class Place:
    def __init__(self, tokens=0, label=None):
        self.tokens = tokens
        self.held_tokens = 0
        self.incoming = []
        self.outgoing = []
        self.label = label

    def add_token(self, count=1, held=True):
        if held:
            self.held_tokens += count
        else:
            self.tokens += count

    def remove_held_tokens(self):
        self.tokens += self.held_tokens
        self.held_tokens = 0

    def remove_token(self, count=1):
        if self.tokens >= count:
            self.tokens -= count
            return True
        return False

    def add_incoming(self, edge):
        if edge not in self.incoming:
            self.incoming.append(edge)

    def add_outgoing(self, edge):
        if edge not in self.outgoing:
            self.outgoing.append(edge)

    def get_incoming_transitions(self):
        return [edge.transition for edge in self.incoming]

    def get_outgoing_transitions(self):
        return [edge.transition for edge in self.outgoing]
