Install Dependencies
--------------------
Requires pip:

    pip install -r ./docs/dependencies.txt
    

Install Dependencies with virtualenv
------------------------------------
The shebang (#!) line for launch.py points to ./env/bin/python, so if you 
use this method, and you launch the server from the shell with ./launch.py,
you will not need to setup any bootstrapping scripts.

Requires pip and virtualenv:

    pip -E env install -r ./docs/dependencies.txt
    
    
    
Start the server
----------------

    python launch.py [port]


