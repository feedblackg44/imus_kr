import matplotlib

from main_model import create_model as create_main_model


def main():
    matplotlib.use("TkAgg")
    tickrate = 100

    petri_net = create_main_model(tickrate)

    petri_net.simulate(1000, draw=False)
    petri_net.draw_viz()


if __name__ == "__main__":
    main()
