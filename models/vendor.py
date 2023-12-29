from PetriNet import Net, Place, Transition


def create_model(tickrate, model_id,
                 confiscation_probability=0.2,
                 customs_delay=3
                 ):
    petri_net = Net(tickrate=tickrate)

    # Places
    Places = [
        Place(1, f"{model_id}\tVendor"),
        Place(0, f"{model_id}\tCustoms"),
        Place(0, f"{model_id}\tConfiscated"),
        Place(0, f"{model_id}\tFor Export"),
        Place(0, f"{model_id}\tOrders")
    ]
    petri_net.add_places(Places)
    Places = {place.label: place for place in Places}

    # Transactions
    Transitions = [
        Transition(f"{model_id}\tExport for Customs", delay=customs_delay),
        Transition(f"{model_id}\tCustoms Failed"),
        Transition(f"{model_id}\tCustoms Passed"),
        Transition(f"{model_id}\tExport"),
        Transition(f"{model_id}\tOrder")
    ]
    petri_net.add_transitions(Transitions)
    Transitions = {transition.label: transition for transition in Transitions}

    # Arcs
    petri_net.connect(Places[f"{model_id}\tVendor"], Transitions[f"{model_id}\tExport for Customs"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\tExport for Customs"], Places[f"{model_id}\tVendor"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\tExport for Customs"], Places[f"{model_id}\tCustoms"],
                      weight=1)
    petri_net.connect(Places[f"{model_id}\tCustoms"], Transitions[f"{model_id}\tCustoms Failed"],
                      weight=1, probability=confiscation_probability)
    petri_net.connect(Places[f"{model_id}\tCustoms"], Transitions[f"{model_id}\tCustoms Passed"],
                      weight=1, probability=1-confiscation_probability)
    petri_net.connect(Transitions[f"{model_id}\tCustoms Failed"], Places[f"{model_id}\tConfiscated"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\tCustoms Passed"], Places[f"{model_id}\tFor Export"],
                      weight=1)
    petri_net.connect(Places[f"{model_id}\tFor Export"], Transitions[f"{model_id}\tExport"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\tOrder"], Places[f"{model_id}\tOrders"], 
                      weight=1)
    petri_net.connect(Places[f"{model_id}\tOrders"], Transitions[f"{model_id}\tExport for Customs"],
                      weight=1)

    return petri_net
