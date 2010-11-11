import math
import random
import itertools
import collections
from util import files

Point = collections.namedtuple('Point', 'x y')

class Planet(object):
    """
    Represents a planet in the star system. All planets modelled by the game 
    have the ability to trade materials.
    """
    def __init__(self, name):
        self.name = name
        self.position = Point(0, 0)
        self.credits = 0
        self.supply = {}
        self.production = {}    
        self.contracts = []
        
    def __repr__(self):        
        return self.name
        

class StarSystem(object):
    """
    Model of a single star system where our game takes place. Planet position is 
    measured in gigameters. Our system will have a possible area of approx. 
    10000^2 Gm. For reference, the Aphelion of Neptune (the outermost planet in 
    the Sol System is 4,554 Gm, which gives our virtual planets roughly the same 
    area to work in. We strangely stick a planet at (0,0), the spot you'd expect 
    to see the star of the system, but since we aren't modelling orbits, or
    sticking a trading post in the sun, this should be ok.
    """
    
    def __init__(self):
        self.planets = []
        self.distance_map = {}
    
    def randomize(self, n_planets=8):
        """
        Build an inital population of planets.       
        """ 
        ng = files.random_line('data/planets.txt')       
        for i in range(n_planets):
            p = Planet(name=ng.next())
            if i != 0:
                p.position = Point(
                    random.randrange(-5000, 5000), 
                    random.randrange(-5000, 5000)
                )
            p.credits = 100000
            self.planets.append(p)            
        
        self.build_distance_map()
        # print self.distance_map
        
    
    def build_distance_map(self):
        """
        Caches a distance map from each planet to every other planet.
        This is an integer representing the number of turns it would take to 
        reach that planet assuming a speed of 1000 Gm per turn.
        """        
        for a,b in itertools.combinations(self.planets, 2):
            if not self.distance_map.has_key(a):
                self.distance_map[a] = {}
            if not self.distance_map.has_key(b):
                self.distance_map[b] = {}                
            dx2 = (b.position.x - a.position.x) ** 2
            dy2 = (b.position.y - a.position.y) ** 2
            dist = int((math.ceil(math.sqrt(dx2 + dy2) / 1000)))
            self.distance_map[a][b] = dist
            self.distance_map[b][a] = dist
                
