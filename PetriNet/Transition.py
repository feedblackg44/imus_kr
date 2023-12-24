class Transition:
    def __init__(self, label=None):
        self.incoming = []
        self.outgoing = []
        self.label = label

    def is_enabled(self):
        return all(edge.can_fire() for edge in self.incoming)

    def fire(self):
        if self.is_enabled():
            for edge in self.incoming:
                edge.consume_tokens()

            for edge in self.outgoing:
                edge.produce_tokens()

    def add_incoming(self, edge):
        if edge not in self.incoming:
            self.incoming.append(edge)

    def add_outgoing(self, edge):
        if edge not in self.outgoing:
            self.outgoing.append(edge)
