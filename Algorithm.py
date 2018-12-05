import copy
from collections import defaultdict, namedtuple
import Exceptions


ReturnValue = namedtuple('ReturnedValue', ['movements', 'ever_opened', 'max_opened'])


class AlgorithmA:
    def __init__(self, heuristic_algorithm):
        self._heuristic_algorithm = heuristic_algorithm()

    def solve(self, desc):
        start_statement = DescStatement(desc, path_from_start=0, heuristic_weight=0, father=None)
        if start_statement.desc.not_placed_tiles == 0:
            return ReturnValue(movements=self.get_movements(start_statement),
                               ever_opened=1,
                               max_opened=1)
        opened = OpenedListContainer()
        opened.add(0, start_statement)
        closed_amount = 0
        while opened:
            current_statement = opened.pop_statement_with_min_weight()
            closed_amount += 1
            founded = current_statement.get_daughters(opened, self._heuristic_algorithm)
            print("Closed: {0}\r".format(closed_amount), end="")
            if founded:
                print()
                return ReturnValue(movements=self.get_movements(founded),
                                   ever_opened=opened.counter_all,
                                   max_opened=opened.max_in_memory)

    @staticmethod
    def get_movements(last_statement):
        movements = []
        while last_statement.father:
            movements.insert(0, last_statement.movement)
            last_statement = last_statement.father
        return movements


class OpenedListContainer:
    def __init__(self):
        self._statements = defaultdict(lambda: [])
        self._statements_for_check = defaultdict(lambda: [])
        self.counter_all = 0
        self.counter_in_memory = 0
        self.counter_in_memory = 0
        self.max_in_memory = 0

    def add(self, weight, statement):
        self._statements[weight].append(statement)
        self._statements_for_check[statement.desc.all_manhattan + statement.desc.not_placed_tiles].append(statement)
        self.counter_all += 1
        self.add_to_counter_in_memory()

    def pop_statement_with_min_weight(self):
        index = min(self._statements)
        statement = self._statements[index].pop()
        if not self._statements[index]:
            del self._statements[index]
            self.counter_in_memory -= 1
        return statement

    def check_for_duplicates(self, new_desc, father):
        for statement in self._statements_for_check[new_desc.all_manhattan + new_desc.not_placed_tiles]:
            if statement.desc == new_desc:
                if statement.path_from_start > father.path_from_start + 1:
                    statement.path_from_start = father.path_from_start + 1
                    statement.father = father
                return True
        return False

    def add_to_counter_in_memory(self):
        self.counter_in_memory += 1
        self.max_in_memory = self.counter_in_memory if self.max_in_memory < self.counter_in_memory \
            else self.counter_in_memory

    def __len__(self):
        return len(self._statements)


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
                if opened_dict.check_for_duplicates(new_desc, self):
                    continue
                movement = Movement(self.desc.zero_x, self.desc.zero_y, new_desc.opposite_operations[func_name])
                new_statement = DescStatement(desc=new_desc, path_from_start=self.path_from_start + 1,
                                              heuristic_weight=heuristic.calculate(new_desc), father=self,
                                              movement=movement)
                opened_dict.add(new_statement.weight, new_statement)
                if new_desc.not_placed_tiles == 0:
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
