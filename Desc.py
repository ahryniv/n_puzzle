import math
from termcolor import colored
import Exceptions
from RandomNumber import random_number_below


class Desc:
    standard_state = None

    def __init__(self, desc=None, size=None):
        self.zero_x, self.zero_y = None, None
        if desc:
            self._desc = desc
            self.size = size
            if self.size != math.sqrt(len(self._desc)):
                raise Exceptions.NotValidDesc("Size of puzzle doesn't match given size")
            self.__class__.standard_state = self.__class__.standard_state if self.__class__.standard_state \
                else self._set_correct_dict()
            try:
                self._find_zero_field()
                self._calculate_not_placed_tiles()
                self._calculate_all_manhattan()
                if not self.is_solvable():
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

    def is_solvable(self):
        less_tiles = self.count_all_inversions()

        # for odd size puzzles
        if self.size % 2 == 1:
            return less_tiles % 2 == 0

        # for even size puzzles
        row = self.zero_x + 1
        if (row % 2 == 1 and less_tiles % 2 == 1) or (row % 2 == 0 and less_tiles % 2 == 0):
            return True
        return False

    def count_all_inversions(self):
        count = 0
        for idx, tile in enumerate(self._desc):
            if tile == 0:
                continue
            count += self._count_inversions(idx, tile)
        return count

    def _count_inversions(self, idx, tile):
        x_tile, y_tile = self.standard_state[tile]
        count = 0
        for j in range(idx + 1, len(self._desc)):
            x_correct_tmp, y_correct_tmp = self.standard_state[self._desc[j]]
            if (x_correct_tmp < x_tile or (x_correct_tmp == x_tile and y_correct_tmp < y_tile)) and self._desc[j] != 0:
                count += 1
        return count

    def _set_correct_dict(self):
        result = {}
        correct_state = self._create_correct_desc()
        for idx, tile in enumerate(correct_state):
            result[tile] = int(idx / self.size), idx % self.size
        return result

    def _create_correct_desc(self):
        numbers = [number for number in range(1, self.size * self.size + 1)]
        numbers[-1] = 0
        return numbers

    def _find_zero_field(self):
        for idx, tile in enumerate(self._desc):
            if tile == 0:
                self.zero_x = int(idx / self.size)
                self.zero_y = idx % self.size
                break

    def shuffle_desc(self, shuffle_number: int):
        i = 0
        last_operation = None
        while i < shuffle_number:
            try:
                operation_, func = tuple(self.operations.items())[random_number_below(4)]
                if self.opposite_operations[operation_] == last_operation:
                    continue
                func(self, self.zero_x, self.zero_y)
                last_operation = operation_
                i += 1
            except Exceptions.MovingDescException:
                continue
        self._calculate_not_placed_tiles()
        self._calculate_all_manhattan()

    def change_tiles(self, x1, y1, x2, y2):
        if x1 >= self.size or x2 >= self.size or y1 >= self.size or y2 >= self.size:
            raise IndexError
        assert self._desc[x1*self.size+y1] == 0 or self._desc[x2*self.size+y2] == 0, \
            "Trying to move TWO not zero tiles (x: {0}, y: {1}) (x: {2}, y: {3})".format(x1, y1, x2, y2)
        manhattan_1 = self._calculate_manhattan(x1, y1, self._desc[x1*self.size+y1]) + \
                      self._calculate_manhattan(x2, y2, self._desc[x2*self.size+y2])
        correct_1 = int(self.is_correct_tile(x1, y1)) + int(self.is_correct_tile(x2, y2))
        buffer = self._desc[x2*self.size+y2]
        self._desc[x2*self.size+y2] = self._desc[x1*self.size+y1]
        self._desc[x1*self.size+y1] = buffer

        correct_2 = int(self.is_correct_tile(x1, y1)) + int(self.is_correct_tile(x2, y2))
        manhattan_2 = self._calculate_manhattan(x1, y1, self._desc[x1*self.size+y1]) + \
                      self._calculate_manhattan(x2, y2, self._desc[x2*self.size+y2])
        self.not_placed_tiles += correct_1 - correct_2
        self.all_manhattan += manhattan_2 - manhattan_1

        ### DELETE it
        if self.not_placed_tiles < 0 or self.all_manhattan < 0:
            raise Exceptions.NotValidDesc("error in change tiles")

        ###
        self.zero_x, self.zero_y = (x1, y1) if self._desc[x1*self.size+y1] == 0 else (x2, y2)

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
        for idx, tile in enumerate(self._desc):
            # if tile == 0:
            #     continue
            i, j = int(idx / self.size), idx % self.size
            if not self.is_correct_tile(i, j):
                self.not_placed_tiles += 1

    def is_correct_tile(self, x, y):
        tile = self._desc[x*self.size+y]
        if (x, y) == self.standard_state[tile]:
            return True
        return False

    def _calculate_all_manhattan(self):
        self.all_manhattan = 0
        for idx, tile in enumerate(self._desc):
            x, y = int(idx / self.size), idx % self.size
            self.all_manhattan += self._calculate_manhattan(x, y, tile)

    def _calculate_manhattan(self, x, y, tile):
        if tile == 0:
            return 0
        x_true, y_true = self.standard_state[tile]
        result = math.fabs(x_true - x) + math.fabs(y_true - y)
        return result

    def calculate_linear_conflict(self):
        linear_conflict = 0
        for idx, tile in enumerate(self._desc):
            x, y = int(idx / self.size), idx % self.size
            linear_conflict += self._calculate_linear_for_tile(x, y, tile)
        return linear_conflict

    def _calculate_linear_for_tile(self, x, y, tile):
        result = 0
        x_true, y_true = self.standard_state[tile]
        tile = tile if tile != 0 else self.size ** 2
        idx = x * self.size + y
        if y == y_true:
            for tmp_tile in self._desc[idx::self.size]:
                tmp_y = self.standard_state[tmp_tile][1]
                tmp_tile = tmp_tile if tmp_tile != 0 else self.size ** 2
                if tmp_y == y and tile > tmp_tile:
                    result += 2
        if x == x_true:
            for tmp_tile in self._desc[idx:((idx+self.size)//self.size)*self.size]:
                tmp_x = self.standard_state[tmp_tile][0]
                tmp_tile = tmp_tile if tmp_tile else self.size ** 2
                if tmp_x == x and tile > tmp_tile:
                    result += 2
        return result

    def __str__(self):
        result = " {0} \n".format(" ".join(["___" for _ in range(self.size)]))
        column_counter = 1
        slices = None
        row = None
        for idx, tile in enumerate(self._desc):
            if column_counter == 1:
                slices = []
                row = "|{0}|\n".format("|".join(["   " for _ in range(self.size)]))
            i, j = int(idx / self.size), idx % self.size
            if j == self.zero_y and i == self.zero_x:
                slices.append("   ".format(tile))
            elif ((j - 1 == self.zero_y or j + 1 == self.zero_y) and i == self.zero_x) \
                    or ((i - 1 == self.zero_x or i + 1 == self.zero_x) and j == self.zero_y):
                slices.append(colored("{: >2d} ".format(tile), "cyan", attrs=["bold"]))
            else:
                slices.append(colored("{: >2d} ".format(tile), "cyan"))
            column_counter = 1 if column_counter == self.size else column_counter + 1
            if column_counter == 1:
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
        desc_ = [[0]*self.size for _ in range(self.size)]
        i = 0
        j = -1
        i_move = 0
        res = [0] * (self.size ** 2)
        while numbers:
            if moves[i_move] == "right" and j < self.size - 1 and desc_[i][j + 1] == 0:
                j += 1
            elif moves[i_move] == "down" and i < self.size - 1 and desc_[i + 1][j] == 0:
                i += 1
            elif moves[i_move] == "left" and j > 0 and desc_[i][j - 1] == 0:
                j -= 1
            elif moves[i_move] == "up" and i > 0 and desc_[i - 1][j] == 0:
                i -= 1
            else:
                i_move = i_move + 1 if i_move < len(moves) - 1 else 0
                continue
            n = numbers.pop()
            desc_[i][j] = n
            res[i * self.size + j] = n
        return res

    def is_solvable(self):
        less_tiles = self.count_all_inversions()

        # for odd size puzzles
        if self.size % 2 == 1:
            return less_tiles % 2 == 0

        # for even size puzzles
        row = self.zero_x + 1
        if (row % 2 == 1 and less_tiles % 2 == 0) or (row % 2 == 0 and less_tiles % 2 == 1):
            return True
        return False


class DescColumn(Desc):
    def _create_correct_desc(self):
        numbers = [number for number in range(1, self.size * self.size + 1)][::-1]
        numbers[0] = 0
        desc_ = [0] * (self.size ** 2)
        for idx in range(self.size ** 2):
            i, j = int(idx / self.size), idx % self.size
            desc_[(j * self.size) + i] = numbers.pop()
        return desc_

    def is_solvable(self):
        less_tiles = self.count_all_inversions()

        # for odd size puzzles
        if self.size % 2 == 1:
            return less_tiles % 2 == 0

        # for even size puzzles
        row = self.zero_x + 1
        if (row % 2 == 1 and less_tiles % 2 == 1) or (row % 2 == 0 and less_tiles % 2 == 0):
            return True
        return False


if __name__ == "__main__":
    desc = Desc(size=5)
    # desc.shuffle_desc(2)
    # descColumn = DescColumn(size=5)
    # descColumn.shuffle_desc(20000)
    # descSnail = DescSnail(size=5)
    # descSnail.shuffle_desc(20000)
    print(desc)
    print(desc.not_placed_tiles)
    # print(descColumn)
    # print(descSnail)

