from PetriNet import Net, Place, Transition


def create_model(tickrate, model_id,
                 out_start_stock=100, income_start_stock=10, unloading_start_stock=100,
                 vendor_order_delay=5,
                 quality_control_probability=0.9, quality_control_speed=1,
                 cases_in_order=20,
                 inc_reorder_point=10, unloading_reorder_point=50, out_reorder_point=30,
                 south_reorder_point=20, north_reorder_point=20,
                 inside_bandwidth=20, to_main_bandwidth=20
                 ):
    petri_net = Net(tickrate=tickrate)

    # Places
    Places = [
        Place(income_start_stock, f"{model_id}\tIncome Warehouse"),
        Place(0, f"{model_id}\tOrders to Vendor"),
        Place(0, f"{model_id}\tQuality Control North"),
        Place(0, f"{model_id}\tQuality Control South"),
        Place(0, f"{model_id}\tBad Quality 1"),
        Place(0, f"{model_id}\tBad Quality 2"),
        Place(out_start_stock, f"{model_id}\tUnloading Warehouse"),
        Place(0, f"{model_id}\tBuffer Warehouse North"),
        Place(0, f"{model_id}\tBuffer Warehouse South"),
        Place(0, f"{model_id}\tOrders to North"),
        Place(0, f"{model_id}\tOrders to South"),
        Place(unloading_start_stock, f"{model_id}\tOutgoing Warehouse")
    ]
    petri_net.add_places(Places)
    Places = {place.label: place for place in Places}

    # Transactions
    Transitions = [
        Transition(f"{model_id}\tVendor Order Request", delay=vendor_order_delay),
        Transition(f"{model_id}\tTo Quality Control"),
        Transition(f"{model_id}\tNot Enough Quality North"),
        Transition(f"{model_id}\tNot Enough Quality South"),
        Transition(f"{model_id}\tEnough Quality North"),
        Transition(f"{model_id}\tEnough Quality South"),
        Transition(f"{model_id}\tFrom North Warehouse"),
        Transition(f"{model_id}\tFrom South Warehouse"),
        Transition(f"{model_id}\tRequest North Warehouse"),
        Transition(f"{model_id}\tRequest South Warehouse"),
        Transition(f"{model_id}\tTo Export Warehouse")
    ]
    petri_net.add_transitions(Transitions)
    Transitions = {transition.label: transition for transition in Transitions}

    # Arcs
    petri_net.connect(Transitions[f"{model_id}\tVendor Order Request"], Places[f"{model_id}\tOrders to Vendor"],
                      weight=1)
    petri_net.connect(Places[f"{model_id}\tIncome Warehouse"], Transitions[f"{model_id}\tTo Quality Control"],
                      weight=quality_control_speed)
    petri_net.connect(Places[f"{model_id}\tIncome Warehouse"], Transitions[f"{model_id}\tVendor Order Request"],
                      weight=inc_reorder_point, inhibitor=True)
    petri_net.connect(Transitions[f"{model_id}\tTo Quality Control"], Places[f"{model_id}\tQuality Control North"],
                      weight=quality_control_speed)
    petri_net.connect(Transitions[f"{model_id}\tTo Quality Control"], Places[f"{model_id}\tQuality Control South"],
                      weight=quality_control_speed)
    petri_net.connect(Places[f"{model_id}\tQuality Control North"], Transitions[f"{model_id}\tNot Enough Quality North"]
                      , weight=quality_control_speed, probability=1-quality_control_probability)
    petri_net.connect(Places[f"{model_id}\tQuality Control South"], Transitions[f"{model_id}\tNot Enough Quality South"]
                      , weight=quality_control_speed, probability=1-quality_control_probability)
    petri_net.connect(Places[f"{model_id}\tQuality Control North"], Transitions[f"{model_id}\tEnough Quality North"],
                      weight=quality_control_speed, probability=quality_control_probability)
    petri_net.connect(Places[f"{model_id}\tQuality Control South"], Transitions[f"{model_id}\tEnough Quality South"],
                      weight=quality_control_speed, probability=quality_control_probability)
    petri_net.connect(Transitions[f"{model_id}\tNot Enough Quality North"], Places[f"{model_id}\tBad Quality 1"],
                      weight=quality_control_speed)
    petri_net.connect(Transitions[f"{model_id}\tNot Enough Quality South"], Places[f"{model_id}\tBad Quality 2"],
                      weight=quality_control_speed)
    petri_net.connect(Transitions[f"{model_id}\tEnough Quality North"], Places[f"{model_id}\tUnloading Warehouse"],
                      weight=cases_in_order * quality_control_speed)
    petri_net.connect(Transitions[f"{model_id}\tEnough Quality South"], Places[f"{model_id}\tUnloading Warehouse"],
                      weight=cases_in_order * quality_control_speed)
    petri_net.connect(Places[f"{model_id}\tUnloading Warehouse"], Transitions[f"{model_id}\tTo Quality Control"],
                      weight=unloading_reorder_point, inhibitor=True, priority=1)
    petri_net.connect(Places[f"{model_id}\tUnloading Warehouse"], Transitions[f"{model_id}\tTo Export Warehouse"],
                      weight=inside_bandwidth)
    petri_net.connect(Transitions[f"{model_id}\tTo Export Warehouse"], Places[f"{model_id}\tOutgoing Warehouse"],
                      weight=inside_bandwidth)
    petri_net.connect(Places[f"{model_id}\tOutgoing Warehouse"], Transitions[f"{model_id}\tTo Export Warehouse"],
                      weight=out_reorder_point, inhibitor=True)
    petri_net.connect(Places[f"{model_id}\tBuffer Warehouse North"], Transitions[f"{model_id}\tFrom North Warehouse"],
                      weight=to_main_bandwidth)
    petri_net.connect(Places[f"{model_id}\tBuffer Warehouse South"], Transitions[f"{model_id}\tFrom South Warehouse"],
                      weight=to_main_bandwidth)
    petri_net.connect(Transitions[f"{model_id}\tFrom North Warehouse"], Places[f"{model_id}\tUnloading Warehouse"],
                      weight=to_main_bandwidth)
    petri_net.connect(Transitions[f"{model_id}\tFrom South Warehouse"], Places[f"{model_id}\tUnloading Warehouse"],
                      weight=to_main_bandwidth)
    petri_net.connect(Places[f"{model_id}\tUnloading Warehouse"], Transitions[f"{model_id}\tRequest North Warehouse"],
                      weight=north_reorder_point, inhibitor=True, priority=2)
    petri_net.connect(Places[f"{model_id}\tUnloading Warehouse"], Transitions[f"{model_id}\tRequest South Warehouse"],
                      weight=south_reorder_point, inhibitor=True, priority=3)
    petri_net.connect(Transitions[f"{model_id}\tRequest North Warehouse"], Places[f"{model_id}\tOrders to North"],
                      weight=1)
    petri_net.connect(Transitions[f"{model_id}\tRequest South Warehouse"], Places[f"{model_id}\tOrders to South"],
                      weight=1)

    return petri_net
