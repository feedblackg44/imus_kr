from models import create_client, create_vendor, create_central_stock, create_secondary_stock
from utils import connect_nets


def create_model(tickrate=10):
    clients_north = [create_client(tickrate, f"north{i}") for i in range(2)]
    clients_south = [create_client(tickrate, f"south{i}") for i in range(3)]
    clients_central = [create_client(tickrate, f"central{i}") for i in range(5)]
    vendor_north = create_vendor(tickrate, "north")
    vendor_south = create_vendor(tickrate, "south")
    vendor_central = create_vendor(tickrate, "central")
    north_stock = create_secondary_stock(tickrate, "north")
    south_stock = create_secondary_stock(tickrate, "south")
    central_stock_model = create_central_stock(tickrate, "central")

    north_net = connect_nets(vendor_north, north_stock, [
        [["transition", "north\nExport", "north\nIncome Warehouse", {"weight": 10}]],
        [["place", "north\nOrders to Vendor", "north\nOrder", {"weight": 1}]],
    ])
    for i, client in enumerate(clients_north):
        north_net = connect_nets(north_net, client, [
            [["place", f"north\nOutgoing Warehouse", f"north{i}\nClient Order",
              {"weight": 5, "probability": 0.5}]],
            []
        ])

    south_net = connect_nets(vendor_south, south_stock, [
        [["transition", "south\nExport", "south\nIncome Warehouse", {"weight": 10}]],
        [["place", "south\nOrders to Vendor", "south\nOrder", {"weight": 1}]],
    ])
    for i, client in enumerate(clients_south):
        south_net = connect_nets(south_net, client, [
            [["place", f"south\nOutgoing Warehouse", f"south{i}\nClient Order",
              {"weight": 5, "probability": 0.33}]],
            []
        ])

    central_net = connect_nets(vendor_central, central_stock_model, [
        [["transition", "central\nExport", "central\nIncome Warehouse", {"weight": 10}]],
        [["place", "central\nOrders to Vendor", "central\nOrder", {"weight": 1}]],
    ])
    for i, client in enumerate(clients_central):
        central_net = connect_nets(central_net, client, [
            [["place", f"central\nOutgoing Warehouse", f"central{i}\nClient Order",
              {"weight": 5, "probability": 0.2}]],
            []
        ])

    north_central_net = connect_nets(north_net, central_net, [
        [["transition", "north\nTo Main Warehouse", "central\nBuffer Warehouse North", {"weight": 20}]],
        [["place", "central\nOrders to North", "north\nTo Main Warehouse", {"weight": 1}]]
    ])

    completed_net = connect_nets(south_net, north_central_net, [
        [["transition", "south\nTo Main Warehouse", "central\nBuffer Warehouse South", {"weight": 20}]],
        [["place", "central\nOrders to South", "south\nTo Main Warehouse", {"weight": 1}]]
    ])

    return completed_net
