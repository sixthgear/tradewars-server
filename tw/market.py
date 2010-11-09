import math
import itertools
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
        self.prices = {}
        self.supply = {}
        self.production = {}
        self.materials = list(commerce.material_names)[:5]
        for p,m in itertools.product(self.world.planets, self.materials):
            p.production[m] = random.randrange(-100,100)
            p.supply[m] = random.randrange(0,2500)
            self.production[m] = self.production.get(m,0) + p.production[m]
            self.supply[m] = self.supply.get(m,0) + p.supply[m]
                
    def update(self):        
        
        for p,m in itertools.product(self.world.planets, self.materials):

            supply = p.supply[m]
            production = p.production[m]

            p.supply[m] = max(0, supply + production)
            self.supply[m] = max(0, self.supply[m] + production)
            
            if production < 0:
                
                turns_left = supply / -production
                amount_for_20 = -production * 20
                price = 10 * (6-turns_left)
                
                if turns_left > 5: continue
                
                pcb = filter(
                    lambda x: x.material==m and x.planet==p and x.type==0,
                    self.contracts)                
                
                if not pcb:
                    self.issue(commerce.BUY, p, m, amount_for_20, price)
                else:
                    pcb[0].price = price
                    pcb[0].amount = amount_for_20
                    
            elif production > 0:    
                
                if supply < 2000: continue
                
                price = 10 * (1+ (supply-2000)/production)
                amount = (supply / 500) * 500
                                
                pcs = filter(
                    lambda x: x.material==m and x.planet==p and x.type==1, 
                    self.contracts)                    
                if not pcs:                    
                    self.issue(commerce.SELL, p, m, amount, 20)                
                else:
                    pcs[0].price = price
                    pcs[0].amount = amount
                    
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
        print 'TOTAL SUPPLY %d' % sum(self.supply.values())
        print 'TOTAL PRODUCTION %d' % sum(self.production.values())        
        for m in self.materials:
            print '%s P%d S%d' % (m, self.production[m], self.supply[m])            
        for p in self.world.planets:
            print p.name
            for m in self.materials:
                print '    %s P%d S%d' % (m, p.production[m], p.supply[m])
        print '~'
        print 'CONTRACTS'
        for c in self.contracts:
            print c
        print '~'
            
            
        
if __name__ == '__main__':
    """
    Dumbass market sim ticker.
    """
    import random
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
    tick = 0
    
    while True:
        tick += 1
        print 'TURN %d' % tick
        
        market.update()
        market.output()
        command = raw_input('#')