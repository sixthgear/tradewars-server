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

planet_names = set((
    'P1',
    'P2',
    'P3',
    'P4',
    'P5',
    'P6',
    'P7',
    'P8',
    'P9',
    'P10',
))

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
    def __init__(self):
        pass