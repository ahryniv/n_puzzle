import time
import Algorithm
import Heuristics
from Desc import Desc

if __name__ == "__main__":
    try:
        # size_desc = int(input("Give me size of desc: "))
        #
        # desc = Desc(size=4)
        # desc.shuffle_desc(20)
        # print("Shuffle desc")
        # print(desc)

        # random_desc = Desc(size=size_desc)
        # random_desc.make_random_desc()
        # print("Random desc")
        # print(random_desc)

        desc_field = [[5, 3, 7, 4],
                      [2, 6, 1, 8],
                      [13, 9, 11, 12],
                      [0, 10, 14, 15]]
        desc = Desc(desc_field)
        print(desc)

        get_miliseconds = lambda: round(time.time() * 1000)
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
