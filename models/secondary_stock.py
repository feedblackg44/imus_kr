from PetriNet import Net, Place, Transition


def create_model(tickrate, model_id,
                 out_start_stock=100, income_start_stock=10, unloading_start_stock=60,
                 vendor_order_delay=5,
                 quality_control_probability=0.9, quality_control_speed=1,
                 cases_in_order=20,
                 inc_reorder_point=10, unloading_reorder_point=50, out_reorder_point=30,
                 inside_bandwidth=10, to_main_bandwidth=20
                 ):
    petri_net = Net(tickrate=tickrate)

    # Places
    Places = [
        Place(income_start_stock, f"{model_id}\tIncome Warehouse"),
        Place(0, f"{model_id}\tOrders to Vendor"),
        Place(0, f"{model_id}\tQuality Control"),
        Place(0, f"{model_id}\tBad Quality"),
        Place(unloading_start_stock, f"{model_id}\tUnloading Warehouse"),
        Place(out_start_stock, f"{model_id}\tOutgoing Warehouse")
    ]
    petri_net.add_places(Places)
    Places = {place.label: place for place in Places}

    # Transactions
    Transitions = [
        Transition(f"{model_id}\tVendor Order Request", delay=vendor_order_delay),
        Transition(f"{model_id}\tTo Quality Control"),
        Transition(f"{model_id}\tNot Enough Quality"),
        Transition(f"{model_id}\tEnough Quality"),
        Transition(f"{model_id}\tTo Export Warehouse"),
        Transition(f"{model_id}\tTo Main Warehouse")
    ]
    petri_net.add_transitions(Transitions)
    Transitions = {transition.label: transition for transition in Transitions}

    # Arcs
    petri_net.connect(Places[f"{model_id}\tIncome Warehouse"], Transitions[f"{model_id}\tVendor Order Request"],
                      weight=inc_reorder_point, inhibitor=True)
    petri_net.connect(Transitions[f"{model_id}\tVendor Order Request"], Places[f"{model_id}\tOrders to Vendor"],
                      weight=1)
    petri_net.connect(Places[f"{model_id}\tIncome Warehouse"], Transitions[f"{model_id}\tTo Quality Control"],
                      weight=quality_control_speed)
    petri_net.connect(Transitions[f"{model_id}\tTo Quality Control"], Places[f"{model_id}\tQuality Control"],
                      weight=quality_control_speed)
    petri_net.connect(Places[f"{model_id}\tQuality Control"], Transitions[f"{model_id}\tNot Enough Quality"],
                      weight=quality_control_speed,
                      probability=1-quality_control_probability)
    petri_net.connect(Places[f"{model_id}\tQuality Control"], Transitions[f"{model_id}\tEnough Quality"],
                      weight=quality_control_speed, probability=quality_control_probability)
    petri_net.connect(Transitions[f"{model_id}\tNot Enough Quality"], Places[f"{model_id}\tBad Quality"],
                      weight=quality_control_speed)
    petri_net.connect(Transitions[f"{model_id}\tEnough Quality"], Places[f"{model_id}\tUnloading Warehouse"],
                      weight=cases_in_order * quality_control_speed)
    petri_net.connect(Places[f"{model_id}\tUnloading Warehouse"], Transitions[f"{model_id}\tTo Quality Control"],
                      weight=unloading_reorder_point, inhibitor=True)
    petri_net.connect(Places[f"{model_id}\tUnloading Warehouse"], Transitions[f"{model_id}\tTo Export Warehouse"],
                      weight=inside_bandwidth, priority=1)
    petri_net.connect(Transitions[f"{model_id}\tTo Export Warehouse"], Places[f"{model_id}\tOutgoing Warehouse"],
                      weight=inside_bandwidth)
    petri_net.connect(Places[f"{model_id}\tOutgoing Warehouse"], Transitions[f"{model_id}\tTo Export Warehouse"],
                      weight=out_reorder_point, inhibitor=True)
    petri_net.connect(Places[f"{model_id}\tUnloading Warehouse"], Transitions[f"{model_id}\tTo Main Warehouse"],
                      weight=to_main_bandwidth, priority=2)

    return petri_net
