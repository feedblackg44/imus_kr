from PetriNet import Net, Place, Transition


def create_model(tickrate, model_id, start_stock=100):
    petri_net = Net(tickrate=tickrate)

    # Places
    Places = [
        Place(10, f"{model_id}\nIncome Warehouse"),
        Place(0, f"{model_id}\nOrders to Vendor"),
        Place(0, f"{model_id}\nQuality Control North"),
        Place(0, f"{model_id}\nQuality Control South"),
        Place(0, f"{model_id}\nBad Quality 1"),
        Place(0, f"{model_id}\nBad Quality 2"),
        Place(100, f"{model_id}\nUnloading Warehouse"),
        Place(0, f"{model_id}\nBuffer Warehouse North"),
        Place(0, f"{model_id}\nBuffer Warehouse South"),
        Place(0, f"{model_id}\nOrders to North"),
        Place(0, f"{model_id}\nOrders to South"),
        Place(start_stock, f"{model_id}\nOutgoing Warehouse")
    ]
    petri_net.add_places(Places)
    Places = {place.label: place for place in Places}

    # Transactions
    Transitions = [
        Transition(f"{model_id}\nVendor Order Request", delay=5),
        Transition(f"{model_id}\nTo Quality Control"),
        Transition(f"{model_id}\nNot Enough Quality North"),
        Transition(f"{model_id}\nNot Enough Quality South"),
        Transition(f"{model_id}\nEnough Quality North"),
        Transition(f"{model_id}\nEnough Quality South"),
        Transition(f"{model_id}\nFrom North Warehouse"),
        Transition(f"{model_id}\nFrom South Warehouse"),
        Transition(f"{model_id}\nRequest North Warehouse"),
        Transition(f"{model_id}\nRequest South Warehouse"),
        Transition(f"{model_id}\nTo Export Warehouse")
    ]
    petri_net.add_transitions(Transitions)
    Transitions = {transition.label: transition for transition in Transitions}

    # Arcs
    petri_net.connect(Transitions[f"{model_id}\nVendor Order Request"], Places[f"{model_id}\nOrders to Vendor"],
                      weight=1)
    petri_net.connect(Places[f"{model_id}\nIncome Warehouse"], Transitions[f"{model_id}\nTo Quality Control"],
                      weight=1)
    petri_net.connect(Places[f"{model_id}\nIncome Warehouse"], Transitions[f"{model_id}\nVendor Order Request"],
                      weight=10, inhibitor=True)
    petri_net.connect(Transitions[f"{model_id}\nTo Quality Control"], Places[f"{model_id}\nQuality Control North"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\nTo Quality Control"], Places[f"{model_id}\nQuality Control South"],
                      weight=1)
    petri_net.connect(Places[f"{model_id}\nQuality Control North"], Transitions[f"{model_id}\nNot Enough Quality North"],
                      weight=1, probability=0.1)
    petri_net.connect(Places[f"{model_id}\nQuality Control South"], Transitions[f"{model_id}\nNot Enough Quality South"],
                      weight=1, probability=0.1)
    petri_net.connect(Places[f"{model_id}\nQuality Control North"], Transitions[f"{model_id}\nEnough Quality North"],
                      weight=1, probability=0.9)
    petri_net.connect(Places[f"{model_id}\nQuality Control South"], Transitions[f"{model_id}\nEnough Quality South"],
                      weight=1, probability=0.9)
    petri_net.connect(Transitions[f"{model_id}\nNot Enough Quality North"], Places[f"{model_id}\nBad Quality 1"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\nNot Enough Quality South"], Places[f"{model_id}\nBad Quality 2"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\nEnough Quality North"], Places[f"{model_id}\nUnloading Warehouse"],
                      weight=20)
    petri_net.connect(Transitions[f"{model_id}\nEnough Quality South"], Places[f"{model_id}\nUnloading Warehouse"],
                      weight=20)
    petri_net.connect(Places[f"{model_id}\nUnloading Warehouse"], Transitions[f"{model_id}\nTo Quality Control"],
                      weight=100, inhibitor=True, priority=1)
    petri_net.connect(Places[f"{model_id}\nUnloading Warehouse"], Transitions[f"{model_id}\nTo Export Warehouse"],
                      weight=20)
    petri_net.connect(Transitions[f"{model_id}\nTo Export Warehouse"], Places[f"{model_id}\nOutgoing Warehouse"],
                      weight=20)
    petri_net.connect(Places[f"{model_id}\nOutgoing Warehouse"], Transitions[f"{model_id}\nTo Export Warehouse"],
                      weight=50, inhibitor=True)
    petri_net.connect(Places[f"{model_id}\nBuffer Warehouse North"], Transitions[f"{model_id}\nFrom North Warehouse"],
                      weight=20)
    petri_net.connect(Places[f"{model_id}\nBuffer Warehouse South"], Transitions[f"{model_id}\nFrom South Warehouse"],
                      weight=20)
    petri_net.connect(Transitions[f"{model_id}\nFrom North Warehouse"], Places[f"{model_id}\nUnloading Warehouse"],
                      weight=20)
    petri_net.connect(Transitions[f"{model_id}\nFrom South Warehouse"], Places[f"{model_id}\nUnloading Warehouse"],
                      weight=20)
    petri_net.connect(Places[f"{model_id}\nUnloading Warehouse"], Transitions[f"{model_id}\nRequest North Warehouse"],
                      weight=20, inhibitor=True, priority=2)
    petri_net.connect(Places[f"{model_id}\nUnloading Warehouse"], Transitions[f"{model_id}\nRequest South Warehouse"],
                      weight=20, inhibitor=True, priority=3)
    petri_net.connect(Transitions[f"{model_id}\nRequest North Warehouse"], Places[f"{model_id}\nOrders to North"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\nRequest South Warehouse"], Places[f"{model_id}\nOrders to South"],
                      weight=1)

    return petri_net
