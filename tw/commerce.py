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