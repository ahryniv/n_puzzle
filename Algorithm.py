import copy
import heapq
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
        opened = OpenedContainer()
        closed = ClosedContainer()
        opened.add(0, start_statement)
        closed_amount = 0
        while opened:
            current_statement = opened.pop()
            closed.add(current_statement)
            closed_amount += 1
            founded = current_statement.get_daughters(opened, closed, self._heuristic_algorithm)
            print("Closed: {0}\r".format(closed_amount), end="")
            if founded:
                print()
                return ReturnValue(movements=self.get_movements(founded),
                                   ever_opened=opened.ever_opened,
                                   max_opened=opened.ever_opened + closed.counter)

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

    def get_daughters(self, opened, closed, heuristic):
        for func_name, func in self.desc.operations.items():
            new_desc = copy.deepcopy(self.desc)
            try:
                func(new_desc, new_desc.zero_x, new_desc.zero_y)
                if closed.check_for_duplicates(new_desc, func_name, self):
                    continue
                movement = Movement(self.desc.zero_x, self.desc.zero_y, new_desc.opposite_operations[func_name])
                new_statement = DescStatement(desc=new_desc, path_from_start=self.path_from_start + 1,
                                              heuristic_weight=heuristic.calculate(new_desc), father=self,
                                              movement=movement)
                opened.add(new_statement.weight, new_statement)
                if new_desc.not_placed_tiles == 0:
                    return new_statement
            except Exceptions.MovingDescException:
                continue
        return False

    def __lt__(self, other):
        return self.desc.not_placed_tiles + self.desc.all_manhattan < other.desc.not_placed_tiles + other.desc.all_manhattan


class OpenedContainer:
    def __init__(self):
        self._statements = []
        self.ever_opened = 0

    def add(self, weight, statement):
        heapq.heappush(self._statements, (weight, statement))
        self.ever_opened += 1

    def pop(self):
        weight, statement = heapq.heappop(self._statements)
        return statement


class ClosedContainer:
    def __init__(self):
        self._statements_for_check = defaultdict(lambda: [])
        self.counter = 0

    def add(self, statement):
        self._statements_for_check[statement.desc.all_manhattan + statement.desc.not_placed_tiles].append(statement)
        self.counter += 1

    def check_for_duplicates(self, new_desc, func_name, father):
        for statement in self._statements_for_check[new_desc.all_manhattan + new_desc.not_placed_tiles]:
            if statement.desc == new_desc:
                if statement.path_from_start > father.path_from_start + 1:
                    statement.path_from_start = father.path_from_start + 1
                    statement.father = father
                    movement = Movement(father.desc.zero_x, father.desc.zero_y, new_desc.opposite_operations[func_name])
                    statement.movement = movement
                return True
        return False


class Movement:
    def __init__(self, x, y, move_key):
        self.x = x
        self.y = y
        self.move_key = move_key

    def __str__(self):
        return self.move_key
