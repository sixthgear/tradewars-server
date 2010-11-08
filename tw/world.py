import collections

Point = collections.namedtuple('Point', 'x y')

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

def name_generator():
    for name in planet_names:
        yield name

ng = name_generator()


class World(object):
    def __init__(self):
        self.planets = []
                
class Planet(object):
    def __init__(self):
        self.name = ng.next()
        self.position = Point(0, 0)
        self.credits = 0
        self.supply = {}
        self.production = {}
        self.consumption = {}
        self.contracts = []
        
class Player(object):
    """
    """
    def __init__(self, connection=None):
        self._connection = connection
        self.name = 'Player'
        self.position = Point(0, 0)
        self.credits = 1000
        self.capacity = 1000
        self.cargo = {}
        self.contracts = []
        self.command_queue = []
        self.output_queue = []
        
    def output(self, data):
        self.output_queue.append(data)
    
    def flush(self):
        while self.output_queue:
            data = self.output_queue.pop(0)
            self._connection.socket.send(data)
                
    def __repr__(self):
        return self.name
                