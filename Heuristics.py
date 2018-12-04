class HeuristicNotPlacedTiles:
    def __init__(self):
        pass

    @staticmethod
    def calculate(desc):
        return desc.not_placed_tiles


class HeuristicManhattan:
    def __init__(self):
        pass

    @staticmethod
    def calculate(desc):
        return desc.all_manhattan


class HeuristicLinearConflictWithManhattan:
    def __init__(self):
        pass

    @staticmethod
    def calculate(desc):
        return desc.calculate_linear_conflict() + desc.all_manhattan


class HeuristicCountLessTiles:
    def __init__(self):
        pass

    @staticmethod
    def calculate(desc):
        return desc.count_all_less_tiles() + desc.all_manhattan
