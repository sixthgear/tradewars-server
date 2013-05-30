# coding=UTF-8

def buy(world, player, contract, minimum, maxium, price):
    """
    Usage: BUY MATERIAL QTYMIN-QTYMAX PRICEPERUNIT

    If you are located at a planet that has an open SELL contract for a good you
    desire, you may buy up to the maximum specified amount for the listed
    price, provided you have the available credits and cargo space. If you issue
    an invalid BUY command (the particular good is not available at this
    location, or you do not have enough credits, or you specify an invalid
    number) you lose your turn.

    BUY medicine 0-1300 15
    """    
    print 'BUY', world, player, contract, minimum, maxium, price
    
def sell(world, player, contract, minimum, maxium, price):
    """
    Usage: SELL MATERIAL QTYMIN-QTYMAX PRICEPERUNIT

    If you are located at a planet that has an open BUY contract for a good you
    possess, you may sell up to the maximum specified amount for the listed 
    price, provided you have the available goods. If you issue an invalid SELL 
    command (the particular good is not requested at this location, or you do 
    not have enough supply, or you specify an invalid number) you lose your 
    turn.

    SELL medicine 0-1200 15    
    """
    print 'SELL', world, player, contract, minimum, maxium, price
    
def issue(world, player, type, resource, amount, price, contract=None):
    """
    This command will issue a contract at the players current location. The 
    required parameters are type (buy or sell), material, price per unit, and 
    amount.

        ISSUE BUY robotics 57 1000
        ISSUE SELL rations 100 1200

    If the type of contract is BUY, the player issuing the contract must have 
    enough credits to cover the transaction. These credits will be taken from 
    that player and held in escrow at the planet until the contract is 
    completed, whereupon they will be immediately transferred to the selling 
    players account. The goods will remain at the planet until the buying player 
    can return to the planet and pick them up.

    If the type of contract is SELL, the player issuing the contract must have 
    enough material to cover the transaction. These materials will be taken from 
    that player and held in escrow at the planet until the contract is 
    completed, whereupon they will be immediately transferred to the buying 
    players cargo hold.
        """
    pass

def cancel(world, player, contract):
    """
    This command will take a open contract that was issued by the player off the 
    market. 

    For a BUY contract, the credits paid will be returned immediately to the 
    player, minus 20%. 

    For a SELL contract the materials, minus 20% may be reclaimed at the planet 
    when the player next visits.

    This command may be used while located at any planet, even if it is not the 
    one where the player issued the contract.

    CANCEL 1
    """
    pass

def modify(world, player, contract, price):
    """
    This command will modify the price of an open contract that was issued by 
    the player. 

    For a BUY contract, the player may increase the price. The funds will be 
    transferred to the escrow immediately.

    For a SELL contract, the player may decrease the price, but not the 
    quantity.

    This command may be used while located at any planet, even if it is not the 
    one where the player issued the contract.

    MODIFY 1 67
    """
    pass

def travel(world, player, destination):
    """
    Begin travel to the specified planet. The travel time will be represented by 
    a number of whole turns. The formula for travel time will be:

        dx = target_x - player_x
        dy = target_y - player_y
        distance = sqrt(dx² + dy²)
        turns = ceil(distance / 1000)

    TRAVEL hoth    
    """
    pass
    
def idle(world, player):
    """
    Do nothing for one turn.
    """
    pass
