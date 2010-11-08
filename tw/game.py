import collections
from tornado import ioloop
import server
import market
import parser

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
        self.cargo = []
        self.contracts = []
        
    def __repr__(self):
        return self.name

class Game(object):
    """
    Main Game controller object.
    """
    
    def __init__(self):
        self.tick = 0
        self.players = {}
        self.planets = []        
        self.timer = None
        self.server = None
        
    def on_start(self): 
        print 'TW is ready to rock on port %d.' % self.server.port
        
    def on_stop(self): 
        print 'Server stopped.'
        
    def on_read(self, connection, data): 
        command = data.strip()        
        print parser.parse(command)
        
    def add_player(self, connection):
        """
        Called whenever the server has a new connection.
        """
        p = Player(connection)
        p.name = 'Player %d' % connection.fileno()
        self.players[connection.fileno()] = p
        print '%s has connected.' % p.name
        
    def update(self):
        """
        Called every 1500ms.
        """
        self.tick += 1
        
        # 1. read connections
        # 2. parse commands
        # 3. update game state
        # 4. simulate market
        # 5. write to connections
                
        print 'sending tick %d...' % self.tick
        self.server.sendall('TURN %d\n' % self.tick)

            
    def run(self, port=1337):
        self.server = server.Server(port)
        self.server.on_new_connection = self.add_player
        self.server.on_start = self.on_start
        self.server.on_stop = self.on_stop
        self.server.on_read = self.on_read
        
        self.timer = ioloop.PeriodicCallback(self.update, 1500)
        self.timer.start()        
        self.server.start()
        ioloop.IOLoop.instance().start()
    
    def shutdown(self):
        print 'Shutting down...'
        self.timer.stop()
        self.server.stop()
        ioloop.IOLoop.instance().stop()