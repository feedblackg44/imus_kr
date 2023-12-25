class Transition:
    def __init__(self, label=None, delay=0):
        self.incoming = []
        self.outgoing = []
        self.label = label
        self.delay = delay

    def is_enabled(self, step_number=0):
        return all(edge.can_fire() for edge in self.incoming) and step_number % (self.delay + 1) == 0

    def fire(self, step_number=0):
        if self.is_enabled(step_number):
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
