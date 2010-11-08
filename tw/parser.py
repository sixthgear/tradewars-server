import commands

verbs = {
    'buy': commands.buy,
    'sell': commands.sell,
    'issue': commands.issue,
    'cancel': commands.cancel,
    'modify': commands.modify,
    'travel': commands.travel,
    'idle': commands.idle    
}

def parse(command):
    world = None
    player = None
    tokens = command.lower().split()
    verb = tokens[0]
    
    if verbs.has_key(verb):
        return verbs[verb](world, player, *tokens[1:])        
    else:
        return 'error'