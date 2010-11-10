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
        self.materials = list(commerce.material_names)[:1]        
        self.id_gen = itertools.count()
    
    @property
    def credits(self):
        return sum([p.credits for p in self.world.planets])
            
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
            
            # randomly choose 2 planets and a material
            a = random.choice(self.world.planets)
            b = random.choice(self.world.planets)
            m = random.choice(self.materials)
            if a == b: continue
            
            # set a random production delta for this iteration
            production_delta = random.randrange(0,20)
            # modify supply by a smimilar factor, this is to encourage
            # planets to get inital contracts up early, so players
            # can quickly decide what to do
            supply_delta = production_delta * 2
            
            # make opposing production modifications for this material
            # that means if we make one planet a producer, another must
            # become a consumer. 
            
            # We add a small bias to the positive side
            # so that economy is slightly inflationary in general.
            # EDIT: this has been remove for study purposes
            
            a.production[m] = a.production.get(m,0) + production_delta # +1 bias
            b.production[m] = b.production.get(m,0) - production_delta
            a.supply[m] = a.supply.get(m,0) + supply_delta
            b.supply[m] = b.supply.get(m,0) - supply_delta
        
        # update our global supply and production totals for each resource
        for p,m in itertools.product(self.world.planets, self.materials):
            self.production[m] = self.production.get(m,0) + p.production[m]
            self.supply[m] = self.supply.get(m,0) + p.supply[m]
        
                
    def update(self):        
        
        # BUY AND SELL
        # to be replaced with players    
        buyers = [b for b in self.contracts if b.type == commerce.BUY]
        sellers = [s for s in self.contracts if s.type == commerce.SELL]        
        pending_deals = []
        self.completed_deals = []
        
        # build a list of pending deals, where there are matching buy and sell
        # contracts
        for b, s in itertools.product(buyers, sellers):            
            if b.planet == s.planet: continue
            if b.material != s.material: continue
            if b.price < s.price: continue            
            pending_deals.append((b,s))
        
        # shuffle so that the first few planets dont steal all the deals
        random.shuffle(pending_deals)
                
        # process each deal in order -- updating the contracts, and removing it
        # if complete. This is highly dependant on the order in which the pending 
        # deals list is built -- thats why we shuffle.
        for b,s in pending_deals:
            # we can only deal the lowest amount requested
            amount = min(b.amount, s.amount)
            price = (b.price * amount)
            m = b.material
            # looks like no more material is left, bummer
            if not amount: continue
            # modify planet supply
            b.planet.supply[m] += amount
            s.planet.supply[m] -= amount
            # modify planet credits
            b.planet.credits -= price
            s.planet.credits += price            
            # modify contracts
            b.amount -= amount
            s.amount -= amount
            # check if contracts should be removed
            if b.amount == 0:
                self.contracts.remove(b)
            if s.amount == 0:
                self.contracts.remove(s)                
            # add to completed deals list for output
            self.completed_deals.append((b,s, amount, price))
                    
        # CONTRACT GENERATION
        # loop through every possible planet-material combination
        for p,m in itertools.product(self.world.planets, self.materials):
            
            supply = p.supply[m]
            production = p.production[m]
            # modify local supply based on production rate
            p.supply[m] = max(0, supply + production)
            self.supply[m] = max(0, self.supply[m] + production)
            
            # new contracts -- only net consumers need to make BUY contracts
            # hopefully we can help planets decide to become middlemen
            # if their production rate is close to zero
            if production < 0:
                turns_left = supply / -production
                # buy when the current supply will run out in 5 turns
                if turns_left > 5: continue                
                type = commerce.BUY
                # buy enough, ideally to last for another 20 turns
                amount = -production * 20 - supply
                # set a price based on how close we are to running out
                price = min(50, 5 * (6-turns_left))
                
            # new contracts -- only net producers to make SELL contracts
            # hopefully we can help planets decide to become middlemen
            # if their production rate is close to zero
            elif production > 0:    
                type = commerce.SELL
                # only sell if we have more than 2000 units
                if supply < 2000: continue
                # sell as much as possible, in 500 unit increments
                amount = (supply / 500) * 500
                # start price naively at 50, and count down in fives
                price = max(5, 5 * (10 - (supply-2000)/production))
                
            # some planets may be production neutral for a given material
            else:                
                continue

            # find any existing contracts this planet has
            existing = [x for x in self.contracts if 
                x.material == m and 
                x.planet == p and
                x.owner == None and
                x.type == type
            ]

            # lets make a new contract
            if not existing:
                self.issue(type, p, m, amount, price)
            # lets just modify the old one
            # we may not allow the planets to change amounts in the real game
            # only prices            
            else:
                existing[0].price = price
                existing[0].amount = amount
            
            
    def issue(self, type, planet, material, amount, price):
        """
        Issue a contract
        """
        c = commerce.Contract()
        c.id = self.id_gen.next()
        c.planet = planet
        c.type = type
        c.material = material        
        c.amount = amount
        c.price = price
        self.contracts.append(c)
        
                                
    def output(self):
        """
        Hacky code to generate a simulation table on the terminal.
        """
        print 'DEALS'
        for b,s,amount,price in self.completed_deals:
            print '%s buys %d %s from %s for %dcR' % (
                b.planet.name,
                amount,
                b.material,
                s.planet.name,
                price)
        print '~'
        mn = 'MARKET (%dcR)' % self.credits
        print \
            mn.ljust(18) + \
            str(sum(self.production.values())).rjust(5) + \
            str(sum(self.supply.values())).rjust(7)
        print '-' * 30
        for m in self.materials:
            print '    %s %s %s' % (
                m.ljust(12), 
                str(self.production[m]).rjust(6), 
                str(self.supply[m]).rjust(6))
        print '~'        
        print 'PLANETS'
        for p in sorted(self.world.planets, key=lambda x: x.name):
            pn = '%s (%dcR)' % (p.name, p.credits)
            print \
                pn.ljust(16) + \
                str(sum(p.production.values())).rjust(7) + \
                str(sum(p.supply.values())).rjust(7)
            print '-' * 30
            for m in self.materials:
                print '    %s %s %s' % (
                    m.ljust(12), 
                    str(p.production[m]).rjust(6), 
                    str(p.supply[m]).rjust(6))
            print
            
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
        p.credits = 100000
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