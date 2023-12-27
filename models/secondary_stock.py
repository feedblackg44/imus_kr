from PetriNet import Net, Place, Transition


def create_model(tickrate, model_id, start_stock=100):
    petri_net = Net(tickrate=tickrate)

    # Places
    Places = [
        Place(0, f"{model_id}\nIncome Warehouse"),
        Place(0, f"{model_id}\nOrders to Vendor"),
        Place(0, f"{model_id}\nQuality Control"),
        Place(0, f"{model_id}\nBad Quality"),
        Place(0, f"{model_id}\nUnloading Warehouse"),
        Place(start_stock, f"{model_id}\nOutgoing Warehouse")
    ]
    petri_net.add_places(Places)
    Places = {place.label: place for place in Places}

    # Transactions
    Transitions = [
        Transition(f"{model_id}\nVendor Order Request"),
        Transition(f"{model_id}\nTo Quality Control"),
        Transition(f"{model_id}\nNot Enough Quality"),
        Transition(f"{model_id}\nEnough Quality"),
        Transition(f"{model_id}\nTo Export Warehouse"),
        Transition(f"{model_id}\nTo Main Warehouse")
    ]
    petri_net.add_transitions(Transitions)
    Transitions = {transition.label: transition for transition in Transitions}

    # Arcs
    petri_net.connect(Places[f"{model_id}\nIncome Warehouse"], Transitions[f"{model_id}\nVendor Order Request"],
                      weight=10, inhibitor=True)
    petri_net.connect(Transitions[f"{model_id}\nVendor Order Request"], Places[f"{model_id}\nOrders to Vendor"],
                      weight=1)
    petri_net.connect(Places[f"{model_id}\nIncome Warehouse"], Transitions[f"{model_id}\nTo Quality Control"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\nTo Quality Control"], Places[f"{model_id}\nQuality Control"],
                      weight=1)
    petri_net.connect(Places[f"{model_id}\nQuality Control"], Transitions[f"{model_id}\nNot Enough Quality"],
                      weight=1,
                      probability=0.1)
    petri_net.connect(Places[f"{model_id}\nQuality Control"], Transitions[f"{model_id}\nEnough Quality"],
                      weight=1, probability=0.9)
    petri_net.connect(Transitions[f"{model_id}\nNot Enough Quality"], Places[f"{model_id}\nBad Quality"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\nEnough Quality"], Places[f"{model_id}\nUnloading Warehouse"],
                      weight=20)
    petri_net.connect(Places[f"{model_id}\nUnloading Warehouse"], Transitions[f"{model_id}\nTo Quality Control"],
                      weight=100, inhibitor=True)
    petri_net.connect(Places[f"{model_id}\nUnloading Warehouse"], Transitions[f"{model_id}\nTo Export Warehouse"],
                      weight=10, priority=2)
    petri_net.connect(Transitions[f"{model_id}\nTo Export Warehouse"], Places[f"{model_id}\nOutgoing Warehouse"],
                      weight=10)
    petri_net.connect(Places[f"{model_id}\nOutgoing Warehouse"], Transitions[f"{model_id}\nTo Export Warehouse"],
                      weight=30, inhibitor=True)
    petri_net.connect(Places[f"{model_id}\nUnloading Warehouse"], Transitions[f"{model_id}\nTo Main Warehouse"],
                      weight=20, priority=1)

    return petri_net
