from PetriNet import Net, Place, Transition


def create_model(tickrate, model_id):
    petri_net = Net(tickrate=tickrate)

    # Places
    Places = [
        Place(1, f"{model_id}\nVendor"),
        Place(0, f"{model_id}\nCustoms"),
        Place(0, f"{model_id}\nConfiscated"),
        Place(0, f"{model_id}\nFor Export"),
        Place(0, f"{model_id}\nOrders")
    ]
    petri_net.add_places(Places)
    Places = {place.label: place for place in Places}

    # Transactions
    Transitions = [
        Transition(f"{model_id}\nExport for Customs", delay=1),
        Transition(f"{model_id}\nCustoms Failed"),
        Transition(f"{model_id}\nCustoms Passed"),
        Transition(f"{model_id}\nExport"),
        Transition(f"{model_id}\nOrder")
    ]
    petri_net.add_transitions(Transitions)
    Transitions = {transition.label: transition for transition in Transitions}

    # Arcs
    petri_net.connect(Places[f"{model_id}\nVendor"], Transitions[f"{model_id}\nExport for Customs"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\nExport for Customs"], Places[f"{model_id}\nVendor"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\nExport for Customs"], Places[f"{model_id}\nCustoms"],
                      weight=1)
    petri_net.connect(Places[f"{model_id}\nCustoms"], Transitions[f"{model_id}\nCustoms Failed"],
                      weight=1, probability=0.2)
    petri_net.connect(Places[f"{model_id}\nCustoms"], Transitions[f"{model_id}\nCustoms Passed"],
                      weight=1, probability=0.8)
    petri_net.connect(Transitions[f"{model_id}\nCustoms Failed"], Places[f"{model_id}\nConfiscated"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\nCustoms Passed"], Places[f"{model_id}\nFor Export"],
                      weight=1)
    petri_net.connect(Places[f"{model_id}\nFor Export"], Transitions[f"{model_id}\nExport"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\nOrder"], Places[f"{model_id}\nOrders"], 
                      weight=1)
    petri_net.connect(Places[f"{model_id}\nOrders"], Transitions[f"{model_id}\nExport for Customs"],
                      weight=1)

    return petri_net
