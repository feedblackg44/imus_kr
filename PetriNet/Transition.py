import random


class Transition:
    def __init__(self, label=None, delay=None):
        self.incoming = []
        self.outgoing = []
        self.label = label
        self.delay = delay
        self.last_fired = 0

    def is_enabled(self, step_number=0):
        if isinstance(self.delay, int):
            return all(edge.can_fire() for edge in self.incoming) and step_number - self.last_fired >= self.delay
        elif isinstance(self.delay, float):
            return all(edge.can_fire() for edge in self.incoming) and random.random() >= self.delay
        else:
            return all(edge.can_fire() for edge in self.incoming)

    def fire(self, step_number=0):
        if self.is_enabled(step_number):
            for edge in self.incoming:
                edge.consume_tokens()

            for edge in self.outgoing:
                edge.produce_tokens()

            self.last_fired = step_number

    def add_incoming(self, edge):
        if edge not in self.incoming:
            self.incoming.append(edge)

    def add_outgoing(self, edge):
        if edge not in self.outgoing:
            self.outgoing.append(edge)
