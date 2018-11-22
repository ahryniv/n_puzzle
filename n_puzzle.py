import Algorithm
import Heuristics
from Desc import Desc

if __name__ == "__main__":
    try:
        size_desc = int(input("Give me size of desc: "))

        # regular_desc = Desc(size=size_desc)
        # print("Regular desc #1")
        # print(regular_desc)
        # print("Not placed tiles: {0}".format(regular_desc.get_not_placed_tiles()))

        shuffle_desc = Desc(size=size_desc)
        shuffle_desc.shuffle_desc(10)
        print("Shuffle desc")
        print(shuffle_desc)
        # print("Not placed tiles: {0}".format(shuffle_desc.get_not_placed_tiles()))

        algorithm_1 = Algorithm.AlgorithmA(Heuristics.HeuristicNotPlacedTiles)
        movements = algorithm_1.solve(shuffle_desc)

        for i in range(len(movements)):
            print(movements[i])

        # random_desc = Desc(size=size_desc)
        # random_desc.make_random_desc()
        # print("Random desc")
        # print(random_desc)
        # print("Not placed tiles: {0}".format(random_desc.get_not_placed_tiles()))

        # another_desc = copy.deepcopy(regular_desc)
        # another_desc.shuffle_desc(5)
        # print("Regular desc")
        # print(regular_desc)
        # print("Another desc")
        # print(another_desc)
        # algo_with_manhattan = algorithm.AlgorithmA(algorithm.HeuristicManhattan)
        # result = algo_with_manhattan.solve(desc_example)
        # print(result)
        # while True:
        #     x_inp = int(input("give me x: "))
        #     y_inp = int(input("give me y: "))
        #     operation = Desc.operations[input("Give me operation: ")]
        #     operation(desc_example, x_inp, y_inp)
        #     print(desc_example)
    except KeyboardInterrupt:
        print()
