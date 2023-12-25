from .Arc import Arc


class ProbabilityArc(Arc):
    def __init__(self, place, transition, weight=1, to_transition=True, label=None, probability=1.0):
        super().__init__(place, transition, weight, to_transition, label)
        self.probability = probability

    def __str__(self):
        return f"{self.place.label} -> {self.transition.label}: {self.weight} ({self.probability})" \
            if self.to_transition \
            else f"{self.transition.label} -> {self.place.label}: {self.weight} ({self.probability})"
