import commerce
    
class Market(object):
    """
    A class designed to contain a simple supply/demand market model.    
    TODO: everything.
    """
    def __init__(self, world):
        """
        Build inital market conditions for the passed world object
        """
        self.world = world
        self.contracts = []
        