import time
import Algorithm as Algorithm
import Heuristics
from Desc import Desc


if __name__ == "__main__":
    get_miliseconds = lambda: round(time.time() * 1000)
    try:

        # random_desc = Desc(size=4)
        # random_desc.make_random_desc()
        # print("Random desc")

        # desc = Desc(size=5)
        # desc.shuffle_desc(30)
        # print("Shuffle desc")

        # Closed = 32000,  201357  Terminated
        # Closed = 413286          Terminated
        # desc_field = [[1, 7, 4, 3],
        #               [13, 0, 2, 8],
        #               [14, 5, 11, 10],
        #               [9, 6, 15, 12]]

        # Closed = 3987, 4995 - 4.5,  1.147 sec
        # Closed = 629,  715  - 0.25, 0.173 sec
        # desc_field = [[1, 3, 10, 4],
        #               [7, 2, 8, 0],
        #               [5, 9, 15, 12],
        #               [13, 14, 6, 11]]

        # Closed = 14274, 17819 - 51,  4.145 sec
        # Closed = 3620,  5002  - 3.3, 1.1   sec
        desc_field = [[1, 6, 4, 2],
                      [9, 11, 5, 3],
                      [13, 7, 0, 12],
                      [14, 10, 8, 15]]

        desc = Desc(desc_field)
        print(desc)

        time1 = get_miliseconds()
        algorithm_1 = Algorithm.AlgorithmA(Heuristics.HeuristicNotPlacedTiles)
        movements = algorithm_1.solve(desc)
        time2 = get_miliseconds()
        print(((time2 - time1) / 1000), "seconds")

        print()
        print("Movements:")
        for i in range(len(movements)):
            print(movements[i])

    except KeyboardInterrupt:
        print()
