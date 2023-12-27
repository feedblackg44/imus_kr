import matplotlib

from model import create_model


def main():
    matplotlib.use("TkAgg")
    tickrate = 1

    petri_net = create_model(tickrate)

    petri_net.simulate(10, draw=True)


if __name__ == "__main__":
    main()
