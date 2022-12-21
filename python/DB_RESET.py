try:    
    import python.MODULES as modules
except:
    import MODULES as modules

def CREATE_TABLES(server="false"):
    modules.CREATE_TABLE_USER()
    modules.CREATE_TABLE_PEOPLE()
    modules.INSERT_DEMO_PEOPLE()
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
    modules.CREATE_TABLE_TRIBUNAL_WORD()
    modules.INSERT_DEMO_WORD_LIST(server) # INSERTS
    modules.CREATE_TABLE_TRIBUNAL_WORD_VOTE()


def GET_ORIGINAL_PROFANITY_LIST():
    word_array = []
    f = open("/root/mansura/files/initial_profanity_insert.txt", "r")
    word_array = f.read().split("\n")[:-1]
    
    #for i in range(len(word_array)):
    #    print(i, word_array[i])
        
    return word_array

def GET_ORIGINAL_PEOPLE_LIST():
    word_array = []
    f = open("/root/mansura/files/db_people.txt", "r")
    word_array = f.read().split("\n")[:-1]
    
    #for i in range(len(word_array)):
    #    print(i, word_array[i])
        
    return word_array
       

def FULL_RESET(): 
    CREATE_TABLES("true")

    
if __name__ == "__main__":
    answer = input("DO YOU WANT TO REALLY RESET?")
    if answer.lower() in ["y", "yes"]:
        FULL_RESET()