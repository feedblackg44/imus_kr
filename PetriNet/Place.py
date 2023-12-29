import random

from .InhibitorArc import InhibitorArc
from .InhibitorPriorityArc import InhibitorPriorityArc
from .PriorityArc import PriorityArc
from .ProbabilityArc import ProbabilityArc
from .PlaceModes import PlaceModes


class Place:
    def __init__(self, tokens=0, label=None):
        self.tokens = tokens
        self.held_tokens = 0
        self.incoming = []
        self.outgoing = []
        self.label = label

    @property
    def outgoings(self):
        return [edge for edge in self.outgoing
                if not isinstance(edge, InhibitorArc) and not isinstance(edge, InhibitorPriorityArc)]

    @property
    def inhibiting_outgoings(self):
        return [edge for edge in self.outgoing
                if isinstance(edge, InhibitorArc) or isinstance(edge, InhibitorPriorityArc)]

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

    @property
    def mode(self):
        if self.outgoings:
            if isinstance(self.outgoing[0], PriorityArc):
                return PlaceModes.PRIORITY
            elif isinstance(self.outgoing[0], ProbabilityArc):
                return PlaceModes.PROBABILITY
        else:
            return PlaceModes.STANDARD

    def check_outgoings_valid(self):
        temp_outgoings = self.outgoings
        out_len = len(temp_outgoings)
        if out_len > 1:
            priorities = {edge.priority for edge in temp_outgoings if isinstance(edge, PriorityArc)}
            probabilities = [edge.probability for edge in temp_outgoings if isinstance(edge, ProbabilityArc)]
            if len(priorities) == len(probabilities) == 0:
                raise ValueError(f"There are multiple outgoing arcs from a place {self.label} "
                                 "without priorities or probabilities")
            if len(priorities) > 1 and len(probabilities) > 1:
                raise ValueError(f"There are multiple outgoing arcs from a place {self.label} "
                                 "with both priorities and probabilities")
            if 0 < len(priorities) < out_len:
                raise ValueError(f"There are multiple outgoing arcs from a place {self.label} "
                                 f"with not enough priorities")
            if 0 < len(probabilities) < out_len:
                raise ValueError(f"There are multiple outgoing arcs from a place {self.label} "
                                 f"with not enough probabilities")
        temp_inhibiting_outgoings = self.inhibiting_outgoings
        inh_len = len(temp_inhibiting_outgoings)
        if inh_len > 1:
            priorities = {edge.priority for edge in temp_inhibiting_outgoings if isinstance(edge, InhibitorPriorityArc)}
            if len(priorities) == 0:
                raise ValueError(f"There are multiple inhibiting outgoing arcs from a place {self.label} "
                                 "without priorities")
            if 0 < len(priorities) < inh_len:
                raise ValueError(f"There are multiple inhibiting outgoing arcs from a place {self.label} "
                                 f"with not enough priorities")
        return True

    def set_enabled_arcs(self, step_num=0):
        for arc in self.outgoing:
            arc.enabled = True
        temp_outgoings = [arc for arc in self.outgoings if arc.transition.is_enabled(step_num)]
        if sum([arc.weight for arc in temp_outgoings]) <= self.tokens:
            for arc in temp_outgoings:
                arc.enabled = True
        elif self.mode == PlaceModes.PRIORITY:
            temp_tokens = self.tokens
            sorted_arcs = sorted(temp_outgoings, key=lambda arc_: arc_.priority)
            for arc in sorted_arcs:
                if temp_tokens >= arc.weight:
                    arc.enabled = True
                    temp_tokens -= arc.weight
                else:
                    arc.enabled = False
        elif self.mode == PlaceModes.PROBABILITY:
            temp_tokens = self.tokens
            temp_arcs = [arc for arc in self.outgoings if arc.transition.is_enabled(step_num)]
            while temp_tokens >= max(0, min([arc.weight for arc in temp_arcs])):
                normalized_probabilities = [arc.probability / sum([arc.probability for arc in temp_arcs])
                                            for arc in temp_arcs]
                F = [0] + [sum(normalized_probabilities[:i + 1])
                           for i in range(len(normalized_probabilities) - 1)] + [1.0]
                rand = random.random()
                for i in range(len(F) - 1):
                    if F[i] <= rand < F[i + 1]:
                        temp_arcs[i].enabled = True
                        temp_tokens -= temp_arcs[i].weight
                        temp_arcs.pop(i)
                        break
            for arc in temp_arcs:
                arc.enabled = False
        else:
            for arc in self.outgoing:
                arc.enabled = True

        temp_inhibiting_outgoings = [arc for arc in self.inhibiting_outgoings if arc.transition.is_enabled(step_num)]
        if len(temp_inhibiting_outgoings) > 1:
            priorities = {edge.priority for edge in temp_inhibiting_outgoings if isinstance(edge, InhibitorPriorityArc)}
            if len(priorities) > 1:
                sorted_arcs = sorted(temp_inhibiting_outgoings, key=lambda arc_: arc_.priority)
                for arc in sorted_arcs:
                    if arc.transition.is_enabled(step_num) and self.tokens < arc.weight:
                        arc.enabled = True
                        temp_inhibiting_outgoings.remove(arc)
                        break
                    else:
                        arc.enabled = False
                for arc in temp_inhibiting_outgoings:
                    arc.enabled = False
