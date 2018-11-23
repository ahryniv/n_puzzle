import random
import Exceptions


class Desc:
    def __init__(self, desc=None, size=3):
        self.zero_x, self.zero_y = None, None
        if desc:
            # NEED DESC VALIDATION
            self._desc = desc
            self.size = len(desc)
            self._find_zero_field()
            self.not_placed_tiles = self.get_not_placed_tiles()
        else:
            self.size = size
            self._desc = self._create_correct_desc()
            self.not_placed_tiles = 0

    def _create_correct_desc(self):
        numbers = [number for number in range(1, self.size * self.size + 1)]
        numbers[-1] = 0
        self.zero_x, self.zero_y = self.size - 1, self.size - 1
        return [numbers[i*self.size:(i+1)*self.size] for i in range(self.size)]

    def _find_zero_field(self):
        for i in range(self.size):
            for j in range(self.size):
                if self._desc[i][j] == 0:
                    self.zero_x = i
                    self.zero_y = j
                    break

    def make_random_desc(self):
        numbers = [number for number in range(self.size * self.size)]
        random.shuffle(numbers)
        self._desc = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                elem = numbers.pop()
                if elem == 0:
                    self.zero_x = i
                    self.zero_y = j
                row.append(elem)
            self._desc.append(row)
        self.not_placed_tiles = self.get_not_placed_tiles()

    def shuffle_desc(self, shuffle_number: int):
        i = 0
        last_operation = None
        while i < shuffle_number:
            try:
                operation_, func = random.choice(tuple(self.operations.items()))
                if self.opposite_operations[operation_] == last_operation:
                    raise Exceptions.MovingDescException()
                func(self, self.zero_x, self.zero_y)
                last_operation = operation_
                i += 1
            except Exceptions.MovingDescException:
                continue
        self.not_placed_tiles = self.get_not_placed_tiles()

    def change_tiles(self, x1, y1, x2, y2):
        assert self._desc[x1][y1] == 0 or self._desc[x2][y2] == 0, \
            "Trying to move TWO not zero tiles (x: {0}, y: {1}) (x: {2}, y: {3})".format(x1, y1, x2, y2)
        correct_1 = int(self.is_correct_tile(x1, y1)) + int(self.is_correct_tile(x2, y2))
        buffer = self._desc[x2][y2]
        self._desc[x2][y2] = self._desc[x1][y1]
        self._desc[x1][y1] = buffer

        correct_2 = int(self.is_correct_tile(x1, y1)) + int(self.is_correct_tile(x2, y2))
        self.not_placed_tiles += correct_2 - correct_1
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

    def get_not_placed_tiles(self):
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.is_correct_tile(i, j):
                    count += 1
        if self._desc[self.size - 1][self.size - 1] == 0:
            count -= 1
        return count

    def is_correct_tile(self, x, y):
        if self._desc[x][y] != (x * self.size) + (y + 1):
            return True
        return False

    def __str__(self):
        return "\n".join(map(str, self._desc))

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
