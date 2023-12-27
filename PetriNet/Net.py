import os
import shutil
import time

import graphviz
import numpy as np
import networkx as nx

from .Arc import Arc
from .InhibitorArc import InhibitorArc
from .Place import Place
from .PriorityArc import PriorityArc
from .ProbabilityArc import ProbabilityArc
from .Transition import Transition


class Net:
    def __init__(self, tickrate: int, folder: str = None) -> None:
        self.graph = None
        self.places: list[Place] = []
        self.transitions: list[Transition] = []
        self.history: list[list[Transition]] = []
        self.tickrate = tickrate
        self.folder = folder if folder else "output"

    def add_place(self, place: Place) -> None:
        self.places.append(place)

    def add_places(self, places: list[Place]) -> None:
        for place in places:
            self.add_place(place)

    def remove_place(self, place: Place) -> None:
        self.places.remove(place)

    def remove_places(self, places: list[Place]) -> None:
        for place in places:
            self.remove_place(place)

    def add_transition(self, transition: Transition) -> None:
        self.transitions.append(transition)

    def add_transitions(self, transitions: list[Transition]) -> None:
        for transition in transitions:
            self.add_transition(transition)

    def remove_transition(self, transition: Transition) -> None:
        self.transitions.remove(transition)

    def remove_transitions(self, transitions: list[Transition]) -> None:
        for transition in transitions:
            self.remove_transition(transition)

    def transitions_state(self, step_num) -> list[bool]:
        return [transition.is_enabled(step_num) for transition in self.transitions]

    def connect(self,
                vertex1: Place | Transition,
                vertex2: Transition | Place,
                weight: int = 1,
                priority: int = 0,
                probability: float = 1.0,
                inhibitor: bool = False) -> None:
        if isinstance(vertex1, Place) and isinstance(vertex2, Transition):
            self._connect(vertex1, vertex2, weight,
                          to_transition=True, priority=priority, probability=probability, inhibitor=inhibitor)
        elif isinstance(vertex1, Transition) and isinstance(vertex2, Place):
            self._connect(vertex2, vertex1, weight,
                          to_transition=False, priority=priority, probability=probability, inhibitor=inhibitor)
        else:
            raise TypeError("Invalid types")

    def _connect(self,
                 place: Place,
                 transition: Transition,
                 weight: int,
                 to_transition: bool,
                 priority: int,
                 probability: float,
                 inhibitor: bool) -> None:
        if place not in self.places:
            raise ValueError("Invalid place")
        if transition not in self.transitions:
            raise ValueError("Invalid transition")

        if inhibitor and to_transition:
            arc = InhibitorArc(place, transition, weight, to_transition)
        elif priority != 0:
            arc = PriorityArc(place, transition, weight, to_transition, priority=priority)
        elif probability != 1.0:
            arc = ProbabilityArc(place, transition, weight, to_transition, probability=probability)
        else:
            arc = Arc(place, transition, weight, to_transition)

        if to_transition:
            place.add_outgoing(arc)
            transition.add_incoming(arc)
        else:
            place.add_incoming(arc)
            transition.add_outgoing(arc)

    def step(self, step_num) -> bool:
        history = []
        for i, state in enumerate(self.transitions_state(step_num)):
            if state:
                transition = self.transitions[i]
                transition.fire(step_num)
                history.append(transition)
        for place in self.places:
            place.remove_held_tokens()
        self.history.append(history)
        return len(history) != 0

    def simulate(self, steps: int, draw=False) -> None:
        for place in self.places:
            place.check_outgoings_valid()
        if draw:
            shutil.rmtree(self.folder, ignore_errors=True)
            os.mkdir(self.folder)
            self.draw_viz(filename=f"graph_step_0")
        print(f"Initial state:")
        sleep_time = 1 / self.tickrate
        for place in self.places:
            print(f"{place.label}: {place.tokens}")
        print()
        for i in range(steps):
            for place in self.places:
                place.set_enabled_arcs()
            if not self.step(i):
                print("There are no more enabled transitions")
                break
            if draw:
                self.draw_viz(filename=f"graph_step_{i + 1}")
            print(f"State {i + 1}:")
            for place in self.places:
                print(f"{place.label}: {place.tokens}")
            print()
            time.sleep(sleep_time)

    @property
    def incidence_matrices(self) -> tuple[np.ndarray, np.ndarray]:
        d_plus = np.zeros((len(self.places), len(self.transitions)))
        d_minus = np.zeros((len(self.places), len(self.transitions)))

        for i, place in enumerate(self.places):
            for arc in place.incoming:
                d_minus[i, self.transitions.index(arc.transition)] += arc.weight

            for arc in place.outgoing:
                d_plus[i, self.transitions.index(arc.transition)] += arc.weight

        return d_plus, d_minus

    @property
    def marking_vector(self) -> np.ndarray:
        return np.array([place.tokens for place in self.places])

    def find_place_by_label(self, label: str) -> Place | None:
        for place in self.places:
            if place.label == label:
                return place
        return None

    def find_transition_by_label(self, label: str) -> Transition | None:
        for transition in self.transitions:
            if transition.label == label:
                return transition
        return None

    def create_graph(self):
        self.graph = nx.DiGraph()

        for place in self.places:
            self.graph.add_node(place.label, label=place.label, type='place')

        for transition in self.transitions:
            self.graph.add_node(transition.label, label=transition.label, type='transition')

        for place in self.places:
            for arc in place.outgoing:
                self.graph.add_edge(place.label, arc.transition.label,
                                    weight=arc.weight,
                                    type='inhibitor' if isinstance(arc, InhibitorArc) else 'standard')
            for arc in place.incoming:
                self.graph.add_edge(arc.transition.label, place.label, weight=arc.weight, type='standard')

    def draw_viz(self, filename='graph_output'):
        filename = os.path.join(self.folder, filename)

        if not self.graph:
            self.create_graph()

        dot = graphviz.Digraph()

        for n in self.graph.nodes:
            if self.graph.nodes[n]['type'] == 'place':
                dot.node(n, label=f"{n}\n{self.find_place_by_label(n).tokens}", shape='circle', style='filled',
                         color='lightblue')
            else:
                dot.node(n, label=n, shape='square', style='filled', color='lightgreen')

        for u, v, data in self.graph.edges(data=True):
            if data['type'] == 'inhibitor':
                dot.edge(u, v, label=str(data['weight']), style='dashed')
            else:
                dot.edge(u, v, label=str(data['weight']))

        dot.render(filename, format='png')
        os.remove(filename)
