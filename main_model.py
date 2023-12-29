from models import create_client, create_vendor, create_central_stock, create_secondary_stock
from utils import connect_nets


def create_model(tickrate, clients, vendors, central_stock, secondary_stocks, trucks, clients_amounts):
    if not clients_amounts:
        clients_amounts = {
            "north": 2,
            "south": 3,
            "central": 5
        }
    if not trucks:
        trucks = {
            "north": 10,
            "south": 10,
            "central": 10
        }

    clients_north = [create_client(tickrate, f"north{i}", **clients['north'])
                     for i in range(clients_amounts['north'])]
    clients_south = [create_client(tickrate, f"south{i}", **clients['south'])
                     for i in range(clients_amounts['south'])]
    clients_central = [create_client(tickrate, f"central{i}", **clients['central'])
                       for i in range(clients_amounts['central'])]
    vendor_north = create_vendor(tickrate, "north", **vendors['north'])
    vendor_south = create_vendor(tickrate, "south", **vendors['south'])
    vendor_central = create_vendor(tickrate, "central", **vendors['central'])
    north_stock = create_secondary_stock(tickrate, "north", **secondary_stocks['north'])
    south_stock = create_secondary_stock(tickrate, "south", **secondary_stocks['south'])
    central_stock_model = create_central_stock(tickrate, "central", **central_stock)

    north_net = connect_nets(vendor_north, north_stock, [
        [["transition", "north\tExport", "north\tIncome Warehouse", {"weight": trucks['north']}]],
        [["place", "north\tOrders to Vendor", "north\tOrder", {"weight": 1}]],
    ])
    for i, client in enumerate(clients_north):
        north_net = connect_nets(north_net, client, [
            [["place", f"north\tOutgoing Warehouse", f"north{i}\tClient Order",
              {"weight": clients['north']['client_demand'], "probability": 1 / len(clients_north)}]],
            []
        ])

    south_net = connect_nets(vendor_south, south_stock, [
        [["transition", "south\tExport", "south\tIncome Warehouse", {"weight": trucks['south']}]],
        [["place", "south\tOrders to Vendor", "south\tOrder", {"weight": 1}]],
    ])
    for i, client in enumerate(clients_south):
        south_net = connect_nets(south_net, client, [
            [["place", f"south\tOutgoing Warehouse", f"south{i}\tClient Order",
              {"weight": clients['south']['client_demand'], "probability": 1 / len(clients_south)}]],
            []
        ])

    central_net = connect_nets(vendor_central, central_stock_model, [
        [["transition", "central\tExport", "central\tIncome Warehouse", {"weight": trucks['central']}]],
        [["place", "central\tOrders to Vendor", "central\tOrder", {"weight": 1}]],
    ])
    for i, client in enumerate(clients_central):
        central_net = connect_nets(central_net, client, [
            [["place", f"central\tOutgoing Warehouse", f"central{i}\tClient Order",
              {"weight": clients['central']['client_demand'], "probability": 1 / len(clients_central)}]],
            []
        ])

    north_central_net = connect_nets(north_net, central_net, [
        [["transition", "north\tTo Main Warehouse", "central\tBuffer Warehouse North",
          {"weight": secondary_stocks['north']['to_main_bandwidth']}]],
        [["place", "central\tOrders to North", "north\tTo Main Warehouse", {"weight": 1}]]
    ])

    completed_net = connect_nets(south_net, north_central_net, [
        [["transition", "south\tTo Main Warehouse", "central\tBuffer Warehouse South",
          {"weight": secondary_stocks['south']['to_main_bandwidth']}]],
        [["place", "central\tOrders to South", "south\tTo Main Warehouse", {"weight": 1}]]
    ])

    return completed_net
