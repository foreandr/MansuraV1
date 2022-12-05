from Python.database import *

"""THIS IS BASICALLY TO ALLOW YOU TO RESET THE DATABASE OR MAKE EMEGENCY CHANGES"""

#test hello world
def UPDATE_USER_BALANCE():
    pass
    
def RESET_DATABASE():
    print("hello world")
    USER_FULL_RESET()

def DEMO_ACCOUNTS_REGISTER():
    full_register('dailyinsights', hashlib.sha256("hellodailyinsights123!".encode('utf-8')).hexdigest(), 'dailyinsights@gmail.com', 'dailyinsights@gmail.com', 5)
    full_register('royalkilla', hashlib.sha256("helloroyalkilla123!".encode('utf-8')).hexdigest(), 'royalkilla@gmail.com', 'royalkilla@gmail.com', 5)
    full_register('ghost_lover2021', hashlib.sha256("helloghost_lover2021123!".encode('utf-8')).hexdigest(), 'ghost_lover2021@gmail.com', 'ghost_lover2021@gmail.com', 5)
    full_register('johnlocke', hashlib.sha256("hellojohnlocke123!".encode('utf-8')).hexdigest(), 'johnlocke@gmail.com', 'johnlocke@gmail.com', 5)
    full_register('Twomanriot', hashlib.sha256("helloTwomanriot123!".encode('utf-8')).hexdigest(), 'Twomanriot@gmail.com', 'Twomanriot@gmail.com', 5)
    full_register('xerihm', hashlib.sha256("helloxerihm123!".encode('utf-8')).hexdigest(), 'xerihm@gmail.com', 'xerihm@gmail.com', 5)
    full_register('Ludus', hashlib.sha256("helloLudus123!".encode('utf-8')).hexdigest(), 'Ludus@gmail.com', 'Ludus@gmail.com', 5)

def DEMO_ACCOUNTS_SUBSCRIBE():
    MANSURA_SUBSCRIBE('dailyinsights')
    MANSURA_SUBSCRIBE('royalkilla')
    MANSURA_SUBSCRIBE('ghost_lover2021')
    MANSURA_SUBSCRIBE('johnlocke')
    MANSURA_SUBSCRIBE('Twomanriot')
    MANSURA_SUBSCRIBE('xerihm')


# DEMO_ACCOUNTS_REGISTER()
DEMO_ACCOUNTS_SUBSCRIBE()
# RESET_DATABASE()
