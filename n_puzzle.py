import time
import Algorithm as Algorithm
import Heuristics
from Desc import Desc

'''
По оптимізації:
1. в класі OpenedListContainer переглянути реалізацію 'dict_for_check', щоб вона чітко працювала в методі 'has'
    Можливо є сенс спробувати інший тип даних для 'dict_for_check'. Наприклад SortedList
'''


if __name__ == "__main__":
    get_miliseconds = lambda: round(time.time() * 1000)
    try:

        # random_desc = Desc(size=4)
        # random_desc.make_random_desc()
        # print("Random desc")
        # print(random_desc)
        #
        # desc = Desc(size=4)
        # desc.shuffle_desc(20)
        # print("Shuffle desc")
        # print(desc)

        # desc_field = [[5, 3, 7, 4],
        #               [2, 6, 1, 8],
        #               [13, 9, 11, 12],
        #               [0, 10, 14, 15]]
        desc_field = [[1, 3, 10, 4],
                      [7, 2, 8, 0],
                      [5, 9, 15, 12],
                      [13, 14, 6, 11]]
        desc = Desc(desc_field)
        print(desc)

        time1 = get_miliseconds()
        algorithm_1 = Algorithm.AlgorithmA(Heuristics.HeuristicNotPlacedTiles)
        result = algorithm_1.solve(desc)
        movements = result[0]
        time2 = get_miliseconds()
        print(((time2 - time1) / 1000), "seconds")
        print("Time for one check =", (time2 - time1) / result[1])

        print()
        print("Movements:")
        for i in range(len(movements)):
            print(movements[i])

    except KeyboardInterrupt:
        print()
