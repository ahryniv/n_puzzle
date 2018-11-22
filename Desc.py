import random
import Exceptions


class Desc:
    def __init__(self, desc=None, size=3):
        self.zero_x, self.zero_y = None, None
        if desc:
            self._desc = desc
        else:
            self.size = size
            self._desc = self._create_correct_desc()

    def _create_correct_desc(self):
        numbers = [number for number in range(1, self.size * self.size + 1)]
        numbers[-1] = 0
        self.zero_x, self.zero_y = self.size - 1, self.size - 1
        return [numbers[i*self.size:(i+1)*self.size] for i in range(self.size)]

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
        return self._desc

    def shuffle_desc(self, shuffle_number: int):
        i = 0
        last_operation = None
        while i < shuffle_number:
            try:
                operation_, func = random.choice(tuple(self.operations.items()))
                if self.opposite_operations[operation_] == last_operation:
                    raise Exceptions.MovingDescException()
                func(self, self.zero_x, self.zero_y)
                # print("({0}, {1}) - {2}".format(self.zero_x, self.zero_y, operation_))
                last_operation = operation_
                i += 1
            except Exceptions.MovingDescException:
                continue

    def move_up_element(self, x, y):
        try:
            if x < 1 or (self._desc[x - 1][y] != 0 and self._desc[x][y] != 0):
                raise Exceptions.MovingDescException("Can't move this up (x: {0}, y: {1})".format(x, y))
        except IndexError:
            raise Exceptions.MovingDescException("Can't move this up (x: {0}, y: {1})".format(x, y))
        buffer = self._desc[x - 1][y]
        self._desc[x - 1][y] = self._desc[x][y]
        self._desc[x][y] = buffer
        self.zero_x, self.zero_y = (x, y) if self._desc[x][y] == 0 else (x - 1, y)

    def move_down_element(self, x, y):
        try:
            if self._desc[x + 1][y] != 0 and self._desc[x][y] != 0:
                raise Exceptions.MovingDescException("Can't move this down (x: {0}, y: {1})".format(x, y))
        except IndexError:
            raise Exceptions.MovingDescException("Can't move this down (x: {0}, y: {1})".format(x, y))
        buffer = self._desc[x + 1][y]
        self._desc[x + 1][y] = self._desc[x][y]
        self._desc[x][y] = buffer
        self.zero_x, self.zero_y = (x, y) if self._desc[x][y] == 0 else (x + 1, y)

    def move_right_element(self, x, y):
        try:
            if self._desc[x][y + 1] != 0 and self._desc[x][y] != 0:
                raise Exceptions.MovingDescException("Can't move this right (x: {0}, y: {1})".format(x, y))
        except IndexError:
            raise Exceptions.MovingDescException("Can't move this right (x: {0}, y: {1})".format(x, y))
        buffer = self._desc[x][y + 1]
        self._desc[x][y + 1] = self._desc[x][y]
        self._desc[x][y] = buffer
        self.zero_x, self.zero_y = (x, y) if self._desc[x][y] == 0 else (x, y + 1)

    def move_left_element(self, x, y):
        try:
            if y < 1 or (self._desc[x][y - 1] != 0 and self._desc[x][y] != 0):
                raise Exceptions.MovingDescException("Can't move this left (x: {0}, y: {1})".format(x, y))
        except IndexError:
            raise Exceptions.MovingDescException("Can't move this left (x: {0}, y: {1})".format(x, y))
        buffer = self._desc[x][y - 1]
        self._desc[x][y - 1] = self._desc[x][y]
        self._desc[x][y] = buffer
        self.zero_x, self.zero_y = (x, y) if self._desc[x][y] == 0 else (x, y - 1)

    def get_not_placed_tiles(self):
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if self._desc[i][j] != (i * self.size) + (j + 1):
                    count += 1
        if self._desc[self.size - 1][self.size - 1] == 0:
            count -= 1
        return count

    def __str__(self):
        return "\n".join(map(str, self._desc))

    def __getitem__(self, item):
        return self._desc[item]

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
