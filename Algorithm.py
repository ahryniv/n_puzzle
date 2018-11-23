import copy
import sys
from collections import defaultdict
from sortedcontainers import SortedList
import Exceptions

class AlgorithmA:
    def __init__(self, heuristic_algorithm):
        self._heuristic_algorithm = heuristic_algorithm()

    def solve(self, desc):
        start_statement = DescStatement(desc, path_from_start=0, heuristic_weight=0, father=None)
        opened = OpenedListContainer()
        opened.add(0, start_statement)
        closed = []
        while opened:
            index = min(opened)
            current_statement = opened.pop(index)
            if not opened[index]:
                del opened[index]
            closed.append(current_statement)
            founded = current_statement.get_daughters(opened, self._heuristic_algorithm)
            sys.stdout.write("\rOpened: {}, Closed: {}".format(str(len(opened)), str(len(closed))))
            if founded:
                print()
                print("Success")
                print(founded.desc)
                return  self.get_movements(founded), len(closed)
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
    def __init__(self, desc, path_from_start, heuristic_weight, father, movement=None):
        self.desc = desc
        self.path_from_start = path_from_start
        self.heuristic_weight = heuristic_weight
        self.father = father
        self.movement = movement

    @property
    def weight(self):
        return self.path_from_start + self.heuristic_weight

    def get_daughters(self, opened_dict, heuristic):
        for func_name, func in self.desc.operations.items():
            new_desc = copy.deepcopy(self.desc)
            try:
                func(new_desc, new_desc.zero_x, new_desc.zero_y)
                duplicate = opened_dict.has(new_desc)
                if duplicate:
                    if (opened_dict[duplicate[0]][duplicate[1]]).path_from_start > self.path_from_start + 1:
                        (opened_dict[duplicate[0]][duplicate[1]]).path_from_start = self.path_from_start + 1
                        (opened_dict[duplicate[0]][duplicate[1]]).father = self
                    continue
                movement = Movement(new_desc.zero_x, new_desc.zero_y, new_desc.opposite_operations[func_name])
                new_statement = DescStatement(desc=new_desc,
                                              path_from_start=self.path_from_start + 1,
                                              heuristic_weight=heuristic.calculate(new_desc),
                                              father=self,
                                              movement=movement)

                opened_dict.add(new_statement.weight, new_statement)
                if new_desc.get_not_placed_tiles() == 0:
                    return new_statement
            except Exceptions.MovingDescException:
                continue
        return False


class OpenedListContainer:
    def __init__(self):
        self.dict = defaultdict(lambda: [])
        self.dict_for_check = defaultdict(lambda: [])

    def add(self, weight, statement):
        self.dict[weight].append(statement)
        self.dict_for_check[statement.desc.not_placed_tiles].append(statement)

    def pop(self, weight):
        statement = self.dict[weight].pop()
        self.dict_for_check[statement.desc.not_placed_tiles].pop()
        return statement

    def has(self, new_desc):
        for key, value in self.dict.items():
            for i, statement in enumerate(value):
                if statement.desc.not_placed_tiles != new_desc.not_placed_tiles:
                    continue
                if statement.desc == new_desc:
                    return key, i
        return False

    def __iter__(self):
        return self.dict.__iter__()

    def __getitem__(self, item):
        return self.dict[item]

    def __delitem__(self, key):
        del self.dict[key]

    def __len__(self):
        return len(self.dict)


class Movement:
    def __init__(self, x, y, move_key):
        self.x = x
        self.y = y
        self.move_key = move_key

    def __str__(self):
        return self.move_key
