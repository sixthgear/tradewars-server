import random
import math
import itertools
import commerce
    
class Market(object):
    """
    A class designed to contain a simple supply/demand market model.    
    TODO: everything.
    """
    def __init__(self, world):
        self.world = world
        self.contracts = []
        self.prices = {}
        self.supply = {}
        self.production = {}
        self.materials = list(commerce.material_names)[:5]

    def randomize(self):
        """
        Build inital market conditions for the passed world object
        """
        
        # zero supply and production for all available materials
        for p,m in itertools.product(self.world.planets, self.materials):
            p.production[m] = 0
            p.supply[m] = 1000
                    
        # iterate 1000 times. perhaps we can use some noise here instead
        for i in range(1000):
            
            a = random.choice(self.world.planets)
            b = random.choice(self.world.planets)
            m = random.choice(self.materials)
            if a == b: continue
            
            production_delta = random.randrange(0,20)
            supply_delta = production_delta * 2
            
            # make opposing production modifications for this material
            # that means if we make one planet a producer, another must
            # become a consumer. We add a small bias to the positive side
            # so that economy is slightly inflationary in general.
            
            a.production[m] = a.production.get(m,0) + production_delta + 1
            b.production[m] = b.production.get(m,0) - production_delta
            a.supply[m] = a.supply.get(m,0) + supply_delta
            b.supply[m] = b.supply.get(m,0) - supply_delta
        
        # update our global supply and production totals for each resource
        for p,m in itertools.product(self.world.planets, self.materials):
            self.production[m] = self.production.get(m,0) + p.production[m]
            self.supply[m] = self.supply.get(m,0) + p.supply[m]
        
                
    def update(self):        
        
        # loop through every possible planet-material combination
        for p,m in itertools.product(self.world.planets, self.materials):

            supply = p.supply[m]
            production = p.production[m]

            # modify local supply based on production rate
            p.supply[m] = max(0, supply + production)
            self.supply[m] = max(0, self.supply[m] + production)
            
            if production < 0:
                
                turns_left = supply / -production
                amount_for_20 = -production * 20
                price = 10 * (6-turns_left)
                
                if turns_left > 5: continue
                
                # find existing contracts
                existing = [x for x in self.contracts if 
                    x.material == m and 
                    x.planet == p and
                    x.owner == None and
                    x.type == commerce.BUY
                ]
                                         
                if not existing:
                    self.issue(commerce.BUY, p, m, amount_for_20, price)
                else:
                    existing[0].price = price
                    existing[0].amount = amount_for_20
                    
            elif production > 0:    
                
                if supply < 2000: continue                
                price = 10 * (1 + (supply-2000)/production)
                amount = (supply / 500) * 500
                    
                # find existing contracts
                existing = [x for x in self.contracts if 
                    x.material == m and 
                    x.planet == p and
                    x.owner == None and
                    x.type == commerce.SELL
                ]
                                        
                if not existing:                    
                    self.issue(commerce.SELL, p, m, amount, price)                
                else:
                    existing[0].price = price
                    existing[0].amount = amount
                    
            else:
                pass
                
    def issue(self, type, planet, material, amount, price):
        c = commerce.Contract()
        c.id = len(self.contracts)
        c.planet = planet
        c.type = type
        c.material = material        
        c.amount = amount
        c.price = price
        self.contracts.append(c)
        
                                
    def output(self):
        print 'MARKET'
        for m in self.materials:
            print '    %s %s %s' % (
                m.ljust(12), 
                str(self.production[m]).rjust(6), 
                str(self.supply[m]).rjust(6))
        print \
            str(sum(self.production.values())).rjust(23) + \
            str(sum(self.supply.values())).rjust(7)
        print '~'        
        print 'PLANETS'        
        for p in self.world.planets:
            print p.name
            for m in self.materials:
                print '    %s %s %s' % (
                    m.ljust(12), 
                    str(p.production[m]).rjust(6), 
                    str(p.supply[m]).rjust(6))
        print '~'
        print 'CONTRACTS'
        for c in self.contracts:
            print c
        print '~'
            
            
        
if __name__ == '__main__':
    """
    Dumbass market sim ticker.
    """
    import world
    w = world.World()
    
    print 'PLANETS'
    for i in range(4):
        p = world.Planet()
        
        if i != 0:
            p.position = world.Point(
                random.randrange(-10000, 10000), 
                random.randrange(-10000, 10000)
            )
        w.planets.append(p)
        print p
    print '~'
            
    market = Market(w)
    market.randomize()
    tick = 0
    
    while True:
        tick += 1
        print 'TURN %d' % tick
        
        market.update()
        market.output()
        command = raw_input('#')