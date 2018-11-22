import copy
import sys
import Exceptions
from collections import defaultdict


class AlgorithmA:
    def __init__(self, heuristic_algorithm):
        self._heuristic_algorithm = heuristic_algorithm()

    def solve(self, desc):
        start_statement = DescStatement(desc, weight=0, father=None)
        opened = defaultdict(lambda: [])
        opened[0].append(start_statement)
        closed = []
        while opened:
            index = min(opened)
            current_statement = opened[index].pop()
            if not opened[index]:
                del opened[index]
            closed.append(current_statement)
            founded = current_statement.get_daughters(opened, self._heuristic_algorithm)
            # sys.stdout(len(opened))
            if founded:
                print("Success")
                print(founded.desc)
                return self.get_movements(founded)
                # break
        # return [Movement(0, 0, "up"), Movement(2, 3, "down"), Movement(2, 4, "left")]

    @staticmethod
    def get_movements(last_statement):
        movements = []
        while last_statement.father:
            movements.insert(0, last_statement.movement)
            last_statement = last_statement.father
        return movements


class DescStatement:
    def __init__(self, desc, weight, father, movement=None):
        self.desc = desc
        self.weight = weight
        self.father = father
        self.movement = movement

    def get_daughters(self, opened_dict, heuristic):
        for func_name, func in self.desc.operations.items():
            new_desc = copy.deepcopy(self.desc)
            try:
                func(new_desc, new_desc.zero_x, new_desc.zero_y)
                movement = Movement(new_desc.zero_x, new_desc.zero_y, new_desc.opposite_operations[func_name])
                new_statement = DescStatement(new_desc,
                                              self.weight + 1 + heuristic.calculate(new_desc),
                                              father=self,
                                              movement=movement)
                # if
                (opened_dict[new_statement.weight]).append(new_statement)
                if new_desc.get_not_placed_tiles() == 0:
                    return new_statement
            except Exceptions.MovingDescException:
                continue
        return False


class Movement:
    def __init__(self, x, y, move_key):
        self.x = x
        self.y = y
        self.move_key = move_key

    def __str__(self):
        return self.move_key
