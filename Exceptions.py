class DescException(Exception):
    pass


class MovingDescException(DescException):
    pass


class NotValidDesc(DescException):
    pass


class Unsolvable(DescException):
    pass
