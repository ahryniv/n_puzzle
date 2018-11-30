import time
import Algorithm as Algorithm
import Heuristics
from Desc import Desc

'''
Перевірити чи функція Desc.is_correct() правильно працює
Відповідь: неправильно.
'''


if __name__ == "__main__":
    get_miliseconds = lambda: round(time.time() * 1000)
    try:

        # desc = Desc(size=4)
        # desc.make_random_desc()
        # print("Random desc")

        # desc = Desc(size=4)
        # desc.shuffle_desc(40)
        # print("Shuffle desc")

        # Closed = 32000,  201357 -         Terminated
        # Closed = 413286 -                 Terminated
        # desc_field = [[1, 7, 4, 3],
        #               [13, 0, 2, 8],
        #               [14, 5, 11, 10],
        #               [9, 6, 15, 12]]

        # Closed = 3987, 4995 -             4.5,  1.147 sec
        # Closed = 629,  715, 84 -          0.25, 0.173, 0.026 sec
        # Closed = 229 -                    0.079 sec
        # desc_field = [[1, 3, 10, 4],
        #               [7, 2, 8, 0],
        #               [5, 9, 15, 12],
        #               [13, 14, 6, 11]]

        # Closed = 14274, 17819 -           51,  4.145 sec
        # Closed = 3620,  5002, 942, 299 -  3.3, 1.1, 0.257, 0.077 sec
        # Closed = 4297 -                   3.278 sec
        desc_field = [[1, 6, 4, 2],
                      [9, 11, 5, 3],
                      [13, 7, 0, 12],
                      [14, 10, 8, 15]]

        # desc_field = [
        #     [1, 2, 3, 4],
        #     [5, 6, 7, 8],
        #     [9, 10, 11, 12],
        #     [13, 14, 15, 0]
        # ]

        desc = Desc(desc_field)

        print(desc)
        if not desc.is_correct():
            print("Not solvable")
            exit()
        # else:
        #     print("Solvable")
        #     exit()
        time1 = get_miliseconds()
        algorithm_1 = Algorithm.AlgorithmA(Heuristics.HeuristicCountLessTiles)
        movements = algorithm_1.solve(desc)
        time2 = get_miliseconds()
        print(((time2 - time1) / 1000), "seconds")

        print()
        print("Movements:")
        for i in range(len(movements)):
            print(movements[i])

    except KeyboardInterrupt:
        print()
