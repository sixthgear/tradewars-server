import collections

Point = collections.namedtuple('Point', 'x y')

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
    
    def disconnect(self):
        self._connection.disconnect
        self._connection = None
    
    def output(self, data):        
        if self._connection:
            self.output_queue.append(data)
    
    def flush(self):
        while self.output_queue:
            data = self.output_queue.pop(0)
            if self._connection:
                self._connection.send(data)
                
    def __repr__(self):
        return self.name

    # COMMANDS
    # Should these go here with the world context?
    
    def buy(self, world, contract, minimum, maxium, price):
        print 'BUY', self, world, contract, minimum, maxium, price
    
    def sell(self, world, contract, minimum, maxium, price):
        print 'SELL', self, world, contract, minimum, maxium, price
    
    def issue(self, world, type, resource, amount, price, contract=None):
        pass

    def cancel(self, world, contract):
        pass

    def modify(self, world, contract, price):
        pass

    def travel(self, world, destination):
        pass
    
    def idle(self, world):
        pass
