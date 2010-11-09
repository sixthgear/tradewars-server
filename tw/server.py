from tornado import ioloop
import socket
import fcntl
import errno

class Connection(object):
    """
    Connection object.
    """
    def on_connect(self): pass
    def on_close(self): pass
    def on_write(self, data): pass
    def on_read(self): pass
    def on_server_stop(self): pass
    
    def fileno(self):
        return self.socket.fileno()
        
    def __init__(self, socket, address):        
        self.socket = socket
        self.address = address
    
    def send(self, data):
        self.socket.send(data)
        
    def disconnect(self):
        self.socket.close()
            
class Server(object):
    """
    Basic multiplexing TCP server. Assign function to these monkey patched
    callbacks to allow your app to listen for connect and read events.
    """
    def on_start(self): pass
    def on_stop(self): pass
    def on_read(self, connection, data): pass
    def on_write(self, connection, data): pass
    def on_new_connection(self, connection): pass
    def on_dropped_connection(self, connection): pass
        
    def __init__(self, port, address="", io_loop=None):
    
        self.io_loop = io_loop or ioloop.IOLoop.instance()
        self._socket = None        
        self._started = False
        self._connections = {}
        self.bind(port, address="")
        self.port = port
        self.address = address
        
    def bind(self, port, address=""):
        """
        Bind the server to listen on a specified port.
        """
        assert not self._socket        
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        flags = fcntl.fcntl(self._socket.fileno(), fcntl.F_GETFD)
        flags |= fcntl.FD_CLOEXEC
        fcntl.fcntl(self._socket.fileno(), fcntl.F_SETFD, flags)        
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.TCP_NODELAY, 0)
        self._socket.setblocking(0)
        self._socket.bind((address, port))
        self._socket.listen(128)
            
    def start(self):
        """
        Starts this server in the IOLoop.
        """
        assert not self._started
        self._started = True            
        self.io_loop.add_handler(
            self._socket.fileno(),
            self.handle_connect,
            ioloop.IOLoop.READ)
        self.on_start()
        
    def stop(self):
        """
        """
        assert self._started
        self._started = False
        self.io_loop.remove_handler(self._socket.fileno())
        self._socket.close()
        self.on_stop()
        
    def handle_connect(self, fd, events):        
        """
        New connection
        """
        try:
            socket, address = self._socket.accept()
            c = Connection(socket, address)
            self._connections[c.fileno()] = c
            self.io_loop.add_handler(c.fileno(), self.handle_read, ioloop.IOLoop.READ)            
                        
        except socket.error, e:
            if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                raise
        
        self.on_new_connection(c)

    def handle_read(self, fd, events):
        """
        Data recieved from client
        """
        c = self._connections[fd]
                
        data = c.socket.recv(1024)

        if data:            
            self.on_read(c, data)
        else:
            # closed connection
            c.socket.close()
            del self._connections[fd]
            self.io_loop.remove_handler(fd)
            self.on_dropped_connection(c)


    def sendall(self, data):
        """
        Send data to all connections
        """
        for fd, c in self._connections.iteritems():
            nbytes = c.socket.send(data)