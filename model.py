from PetriNet import Net, Place, Transition


def create_model(tickrate):
    # Petri net
    petri_net = Net(tickrate=tickrate)

    # Places
    places = [
        Place(1, "vendor"),
        Place(5, "storage_reserve"),
        Place(4, "storage"),
        Place(0, "manager"),
        Place(1, "client_order"),
        Place(0, "client"),
        Place(0, "satisfied_client"),
        Place(0, "unhappy_client"),
    ]
    petri_net.add_places(places)
    places = {place.label: place for place in places}

    # Transactions
    transactions = [
        Transition("replenishment"),
        Transition("delivery"),
        Transition("sale", delay=1),
        Transition("satisfied"),
        Transition("unhappy", delay=1),
    ]
    petri_net.add_transitions(transactions)
    transactions = {transaction.label: transaction for transaction in transactions}

    # Arcs
    petri_net.connect(places["vendor"], transactions["replenishment"], weight=1)
    petri_net.connect(transactions["replenishment"], places["vendor"], weight=1)
    petri_net.connect(transactions["replenishment"], places["storage_reserve"], weight=1)
    petri_net.connect(places["storage_reserve"], transactions["delivery"], weight=1)
    petri_net.connect(transactions["delivery"], places["manager"], weight=1)
    petri_net.connect(places["manager"], transactions["replenishment"], weight=1)
    petri_net.connect(transactions["delivery"], places["storage"], weight=12)
    petri_net.connect(places["storage"], transactions["delivery"], weight=3, inhibitor=True)
    petri_net.connect(places["storage"], transactions["sale"], weight=2)
    petri_net.connect(transactions["sale"], places["client"], weight=2)
    petri_net.connect(places["client"], transactions["satisfied"], weight=2)
    petri_net.connect(transactions["satisfied"], places["satisfied_client"], weight=1)
    petri_net.connect(places["client_order"], transactions["sale"], weight=1, priority=2)
    petri_net.connect(transactions["sale"], places["client_order"], weight=1)
    petri_net.connect(places["client_order"], transactions["unhappy"], weight=1, priority=1)
    petri_net.connect(transactions["unhappy"], places["client_order"], weight=1)
    petri_net.connect(transactions["unhappy"], places["unhappy_client"], weight=1)

    return petri_net
