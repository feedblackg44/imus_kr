from PetriNet import Net


def connect_nets(net1, net2, connections):
    if not isinstance(connections, list):
        connections = [connections]
    if net1.tickrate != net2.tickrate:
        raise Exception("Cannot connect nets with different tickrates")
    new_net = Net(net1.tickrate)

    new_net.add_places(net1.places)
    new_net.add_places(net2.places)

    new_net.add_transitions(net1.transitions)
    new_net.add_transitions(net2.transitions)

    for connection in connections[0]:
        if connection[0] == "place":
            new_net.connect(net1.find_place_by_label(connection[1]),
                            net2.find_transition_by_label(connection[2]),
                            **connection[3])
        elif connection[0] == "transition":
            new_net.connect(net1.find_transition_by_label(connection[1]),
                            net2.find_place_by_label(connection[2]),
                            **connection[3])
        else:
            raise Exception("Invalid connection type")

    for connection in connections[1]:
        if connection[0] == "place":
            new_net.connect(net2.find_place_by_label(connection[1]),
                            net1.find_transition_by_label(connection[2]),
                            **connection[3])
        elif connection[0] == "transition":
            new_net.connect(net2.find_transition_by_label(connection[1]),
                            net1.find_place_by_label(connection[2]),
                            **connection[3])
        else:
            raise Exception("Invalid connection type")

    return new_net
