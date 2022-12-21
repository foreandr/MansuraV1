try:    
    import python.MODULES as modules
except:
    import MODULES as modules

def CREATE_TABLES():
    modules.CREATE_TABLE_USER()
    modules.CREATE_TABLE_PEOPLE()
    modules.CREATE_TABLE_POST()
    modules.CREATE_TABLE_POST_PERSON()
    modules.CREATE_TABLE_SUBJECTS()
    modules.CREATE_TABLE_LIKES()
    # modules.CREATE_TABLE_DISLIKES()
    modules.CREATE_TABLE_FAVOURITES()
    modules.CREATE_TABLE_COMMENTS()
    modules.CREATE_TABLE_VIEWS()
    modules.CREATE_TABLE_CONNECTIONS()
    modules.CREATE_TABLE_BLOCKS()
    modules.CREATE_TABLE_IP_ADRESSES()
    modules.CREATE_TABLE_CHAT_ROOMS()
    modules.CREATE_TABLE_CHAT_ADMINS()
    modules.CREATE_TABLE_CHAT_USERS()
    modules.CREATE_TABLE_REQUESTS()
    modules.CREATE_TABLE_1_TIME_PASSWORDS()


    
def FULL_RESET():
    CREATE_TABLES()
    
if __name__ == "__main__":
    FULL_RESET()