import random


class Transition:
    def __init__(self, label=None, delay=0):
        self.incoming = []
        self.outgoing = []
        self.label = label
        self.delay = delay
        self.last_fired = 0
        self.not_fired = True

    def is_enabled(self, step_number=0):
        if self.delay >= 1:
            return (all(edge.can_fire() for edge in self.incoming) and
                    (self.not_fired or step_number - self.last_fired >= self.delay))
        elif self.delay > 0:
            return all(edge.can_fire() for edge in self.incoming) and random.random() < self.delay
        else:
            return all(edge.can_fire() for edge in self.incoming)

    def fire(self, step_number=0):
        if self.is_enabled(step_number):
            for edge in self.incoming:
                edge.consume_tokens()

            for edge in self.outgoing:
                edge.produce_tokens()

            self.last_fired = step_number
            if self.not_fired:
                self.not_fired = False
            return True
        return False

    def add_incoming(self, edge):
        if edge not in self.incoming:
            self.incoming.append(edge)

    def add_outgoing(self, edge):
        if edge not in self.outgoing:
            self.outgoing.append(edge)
