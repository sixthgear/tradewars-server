#!./env/bin/python


if __name__ == '__main__':
    
    import signal
    import sys        
    from tw import game
    
    g = game.Game()
    
    def signal_handler(signal, frame):
        g.shutdown()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)    
    g.run(4000)