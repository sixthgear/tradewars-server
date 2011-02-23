Things that each language client library should handle:

- simple blocking tcp socket client
    - try to use the standard library only if possible
    - tricky: socket.h vs winsock for C

- connect function
    - send authentication token

- data structures
    
    - list of planets
        - position
        
    - list of open contracts
        - buy or sell
        - material name (or id)
        - quantity
        - price
        
    - my player
        - position
        - credits
        - list of cargo
        - capacity limit
        - list of my open contracts

    - other players
        - position
    
- basic parser for game state information (see spec for format)

    - create list of planets
    - create list of players
    - create and update list of open contracts
    - update my player data (position, cargo, credits, contracts)

- wrapper functions (or at least stubs) for each of the possible commands
    1. Buy goods
    2. Sell goods
    3. Travel
    4. Issue contract
    5. Cancel contract
    6. Modify contract
    7. Idle
    
- simple game loop
    - read from socket (collect data and block until turn symbol "#" encountered)
    - parse and update game state
    - perform basic AI
    - write command to socket
    
- braindead AI
    - pick a random contract
    - fly to location
    - buy materials
    - wait until sell contract appears for that material
    - fly to location
    - sell materials
    - repeat

- don't bother with
    - time limits
    - anything fancy