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
            self.id, 
            self.planet.name, 
            'SELL' if self.type else 'BUY', 
            self.material, 
            self.amount, 
            self.price
        )
        
        return '%d %s %s %s %d %dcR' % r

        