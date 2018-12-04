import time
from optparse import OptionParser
import Algorithm as Algorithm
import Heuristics
from Desc import Desc
import Exceptions

'''
1. Перевірити, яке має бути правильне положення п'ятнашки: по черзі чи змійкою
'''


class Parameters:
    heuristics = {
        'Manhattan': Heuristics.HeuristicManhattan,
        'LinearConflict': Heuristics.HeuristicLinearConflictWithManhattan,
        'NotPlacedTiles': Heuristics.HeuristicNotPlacedTiles,
        'CountLessTiles': Heuristics.HeuristicCountLessTiles
    }

    def __init__(self):
        parser = OptionParser()
        self.add_options_to_parser(parser)
        opts, args = parser.parse_args()
        self.file = opts.file
        self.shuffle = opts.shuffle
        self.size = opts.size
        self.algorithm = opts.algorithm
        if self.algorithm not in self.heuristics.keys():
            print("There is not such heuristic algorithm:", self.algorithm)
            exit()

    def add_options_to_parser(self, parser):
        heuristics = ", ".join(self.heuristics.keys())
        parser.add_option('-a', '--algorithm', dest="algorithm",
                          help="[" + heuristics + "], " + "[default: %default]")
        parser.add_option('--shuffle', dest="shuffle", type="int",
                          help="Amount of random moves from correct state"
                               " of desc, [default: %default]")
        parser.add_option('-s', '--size', dest="size", type="int",
                          help="Size of the desc, [default: %default]")
        parser.add_option('-f', '--file', dest="file",
                          help="File with start statement of desc")
        parser.set_defaults(algorithm="Manhattan", shuffle=30, size=4)


class DescParser:
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        fp = None
        result = []
        try:
            fp = open(self.filename)
            for line in fp:
                line = line.strip()
                if line.startswith("#") or not line:
                    continue
                elif "#" in line:
                    line = line.split("#")[0].strip()
                elements = [int(x) for x in line.split()]
                result.append(elements)
            return result
        except ValueError as err:
            raise Exceptions.NotValidDesc
        finally:
            if fp is not None:
                fp.close()


class Solver:
    def __init__(self):
        self.parameters = Parameters()
        self._create_desc()

    def _create_desc(self):
        if self.parameters.file is not None:
            try:
                desc_parser = DescParser(self.parameters.file)
                desc_field = desc_parser.parse()
                self.desc = Desc(desc=desc_field)
            except Exceptions.NotValidDesc:
                print("Puzzle is not valid")
                exit()
            except Exceptions.Unsolvable:
                print("Puzzle in unsolvable")
                exit()
        else:
            self.desc = Desc(size=self.parameters.size)
            self.desc.shuffle_desc(self.parameters.shuffle)

    def solve(self):
        def get_milliseconds():
            return round(time.time() * 1000)
        print("Start state of puzzle:")
        print(self.desc)
        time1 = get_milliseconds()
        algorithm_1 = Algorithm.AlgorithmA(self.parameters.heuristics[self.parameters.algorithm])
        returned_value = algorithm_1.solve(self.desc)
        time2 = get_milliseconds()
        self.print_output(returned_value, time2 - time1)

    def print_output(self, returned_value, time_diff):
        print("Movements:")
        for movement in returned_value.movements:
            try:
                self.desc.green_x = movement.x
                self.desc.green_y = movement.y
                print(movement)
                func = self.desc.operations[self.desc.opposite_operations[str(movement)]]
                func(self.desc, self.desc.zero_x, self.desc.zero_y)
                print(self.desc)
            except Exceptions.MovingDescException as err:
                print(err)
        print("Heuristic algorithm:", self.parameters.algorithm)
        print("Time:", (time_diff / 1000), "seconds")
        print("Total number of states ever selected in the opened set:", returned_value.ever_opened)
        print("Maximum number of states ever represented in memory at the same time:", returned_value.max_opened)
        print("Number of moves:", len(returned_value.movements))
        print()


if __name__ == "__main__":
    try:
        solver = Solver()
        solver.solve()
    except KeyboardInterrupt:
        print()
