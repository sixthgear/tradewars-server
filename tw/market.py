import commerce
    
class Market(object):
    """
    A class designed to contain a simple supply/demand market model.
    
    TODO: everything.
    
    Market:
        Resource:
            supply = sum(planets-resouces supply)
            demand = sum(planets-resouces supply)
    
    Planet:
        Resource:
            consumption
            supply
            demand
            production
    """
    def __init__(self, world):
        """
        Build inital market conditions for the passed world object
        """
        self.world = world
        self.contracts = []
        