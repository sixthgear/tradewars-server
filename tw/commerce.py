BUY, SELL = range(2)

material_names = set((
    'ammunition',
    'fuel ore',
    'medicine',
    'minerals',
    'mutagens',
    'nuclides',
    'optics',
    'organics', 
    'alloys',
    'robotics',
    'stimulants',
    'vespene',
))

class Contract(object):
    """
    A contract is a request to buy or sell a particular amount of a particular 
    good at a particular price at a certain location (whew). Issuing and 
    completing contracts is the basis for all trading that occurs in the game. 
    Contracts may be issued on any turn by either the internal market model, or 
    by the players themselves. At the start of every turn, players will be 
    informed of all the currently open contracts on the market.
    """
    def __init__(self):
        self.id = 0
        self.turn_created = 0
        self.planet = None
        self.owner = None
        self.type = BUY
        self.material = ''
        self.amount = 0
        self.price = 0

    def __repr__(self):
        r = (
            str(self.id).ljust(4), 
            self.planet.name.ljust(11), 
            ('SELL' if self.type else 'BUY').ljust(5), 
            self.material.ljust(12), 
            str(self.amount).rjust(5), 
            (str(self.price)+'cR').rjust(5)
        )        
        return '%s %s %s %s %s %s' % r