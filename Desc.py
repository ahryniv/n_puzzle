import math
from termcolor import colored
import Exceptions
from RandomNumber import random_number_below


class Desc:
    standard_state = None

    def __init__(self, desc=None, size=3):
        self.zero_x, self.zero_y = None, None
        if desc:
            self._desc = desc
            self.size = len(desc)
            self.__class__.standard_state = self.__class__.standard_state if self.__class__.standard_state \
                else self._set_correct_dict()
            try:
                self._find_zero_field()
                self._calculate_not_placed_tiles()
                self._calculate_all_manhattan()
                if not self.is_correct():
                    raise Exceptions.Unsolvable()
            except IndexError:
                raise Exceptions.NotValidDesc()
        else:
            self.size = size
            self.__class__.standard_state = self.__class__.standard_state if self.__class__.standard_state \
                else self._set_correct_dict()
            self._desc = self._create_correct_desc()
            self._find_zero_field()
            self.not_placed_tiles = 0
            self.all_manhattan = 0

    def is_correct(self):
        for i in range(self.size):
            if len(self._desc[i]) != self.size:
                raise Exceptions.NotValidDesc()
        count = self.count_all_less_tiles() + self.zero_x + 1
        if count % 2 == 1:
            return False
        return True

    def _set_correct_dict(self):
        result = {}
        correct_state = self._create_correct_desc()
        for i in range(self.size):
            for j in range(self.size):
                result[correct_state[i][j]] = (i, j)
        return result

    def _create_correct_desc(self):
        numbers = [number for number in range(1, self.size * self.size + 1)]
        numbers[-1] = 0
        return [numbers[i*self.size:(i+1)*self.size] for i in range(self.size)]

    def count_all_less_tiles(self):
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if self._desc[i][j] == 0:
                    continue
                count += self._count_less_tiles(i, j)
        return count

    def _count_less_tiles(self, x, y):
        tile = self._desc[x][y]
        x_tile, y_tile = self.standard_state[tile]
        count = 0
        for i in range(x, self.size):
            for j in range(y + 1, self.size):
                x_tmp, y_tmp = self.standard_state[self._desc[i][j]]
                if (x_tmp < x_tile or (x_tmp == x_tile and y_tmp < y_tile)) and self._desc[i][j] != 0:
                    count += 1
        return count

    def _find_zero_field(self):
        for i in range(self.size):
            for j in range(self.size):
                if self._desc[i][j] == 0:
                    self.zero_x = i
                    self.zero_y = j
                    break

    def shuffle_desc(self, shuffle_number: int):
        i = 0
        last_operation = None
        while i < shuffle_number:
            try:
                operation_, func = tuple(self.operations.items())[random_number_below(4)]
                if self.opposite_operations[operation_] == last_operation:
                    raise Exceptions.MovingDescException()
                func(self, self.zero_x, self.zero_y)
                last_operation = operation_
                i += 1
            except Exceptions.MovingDescException:
                continue
        self._calculate_not_placed_tiles()
        self._calculate_all_manhattan()

    def change_tiles(self, x1, y1, x2, y2):
        assert self._desc[x1][y1] == 0 or self._desc[x2][y2] == 0, \
            "Trying to move TWO not zero tiles (x: {0}, y: {1}) (x: {2}, y: {3})".format(x1, y1, x2, y2)
        manhattan_1 = self._calculate_manhattan(x1, y1) + self._calculate_manhattan(x2, y2)
        correct_1 = int(self.is_correct_tile(x1, y1)) + int(self.is_correct_tile(x2, y2))
        buffer = self._desc[x2][y2]
        self._desc[x2][y2] = self._desc[x1][y1]
        self._desc[x1][y1] = buffer

        correct_2 = int(self.is_correct_tile(x1, y1)) + int(self.is_correct_tile(x2, y2))
        manhattan_2 = self._calculate_manhattan(x1, y1) + self._calculate_manhattan(x2, y2)
        self.not_placed_tiles += correct_1 - correct_2
        self.all_manhattan += manhattan_2 - manhattan_1
        self.zero_x, self.zero_y = (x1, y1) if self._desc[x1][y1] == 0 else (x2, y2)

    def move_down_element(self, x, y):
        try:
            self.change_tiles(x, y, x + 1, y)
        except IndexError:
            raise Exceptions.MovingDescException("Can't move this down (x: {0}, y: {1})".format(x, y))

    def move_right_element(self, x, y):
        try:
            self.change_tiles(x, y + 1, x, y)
        except IndexError:
            raise Exceptions.MovingDescException("Can't move this right (x: {0}, y: {1})".format(x, y))

    def move_up_element(self, x, y):
        try:
            if x < 1:
                raise Exceptions.MovingDescException("Can't move this up (x: {0}, y: {1})".format(x, y))
            self.change_tiles(x - 1, y, x, y)
        except IndexError:
            raise Exceptions.MovingDescException("Can't move this up (x: {0}, y: {1})".format(x, y))

    def move_left_element(self, x, y):
        try:
            if y < 1:
                raise Exceptions.MovingDescException("Can't move this left (x: {0}, y: {1})".format(x, y))
            self.change_tiles(x, y - 1, x, y)
        except IndexError:
            raise Exceptions.MovingDescException("Can't move this left (x: {0}, y: {1})".format(x, y))

    def _calculate_not_placed_tiles(self):
        self.not_placed_tiles = 0
        for i in range(self.size):
            for j in range(self.size):
                if not self.is_correct_tile(i, j):
                    self.not_placed_tiles += 1

    def is_correct_tile(self, x, y):
        if (x, y) == self.standard_state[self._desc[x][y]]:
            return True
        return False

    def _calculate_all_manhattan(self):
        self.all_manhattan = 0
        for i in range(self.size):
            for j in range(self.size):
                self.all_manhattan += self._calculate_manhattan(i, j)

    def _calculate_manhattan(self, x, y):
        tile = self._desc[x][y]
        if tile == 0:
            return 0
        x_true, y_true = self.standard_state[tile]
        result = math.fabs(x_true - x) + math.fabs(y_true - y)
        return result

    def calculate_linear_conflict(self):
        linear_conflict = 0
        for i in range(self.size):
            for j in range(self.size):
                linear_conflict += self.calculate_linear_for_tile(i, j)
        return linear_conflict

    def calculate_linear_for_tile(self, x, y):
        result = 0
        x_true, y_true = self.standard_state[self._desc[x][y]]
        tile = self._desc[x][y]
        tile = tile if tile != 0 else self.size ** 2
        if y == y_true:
            for i in range(x + 1, self.size):
                tmp = self._desc[i][y]
                tmp_y = self.standard_state[tmp][1]
                tmp = tmp if tmp != 0 else self.size ** 2
                if tmp_y == y and tile > tmp:
                    result += 2
        if x == x_true:
            for j in range(y + 1, self.size):
                tmp = self._desc[x][j]
                tmp_x = self.standard_state[tmp][0]
                tmp = tmp if tmp else self.size ** 2
                if tmp_x == x and tile > tmp:
                    result += 2
        return result

    def __str__(self):
        result = " {0} \n".format(" ".join(["___" for _ in range(self.size)]))
        for i in range(self.size):
            row = "|{0}|\n".format("|".join(["   " for _ in range(self.size)]))
            slices = []
            for j in range(self.size):
                if j == self.zero_y and i == self.zero_x:
                    slices.append(colored("{: >2d} ".format(self._desc[i][j]), "blue"))
                else:
                    slices.append("{: >2d} ".format(self._desc[i][j]))
            row += "|{0}|\n".format("|".join(slices))
            row += "|{0}|\n".format("|".join(["___" for _ in range(self.size)]))
            result += row
        return result

    def __getitem__(self, item):
        return self._desc[item]

    def __eq__(self, other):
        if not isinstance(other, Desc):
            raise TypeError("not comparable types")
        return other._desc == self._desc

    operations = {
        'up': move_up_element,
        'down': move_down_element,
        'right': move_right_element,
        'left': move_left_element
    }

    opposite_operations = {
        "left": "right",
        "right": "left",
        "up": "down",
        "down": "up"
    }


class DescSnail(Desc):
    def _create_correct_desc(self):
        numbers = [number for number in range(1, self.size * self.size + 1)][::-1]
        numbers[0] = 0
        moves = ["right", "down", "left", "up"]
        desc = [[0]*self.size for _ in range(self.size)]
        i = 0
        j = -1
        i_move = 0
        while numbers:
            if moves[i_move] == "right" and j < self.size - 1 and desc[i][j + 1] == 0:
                j += 1
            elif moves[i_move] == "down" and i < self.size - 1 and desc[i + 1][j] == 0:
                i += 1
            elif moves[i_move] == "left" and j > 0 and desc[i][j - 1] == 0:
                j -= 1
            elif moves[i_move] == "up" and i > 0 and desc[i - 1][j] == 0:
                i -= 1
            else:
                i_move = i_move + 1 if i_move < len(moves) - 1 else 0
                continue
            n = numbers.pop()
            desc[i][j] = n
        self.zero_x, self.zero_y = i, j
        return desc


if __name__ == "__main__":
    snail_desc = DescSnail(size=4)
    print(snail_desc)
