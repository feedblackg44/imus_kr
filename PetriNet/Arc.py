class Arc:
    def __init__(self, place, transition, weight=1, to_transition=True, label=None):
        self.place = place
        self.transition = transition
        self.weight = int(weight)
        self.to_transition = to_transition
        self.label = label
        self.enabled = True

    def can_fire(self):
        if self.to_transition:
            return self.place.tokens >= self.weight and self.enabled
        else:
            return self.enabled

    def consume_tokens(self):
        if self.can_fire():
            self.place.remove_token(self.weight)

    def produce_tokens(self):
        self.place.add_token(self.weight)

    def __str__(self):
        return f"{self.place.label} -> {self.transition.label}: {self.weight}" \
            if self.to_transition \
            else f"{self.transition.label} -> {self.place.label}: {self.weight}"
