import os
import random

def random_line(filename):
    """
    Generator to open a large file and yield random lines from it.
    This should be very memory efficent and quick, since we do
    not read the whole file, just seek to a random spot and return
    the next full line.
    """
    with open(filename,'r') as file:
        size = os.stat(filename)[6]
        while True:
            # pick a random byte from the file, wrap around to file size
            n = random.randint(0,size - 1) % size
            file.seek(n)
            # read a dummy-line. We do this to make sure that our random seek
            # didn't stick us in the middle of a line.
            file.readline()            
            yield file.readline().strip()
