try:    
    import python.MODULES as modules
except:
    import MODULES as modules

def CREATE_TABLES(server="false"):
    if server == "true":
        modules.print_title(f"INSIDE SERVER, ONLY ADD NEW TABLES [{server}]")
    else:
        modules.print_title(f"DEVELOPING, RECREATING ALL TABLES [{server}]", )
        
    modules.CREATE_TABLE_USER(server)
    # modules.CREATE_TABLE_USER_STATUS(server)
    modules.CREATE_TABLE_PEOPLE(server)
    modules.CREATE_TABLE_POST(server)
    modules.CREATE_TABLE_POST_PERSON(server)
    modules.CREATE_TABLE_SUBJECTS(server)
    modules.CREATE_TABLE_POST_SUBJECTS(server)
    modules.CREATE_TABLE_LIKES(server)
    modules.CREATE_TABLE_FAVOURITES(server)
    modules.CREATE_TABLE_COMMENTS(server)
    modules.CREATE_TABLE_COMMENT_VOTES(server)
    modules.CREATE_TABLE_VIEWS(server)
    modules.CREATE_TABLE_CONNECTIONS(server)
    modules.CREATE_TABLE_BLOCKS(server)
    modules.CREATE_TABLE_IP_ADRESSES(server)
    modules.CREATE_TABLE_CHAT_ROOMS(server)
    modules.CREATE_TABLE_CHAT_ROOM_INVITES(server)
    modules.CREATE_TABLE_CHAT_ADMINS(server)
    modules.CREATE_TABLE_CHAT_USERS(server)
    modules.CREATE_TABLE_CHAT_MESSAGES(server)
    modules.CREATE_TABLE_SUBJECT_REQUESTS(server)
    modules.CREATE_TABLE_1_TIME_PASSWORDS(server)
    modules.CREATE_TABLE_TRIBUNAL_WORD(server)
    modules.CREATE_TABLE_TRIBUNAL_WORD_VOTE(server)
    modules.CREATE_TABLE_MODERATION_ADMINS(server)
    modules.CREATE_TABLE_SEARCH_ALGORITHMS(server)
    modules.CREATE_TABLE_SEARCH_ALGORITM_VOTES(server)
    modules.CREATE_TABLE_CURRENT_USER_SEARCH_ALGORITHM(server)
    modules.CREATE_TABLE_SEARCH_ALGORITM_SAVE(server)
    
    
    if server != "true":
        modules.INSERT_DEMO_PEOPLE()
        modules.INSERT_DEMO_WORD_LIST() # INSERTS
    

def GET_ORIGINAL_PROFANITY_LIST():
    word_array = []
    f = open("/root/mansura/files/profanity_list.txt", "r")
    word_array = f.read().split(",")[:-1]
    
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
       
def FULL_LIVE_RESET(server="true"):
    answer = input(F"DO YOU WANT TO RESET [{server}]") 
    if answer.lower() == "y": 
        CREATE_TABLES(server=server)

    
if __name__ == "__main__":
    FULL_LIVE_RESET("true")
        