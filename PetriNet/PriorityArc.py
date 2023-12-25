from .Arc import Arc


class PriorityArc(Arc):
    def __init__(self, place, transition, weight=1, to_transition=True, label=None, priority=0):
        super().__init__(place, transition, weight, to_transition, label)
        self.priority = priority

    def __str__(self):
        return f"{self.place.label} -> {self.transition.label}: {self.weight} ({self.priority})" \
            if self.to_transition \
            else f"{self.transition.label} -> {self.place.label}: {self.weight} ({self.priority})"
