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
        # desc._calculate_all_manhattan()
        return desc.all_manhattan
