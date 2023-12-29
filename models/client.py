from PetriNet import Net, Place, Transition


def create_model(tickrate, model_id,
                 order_probability=0.5,
                 client_demand=5
                 ):
    petri_net = Net(tickrate=tickrate)

    # Places
    Places = [
        Place(0, f"{model_id}\tClient"),
        Place(0, f"{model_id}\tOrder Requests"),
        Place(0, f"{model_id}\tSatisfied Clients"),
        Place(0, f"{model_id}\tUnhappy Clients")
    ]
    petri_net.add_places(Places)
    Places = {place.label: place for place in Places}

    # Transactions
    Transitions = [
        Transition(f"{model_id}\tClient Order"),
        Transition(f"{model_id}\tCreate Order", delay=order_probability),
        Transition(f"{model_id}\tSatisfied"),
        Transition(f"{model_id}\tUnhappy")
    ]
    petri_net.add_transitions(Transitions)
    Transitions = {transition.label: transition for transition in Transitions}

    # Arcs
    petri_net.connect(Transitions[f"{model_id}\tClient Order"], Places[f"{model_id}\tClient"],
                      weight=client_demand)
    petri_net.connect(Places[f"{model_id}\tClient"], Transitions[f"{model_id}\tCreate Order"],
                      weight=1, inhibitor=True)
    petri_net.connect(Places[f"{model_id}\tClient"], Transitions[f"{model_id}\tSatisfied"],
                      weight=client_demand)
    petri_net.connect(Transitions[f"{model_id}\tCreate Order"], Places[f"{model_id}\tOrder Requests"],
                      weight=1)
    petri_net.connect(Places[f"{model_id}\tOrder Requests"], Transitions[f"{model_id}\tClient Order"],
                      weight=1, priority=1)
    petri_net.connect(Places[f"{model_id}\tOrder Requests"], Transitions[f"{model_id}\tUnhappy"],
                      weight=1, priority=2)
    petri_net.connect(Transitions[f"{model_id}\tUnhappy"], Places[f"{model_id}\tUnhappy Clients"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\tSatisfied"], Places[f"{model_id}\tSatisfied Clients"],
                      weight=1)

    return petri_net
