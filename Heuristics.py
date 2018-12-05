class HeuristicNotPlacedTiles:
    name = "Not placed tiles"

    def __init__(self):
        pass

    @staticmethod
    def calculate(desc):
        return desc.not_placed_tiles


class HeuristicManhattan:
    name = "Manhattan"

    def __init__(self):
        pass

    @staticmethod
    def calculate(desc):
        return desc.all_manhattan


class HeuristicLinearConflictWithManhattan:
    name = "Linear conflict with Manhattan"

    def __init__(self):
        pass

    @staticmethod
    def calculate(desc):
        return desc.calculate_linear_conflict() + desc.all_manhattan


class HeuristicCountLessTiles:
    name = "Count less tiles"

    def __init__(self):
        pass

    @staticmethod
    def calculate(desc):
        return desc.count_all_less_tiles() + desc.all_manhattan
