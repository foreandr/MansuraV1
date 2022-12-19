try:    
    import python.MODULES as modules
except:
    import MODULES as modules

def CREATE_TABLES():
    modules.CREATE_TABLE_USER()
    modules.CREATE_TABLE_CATEGORIES()
    modules.CREATE_TABLE_POST()
    modules.CREATE_TABLE_POST_CATEGORY()
    modules.CREATE_TABLE_TAGS()
    modules.CREATE_TABLE_LIKES()
    # modules.CREATE_TABLE_DISLIKES()
    modules.CREATE_TABLE_FAVOURITES()
    modules.CREATE_TABLE_COMMENTS()
    modules.CREATE_TABLE_VIEWS()
    modules.CREATE_TABLE_CONNECTIONS()
    modules.CREATE_TABLE_IP_ADRESSES()
    modules.CREATE_TABLE_CHAT_ROOMS()
    modules.CREATE_TABLE_CHAT_ADMINS()
    modules.CREATE_TABLE_CHAT_USERS()
    # BLOCKS
    # REQUESTS
    # TAG REQUESTS
    # POST REQUESTS
    # CATEGORY REQUESTS
    
def FULL_RESET():
    CREATE_TABLES()
    
if __name__ == "__main__":
    FULL_RESET()