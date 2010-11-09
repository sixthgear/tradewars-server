Draft of the Market Model
=========================

- Planet
    - Each Resource
        - supply:       the real units owned by the planet
        
        - production:   the rate at which the supply changes every turn. planets 
                        with negative production rates are considered to be net 
                        consumers of that resource.

- Market
    - Each Resource:
        - price_index:  tricky but maybe vital!?
                        ESTIMATED market price for this resource. This is 
                        calculated using total universal supply and production 
                        rates, along with the results of contracts. Local 
                        factors such as transportation distance and local supply 
                        are ignored here.
                     
        - supply:       sum of all planets total supply of this resource
        
        - production:   sum of the universal net production rate for this 
                        resource

- Resource
    - shelf life:       unsure about this variable, but this may help make more
                        dynamic market activity. This is the number of turns                
                        that this resource will persist for after being created.    
                        It may be too difficult to model directly, but may be 
                        used as a fudge rate for determining pricing in 
                        oversupply situations. It also may be used to calculate
                        contract size, as materials with high shelf lives can be 
                        hoarded, while short shelf lives need to be bought on 
                        demand.                    
                        
Game Setup
----------

1.  For each planet, for each material, create initial supply and determine production rate. Let's use perlin or simplex noise here to create some peaks and valleys. In general we want to make sure that each planet is a net producer of total units, so that we don't get any global recession situations. Hopefully that for every resource that has a negative production rate somewhere, we also have another producer of that resource elsewhere. 
    
2.  Try to create an initial price index for each resource. This will be tricky to estimate, but perhaps there is a simple formula we can use based on the global supply and global production rate.
    
3.  When setting prices, planets may look at the distance to the nearest producer or consumer as a price modifier. We may want to build a quick planet distance lookup table so that we don't need to do tons of sqrts() every turn.

Each Turn
---------

1.  Modify local supply for each planet's resources by using the production rate.

2.  Examine recent contract results and try to determine if the current market price is accurate. 

Things that might cause the market price to increase:
    
    - SELL contracts completed at higher than list value
    - SELL contracts filled quickly, assuming contract price >= market price    
    - BUY contracts persisting for > 10 turns, assuming contract price >= market 
      price
    
Things that might cause the market price to decrease:
    
    - BUY contracts completed at lower than list value
    - BUY contracts filled quickly, if contract price <= market price
    - SELL contracts persisting for > 10 turns, if contract price <= market 
      price

3.  Check for contract conditions. Create contracts if required.

If local supply is lower than threshold rmin, and the planet has a non-positive production rate, the planet has a chance of creating a BUY  contract this turn if one does not already exist. If one exists, there is a chance of increasing the price of that contract.
    
If local supply is greater than threshold rmax and the planet has a non-negative production rate the planet has a chance of creating a SELL contract this turn if one does not already exist. If one exists, there is a chance of reducing the price of that contract.
    
The price for this contract is created using the following factors:
    
    - market price index - this is the baseline
    - turns left before zero-supply, or spoilage
    - distance from nearest net producer/consumer - this might be unnecessary
    
    
Questions
--------- 

The simplest model may be to make it so that production rates never change. This will still be challenging for bots, because they enter the game with no knowledge of market conditions, and will need to observe contracts to determine who produces and who consumes. The question is whether this is an accurate enough market simulation, which of course reacts to countless variables and may see many local and global price changes.

In a static model like this, there should be a price equilibrium somewhere, and it will just take a certain number of turns to reach that equilibrium assuming bots behave rationally.

If we decide to change production rates, how can we model that? I'm not sure using noise to modify production rates is fair, because it then becomes much harder for bots to build a predictible simulation of future prices.
    
Perhaps vast oversupply and undersupply situations might be corrected dynamically, with a planet deciding to become a consumer or producer to try to correct this situation -- we do not however want to create a situation where all prices are generally the same!