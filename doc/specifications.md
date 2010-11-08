TW2012 Specifications (working title, don’t sue us!)
====================================================
 
1. Game Overview
----------------
 
### Objective ###
 
TW2012 is a loose interpretation of a BBS door game called TradeWars 2002. The game has been modified to simplify the rules, and is designed to be played concurrently by several remote AI scripts, rather than human players.
 
Each game will last approximately 20 minutes. During that 20 minutes, 600 turns will be executed with each AI player performing one action on every turn.
 
Each AI player controls a cargo ship, which can be used to navigate a map of various planets and star systems. Each of these locations has a list of goods that they wish to buy or sell. 
 
The goal of each game is to formulate and execute a strategy to acquire the most credits before the final turn is complete. Credits are obtained by buying goods, transporting them to another planet  in the universe, and (hopefully!) selling them for a higher price than they were purchased for.
 
### Market Model ###
 
Part of the challenge of this game is that the market model will be hidden from players. It will be governed by a set of simple rules and a few key initial variables that will be randomly determined before the start of every game. The most successful AIs will be expected to be able to determine the nuances of this model through indirect observation during the game.
 
2. Rules
--------
        
### Players ###
 
From here on, “player” refers to a a game character controlled by a remote AI program. Players are represented in-game as a interstellar cargo ship.
 
Players begin the game with 1000 credits each, and an empty cargo hold capable of carrying up to 1000 units of material. The player occupies a position in space represented by an x y pair of integer coordinates.
 
### Planets ###
 
The universe will be populated by a number of planets. Planets also have a position represented by x y integer coordinates. The main hub planet will always be located at 0,0 and all players will start the game from this location. In order to conduct business with other planets, players must first travel there.
 
### Credits ###
 
Credits (cR) are the central currency of the universe. Credits may be exchanged for materials and vice-versa. Materials may not be traded for other materials. A player is not limited by the number of credits they may carry. 
 
### Materials ###
 
A number of materials will be created on the planets in the universe. The internal market model will determine if and when planets will issue contracts to buy or sell these materials. When a player buys materials, they are placed into that player’s cargo hold. The player may not exceed the capacity of their cargo hold.
 
### Contracts ###
 
A contract is a request to buy or sell a particular amount of a particular good at a particular price at a certain location (whew). Issuing and completing contracts is the basis for all trading that occurs in the game. Contracts may be issued on any turn by either the internal market model, or by the players themselves. At the start of every turn, players will be informed of all the currently open contracts on the market.
 
Once a contract is first issued, it will remain on the market until it is completed. The contract price may be modified on any turn by the player who issued it. SELL contracts may only be made cheaper, and BUY contracts may only be made more expensive.
 
Players who wish to issue contracts (in order to conduct business with other players) must first travel to any planet. From there they may issue a contract to buy or sell a given material for a given price to a given maximum number of units. The player must pay the entire price of the contract up-front (in materials for a SELL contract, or credits for a BUY contract) and leave them at the planet.
 
This contract will enter the market on the next turn, and all players in the game will be informed.
 
When the contract is completed in whole or in part (by another player performing a BUY or SELL action), the credits will exchange hands immediately. Any materials that are received by the planet as part of a player-issued BUY contract will remain at the planet until the buying player travels there and picks them up. 
 
Materials and credits from an expired contract will be returned to the original player, although in the case of materials left as part of an expired SELL contract, the player will need to travel back to the original planet to pick them up.
 
Players may renew expiring contracts from anywhere in the universe.
        
### Player Actions ###
        
Every turn, each AI player may perform ONE of the following actions.
 
1. Buy goods
2. Sell goods
3. Travel
4. Issue contract
5. Idle
 
### Buy Goods ###

Usage: BUY MATERIAL QTYMIN-QTYMAX PRICEPERUNIT

If you are located at a planet that has an open SELL contract for a good you desire, you may buy up to the maximum specified amount for the listed price, provided you have the available credits and cargo space. If you issue an invalid BUY command (the particular good is not available at this location, or you do not have enough credits, or you specify an invalid number) you lose your turn.
 
    BUY medicine 0-1300 15
 
### Sell Goods ###
 
 
Usage: SELL MATERIAL QTYMIN-QTYMAX PRICEPERUNIT
 
If you are located at a planet that has an open BUY contract for a good you possess, you may sell up to the maximum specified amount for the listed price, provided you have the available goods. If you issue an invalid SELL command (the particular good is not requested at this location, or you do not have enough supply, or you specify an invalid number) you lose your turn.
 
    SELL medicine 0-1200 15cR
        
### Travel ###
 
Begin travel to the specified planet. The travel time will be represented by a number of whole turns. The formula for travel time will be:
 
        dx = target_x - player_x
        dy = target_y - player_y
        distance = sqrt(dx² + dy²)
        turns = ceil(distance / 1000)

Example:

        TRAVEL hoth
        
 
### Issue Contract ###
 
This command will issue a contract at the players current location. The required parameters are type (buy or sell), material, price per unit, and amount.
 
    ISSUE BUY robotics 57 1000
    ISSUE SELL rations 100 1200
 
If the type of contract is BUY, the player issuing the contract must have enough credits to cover the transaction. These credits will be taken from that player and held in escrow at the planet until the contract is completed, whereupon they will be immediately transferred to the selling players account. The goods will remain at the planet until the buying player can return to the planet and pick them up.
 
If the type of contract is SELL, the player issuing the contract must have enough material to cover the transaction. These materials will be taken from that player and held in escrow at the planet until the contract is completed, whereupon they will be immediately transferred to the buying players cargo hold.
 
### Idle ###
 
    IDLE
 
Do nothing for one turn.
 

### Resolving Deadlocks while buying and selling ###

Sometimes two or more players wish to perform the same BUY or SELL action at the same time. When this happens, the deadlocked players will be ranked by the details of their offer, and then then each player in order will be given an opportunity to buy or sell, until the contract has been fulfilled.

#### Price per unit

The better the offered price, the higher priority a player will receive. This means that the highest offered price over list on a SELL contract, or the lowest offered price under list on a BUY contract.

#### Maximum cargo amount

Among players who have offered the same price, players who wish to buy or sell more material will receive precedence. A player who wishes to buy 1000 units of a material will receive his goods before someone who asks for 500.

#### Splitting the contract

Finally, if two or more players have offered the same price, and the same quantity, the rest of the contract will be split equally among the interested parties.

#### Minimum Amount ####

If at any point in the deadlock negotiation process the amount of goods involved for a player drops below the minimum, that player will drop out of contention for the contract. This may be useful to set a volume limit at which a deal is no longer profitable to proceed with. A player who forfeits the contract because of a minimum price will not be allowed to take a different action that turn.


3. Market Model
---------------
 
Wibbley-wobbley, supply and demandey stuff.
 
4. Protocol
------------
   
Players should connect to the game server via TCP socket. The game protocol is a very simple text one that resembles a MUD in a few ways.
 
### Login ###
 
Upon connection, the server will send a single line:
 
    AUTH
 
The player needs to immediately respond with the secret token that they received from the competition website upon registration.
 
From this point on, the client must remain silent unless asked for a command from the server. The client will know a command is expected when it receives a pound # symbol.
 
Any deviation from this protocol will result in disconnection.
 
### Initial Game Information ###
 
At the start of the game, the player will be given a list of planets and their coordinates. The programs should record this information and use it to calculate possible destinations and travel times. The list will be terminated by a line containing a single tilde ~ character.
        
    PLANETS
    hoth, 0, 0
    alderaan, 1034, 3455  
    kashyyk, 3440, -3000
    ~
 
### Turn Information ###
 
At the start of every turn, the player will be given a list of 
information about the current state of the universe.
 
### 1. Current turn number. ###
 
A single line of information with the word “TURN” followed by a space and an integer representing the current turn number.
 
    TURN 1
 
### 2. List of open contracts ###
 
The next set of data is a list of all open contracts on the market. This list will take the form of series of comma-separated values. The fields are: id, planet-name, type, material, credits-per-unit, quantity, turns-remaining. The list will be terminated by a line containing a single tilde ~ character.
 
    CONTRACTS
    1, hoth, BUY, robotics, 54, 4000, 5
    2, hoth, BUY, rations, 120, 2300, 6
    3, alderaan, BUY, medicine, 34, 1200, 9
    4, kashyyk, SELL, medicine, 16, 1300, 10
    ~
 
A unique contract id is given so that the player can determine easily which contracts have been created, modified or removed from turn to turn. 
 
### 3. Players ###
 
The final set of turn data is a list of player names, their current coordinates, and their total accumulated credits. The list will be terminated by a line containing a single tilde ~ character.
 
    PLAYERS
    sixthgear, 0, 0, 1200
    mjard, 156, -45, 5633
    islands, 3440, -3000, 6220
    ~

### 4. Private Information ###
    
    CARGO
    robotics, 750
    medicine, 200
    mutagens, 50
    ~    
    LAST SUCCESS 1000
    ~
    ERRORS
    ~

### 5. Ready ###
 
Finally the server will send a pound # symbol to inform the player that it is ready to receive its next action.

    #


5. Server Architecture
----------------------

    TODO