from PetriNet import Net, Place, Transition


def create_model(tickrate):
    # Petri net
    petri_net = Net(tickrate=tickrate)

    # Places
    places = [
        Place(1, "Vendor"),
        Place(5, "Storage Reserve"),
        Place(4, "Storage"),
        Place(0, "Manager"),
        Place(1, "Client Order"),
        Place(0, "Client"),
        Place(0, "Satisfied Client"),
        Place(0, "Unhappy Client"),
    ]
    petri_net.add_places(places)
    places = {place.label: place for place in places}

    # Transactions
    transactions = [
        Transition("Replenishment"),
        Transition("Delivery"),
        Transition("Sale", delay=1),
        Transition("Satisfied"),
        Transition("Unhappy", delay=1),
    ]
    petri_net.add_transitions(transactions)
    transactions = {transaction.label: transaction for transaction in transactions}

    # Arcs
    petri_net.connect(places["Vendor"], transactions["Replenishment"], weight=1)
    petri_net.connect(transactions["Replenishment"], places["Vendor"], weight=1)
    petri_net.connect(transactions["Replenishment"], places["Storage Reserve"], weight=1)
    petri_net.connect(places["Storage Reserve"], transactions["Delivery"], weight=1)
    petri_net.connect(transactions["Delivery"], places["Manager"], weight=1)
    petri_net.connect(places["Manager"], transactions["Replenishment"], weight=1)
    petri_net.connect(transactions["Delivery"], places["Storage"], weight=12)
    petri_net.connect(places["Storage"], transactions["Delivery"], weight=3, inhibitor=True)
    petri_net.connect(places["Storage"], transactions["Sale"], weight=2)
    petri_net.connect(transactions["Sale"], places["Client"], weight=2)
    petri_net.connect(places["Client"], transactions["Satisfied"], weight=2)
    petri_net.connect(transactions["Satisfied"], places["Satisfied Client"], weight=1)
    petri_net.connect(places["Client Order"], transactions["Sale"], weight=1, priority=1)
    petri_net.connect(transactions["Sale"], places["Client Order"], weight=1)
    petri_net.connect(places["Client Order"], transactions["Unhappy"], weight=1, priority=2)
    petri_net.connect(transactions["Unhappy"], places["Client Order"], weight=1)
    petri_net.connect(transactions["Unhappy"], places["Unhappy Client"], weight=1)

    return petri_net
