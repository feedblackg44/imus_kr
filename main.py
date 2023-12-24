import matplotlib

from PetriNet import Net, Place, Transition


def main():
    matplotlib.use("TkAgg")

    petri_net = Net()

    places = [
        Place(1, "p1"),
        Place(15, "p2"),
        Place(0, "p3"),
        Place(0, "p4"),
        Place(0, "p5"),
        Place(0, "p6"),
        Place(1, "p7")
    ]

    transactions = [
        Transition("t1"),
        Transition("t2"),
        Transition("t3"),
        Transition("t4"),
        Transition("t6")
    ]

    petri_net.add_places(places)
    petri_net.add_transitions(transactions)

    petri_net.connect(places[0], transactions[0])
    petri_net.connect(transactions[0], places[0])
    petri_net.connect(transactions[0], places[1], 12)
    petri_net.connect(places[1], transactions[1], 2)
    petri_net.connect(places[1], transactions[2])
    petri_net.connect(transactions[2], places[1])
    petri_net.connect(places[2], transactions[0], 6)
    petri_net.connect(transactions[2], places[2], 1)
    petri_net.connect(transactions[1], places[3], 2)
    petri_net.connect(places[3], transactions[3], 2)
    petri_net.connect(transactions[3], places[4])
    petri_net.connect(transactions[4], places[5])
    petri_net.connect(places[6], transactions[1])
    petri_net.connect(transactions[1], places[6])
    petri_net.connect(places[6], transactions[4])
    petri_net.connect(transactions[4], places[6])

    petri_net.simulate(50, draw=True)


if __name__ == "__main__":
    main()
