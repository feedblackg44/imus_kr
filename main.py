import datetime
import json
import math
import random

import matplotlib.pyplot as plt

from main_model import create_model as create_main_model


def main():
    tickrate = 100

    with open("model_settings.json", "r") as f:
        model_settings = json.load(f)

    # Z_arr = [[] for _ in range(10)]
    # for i in range(10):
    #     model_settings['central_stock']['out_reorder_point'] = random.randint(1, 60)
    #     model_settings['secondary_stocks']['north']['out_reorder_point'] = random.randint(1, 60)
    #     model_settings['secondary_stocks']['south']['out_reorder_point'] = random.randint(1, 60)
    #     petri_net = create_main_model(tickrate, **model_settings)
    #     for _ in range(1, 1001):
    #         petri_net.simulate(1, draw=False)
    #         # petri_net.draw_viz()
    #
    #         satisfied_clients = petri_net.get_satisfied_clients()
    #         unhappy_clients = petri_net.get_unsatisfied_clients()
    #         max_tokens = petri_net.max_tokens
    #
    #         W1 = satisfied_clients + unhappy_clients
    #         W2 = unhappy_clients
    #         W3 = max_tokens['income']
    #         W4 = max_tokens['unloading']
    #         W5 = max_tokens['outgoing']
    #
    #         # print(f"Кількість клієнтів W1: {W1}")
    #         # print(f"Кількість незадоволених клієнтів W2: {W2}")
    #         # print(f"Максимальна кількість товарів в зонах прибуття W3: {W3}")
    #         # print(f"Максимальна кількість товарів в зонах розвантаження W4: {W4}")
    #         # print(f"Максимальна кількість товарів в зонах відправки W5: {W5}")
    #
    #         Z = W2 + sum([W3[key] for key in W3]) + sum([W4[key] for key in W4]) + sum([W5[key] for key in W5])
    #
    #         print(f"Цільова функція Z: {Z}")
    #
    #         Z_arr[i].append(Z)
    #
    # x = [i for i in range(1, 1001)]
    # for i in range(10):
    #     plt.plot(x, Z_arr[i])
    # plt.xlabel("Час")
    # plt.ylabel("Значення цільової функції")
    # plt.show()

    # Z_arr = []
    # for i in range(100):
    #     petri_net = create_main_model(tickrate, **model_settings)
    #
    #     petri_net.simulate(200, draw=False)
    #     # petri_net.draw_viz()
    #
    #     satisfied_clients = petri_net.get_satisfied_clients()
    #     unhappy_clients = petri_net.get_unsatisfied_clients()
    #     max_tokens = petri_net.max_tokens
    #
    #     W1 = satisfied_clients + unhappy_clients
    #     W2 = unhappy_clients
    #     W3 = max_tokens['income']
    #     W4 = max_tokens['unloading']
    #     W5 = max_tokens['outgoing']
    #
    #     Z = W2 + sum([W3[key] for key in W3]) + sum([W4[key] for key in W4]) + sum([W5[key] for key in W5])
    #
    #     print(f"{i}. Цільова функція Z: {Z}")
    #
    #     Z_arr.append(Z)
    #
    # Z_mean = sum(Z_arr) / len(Z_arr)
    # epsilon = Z_mean * 0.05
    # Z_dispersion = sum([(Z - Z_mean) ** 2 for Z in Z_arr]) / len(Z_arr)
    #
    # print(f"Середнє значення Z: {Z_mean}")
    # print(f"Епсілон: {epsilon}")
    # print(f"Дисперсія Z: {Z_dispersion}")

    Z_arr = []
    params_arr = []
    W_arr = []
    time_now = datetime.datetime.now()
    p = 100
    for j in range(p):
        param1 = random.randint(1, 60)
        param2 = random.randint(1, 60)
        param3 = random.randint(1, 60)
        # model_settings['central_stock']['out_reorder_point'] = param1
        # model_settings['secondary_stocks']['north']['out_reorder_point'] = param2
        # model_settings['secondary_stocks']['south']['out_reorder_point'] = param3
        # model_settings['central_stock']['unloading_reorder_point'] = param1
        # model_settings['secondary_stocks']['north']['unloading_reorder_point'] = param2
        # model_settings['secondary_stocks']['south']['unloading_reorder_point'] = param3
        model_settings['central_stock']['inc_reorder_point'] = param1
        model_settings['secondary_stocks']['north']['inc_reorder_point'] = param2
        model_settings['secondary_stocks']['south']['inc_reorder_point'] = param3
        Z_ = []
        W1_ = []
        W2_ = []
        W3_ = []
        W4_ = []
        W5_ = []
        print(f"Зміна параметрів: {j}")
        for i in range(3):
            petri_net = create_main_model(tickrate, **model_settings)

            petri_net.simulate(200, draw=False)
            # petri_net.draw_viz()

            satisfied_clients = petri_net.get_satisfied_clients()
            unhappy_clients = petri_net.get_unsatisfied_clients()
            max_tokens = petri_net.max_tokens

            W1 = satisfied_clients + unhappy_clients
            W2 = unhappy_clients
            W3 = max_tokens['income']
            W4 = max_tokens['unloading']
            W5 = max_tokens['outgoing']

            Z = W2 + sum([W3[key] for key in W3]) + sum([W4[key] for key in W4]) + sum([W5[key] for key in W5])

            print(f"{i}. Цільова функція Z: {Z}")

            W1_.append(W1)
            W2_.append(W2)
            W3_.append(W3)
            W4_.append(W4)
            W5_.append(W5)
            Z_.append(Z)
        Z_arr.append(sum(Z_) / len(Z_))
        params_arr.append([param1, param2, param3])
        W_arr.append([sum(W1_) / len(W1_),
                      sum(W2_) / len(W2_),
                      [sum(W3_[i][key] for i in range(len(W3_))) / len(W3_) for key in W3_[0].keys()],
                      [sum(W4_[i][key] for i in range(len(W4_))) / len(W4_) for key in W4_[0].keys()],
                      [sum(W5_[i][key] for i in range(len(W5_))) / len(W5_) for key in W5_[0].keys()]])
    time_now = datetime.datetime.now() - time_now
    print(f"Час виконання: {time_now}")

    Z_mean = sum(Z_arr) / len(Z_arr)
    Z_dispersion = sum([(Z - Z_mean) ** 2 for Z in Z_arr]) / len(Z_arr)

    print(f"Середнє значення Z: {Z_mean}")
    print(f"Дисперсія Z: {Z_dispersion}")

    epsilon = math.sqrt(Z_dispersion / (p * (1 - 0.95)))
    print(f"Епсілон: {epsilon}")
    print(f"Похибка: {epsilon / Z_mean}")

    print(f"min: {min(Z_arr)}")
    print(f"Точка мінімуму: {Z_arr.index(min(Z_arr))}")
    print(f"Параметри: {params_arr[Z_arr.index(min(Z_arr))]}")
    print(f"Задоволені клієнти: {W_arr[Z_arr.index(min(Z_arr))][0]}")
    print(f"Незадоволені клієнти: {W_arr[Z_arr.index(min(Z_arr))][1]}")
    print(f"Максимальна кількість товарів в зонах прибуття: {W_arr[Z_arr.index(min(Z_arr))][2]}")
    print(f"Максимальна кількість товарів в зонах розвантаження: {W_arr[Z_arr.index(min(Z_arr))][3]}")
    print(f"Максимальна кількість товарів в зонах відправки: {W_arr[Z_arr.index(min(Z_arr))][4]}")


if __name__ == "__main__":
    main()
