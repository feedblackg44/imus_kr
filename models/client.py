import random

from PetriNet import Net, Place, Transition


def create_model(tickrate, model_id, order_probability=0.5, client_demand=5):
    petri_net = Net(tickrate=tickrate)

    # Places
    Places = [
        Place(0, f"{model_id}\nClient"),
        Place(0, f"{model_id}\nOrder Requests"),
        Place(0, f"{model_id}\nSatisfied Clients"),
        Place(0, f"{model_id}\nUnhappy Clients")
    ]
    petri_net.add_places(Places)
    Places = {place.label: place for place in Places}

    # Transactions
    Transitions = [
        Transition(f"{model_id}\nClient Order"),
        Transition(f"{model_id}\nCreate Order", delay=order_probability),
        Transition(f"{model_id}\nSatisfied"),
        Transition(f"{model_id}\nUnhappy")
    ]
    petri_net.add_transitions(Transitions)
    Transitions = {transition.label: transition for transition in Transitions}

    # Arcs
    petri_net.connect(Transitions[f"{model_id}\nClient Order"], Places[f"{model_id}\nClient"],
                      weight=client_demand)
    petri_net.connect(Places[f"{model_id}\nClient"], Transitions[f"{model_id}\nCreate Order"],
                      weight=1, inhibitor=True)
    petri_net.connect(Places[f"{model_id}\nClient"], Transitions[f"{model_id}\nSatisfied"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\nCreate Order"], Places[f"{model_id}\nOrder Requests"],
                      weight=1)
    petri_net.connect(Places[f"{model_id}\nOrder Requests"], Transitions[f"{model_id}\nClient Order"],
                      weight=1, priority=1)
    petri_net.connect(Places[f"{model_id}\nOrder Requests"], Transitions[f"{model_id}\nUnhappy"],
                      weight=1, priority=2)
    petri_net.connect(Transitions[f"{model_id}\nUnhappy"], Places[f"{model_id}\nUnhappy Clients"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\nSatisfied"], Places[f"{model_id}\nSatisfied Clients"],
                      weight=1)

    return petri_net
