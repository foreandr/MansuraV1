try:    
    import python.MODULES as modules
except:
    import MODULES as modules

from better_profanity import profanity
    
def SERVER_CHECK(server, function):
    # print()
    cursor, conn = modules.create_connection()
    if server == "false":
        if function == "CREATE_TABLE_USER":
            cursor.execute("""DROP TABLE IF EXISTS USERS CASCADE""")
            modules.print_segment()
        
        elif function == "CREATE_TABLE_PEOPLE":
            cursor.execute("""DROP TABLE IF EXISTS PEOPLE CASCADE""")
            modules.print_segment()
        
        elif function == "CREATE_TABLE_POST":
            cursor.execute("""DROP TABLE IF EXISTS POSTS CASCADE""")
            modules.print_segment()
        
        elif function == "CREATE_TABLE_SUBJECTS":
            cursor.execute("""DROP TABLE IF EXISTS SUBJECTS CASCADE""")
            modules.print_segment()
        
        elif function == "CREATE_TABLE_LIKES":
            cursor.execute("""DROP TABLE IF EXISTS LIKES CASCADE""")
            modules.print_segment()
        
        elif function == "CREATE_TABLE_DISLIKES":
            cursor.execute("""DROP TABLE IF EXISTS DISLIKES CASCADE""")
            modules.print_segment()
        
        elif function == "CREATE_TABLE_COMMENTS":
            cursor.execute("""DROP TABLE IF EXISTS COMMENTS CASCADE""")
            modules.print_segment()
        
        elif function == "CREATE_TABLE_VIEWS":
            cursor.execute("""DROP TABLE IF EXISTS VIEWS CASCADE""")
            modules.print_segment()
        
        elif function == "CREATE_TABLE_CONNECTIONS":
            cursor.execute("""DROP TABLE IF EXISTS CONNECTIONS CASCADE""")
            modules.print_segment()
        
        elif function == "CREATE_TABLE_IP_ADRESSES":
            cursor.execute("""DROP TABLE IF EXISTS IP_ADRESSES CASCADE""")
            modules.print_segment()
            
        elif function == "CREATE_TABLE_CHAT_ROOMS":
            cursor.execute("""DROP TABLE IF EXISTS CHAT_ROOMS CASCADE""")
            modules.print_segment()
        
        elif function == "CREATE_TABLE_CHAT_ADMINS":
            cursor.execute("""DROP TABLE IF EXISTS CHAT_ADMINS CASCADE""")
            modules.print_segment()
        
        elif function == "CREATE_TABLE_POST_PERSON":
            cursor.execute("""DROP TABLE IF EXISTS POST_PERSON CASCADE""")
            modules.print_segment()
        
        elif function == "CREATE_TABLE_FAVOURITES":
            cursor.execute("""DROP TABLE IF EXISTS FAVOURITES CASCADE""")
            modules.print_segment()
            
        elif function == "CREATE_TABLE_CHAT_USERS":
            cursor.execute("""DROP TABLE IF EXISTS CHAT_USERS CASCADE""")
            modules.print_segment()
            
        elif function == "CREATE_TABLE_BLOCKS":
            cursor.execute("""DROP TABLE IF EXISTS BLOCKS CASCADE""")
            modules.print_segment()
            
        elif function == "CREATE_TABLE_REQUESTS":
            cursor.execute("""DROP TABLE IF EXISTS REQUESTS CASCADE""")
            modules.print_segment()
            
        elif function == "CREATE_TABLE_1_TIME_PASSWORDS":
            cursor.execute("""DROP TABLE IF EXISTS ONE_TIME_PASSWORDS CASCADE""")
            modules.print_segment()
             
        conn.commit()
        modules.print_green(F"CASCADE DROPPED TABLE {function}")
        
def CHECK_IF_MOBILE(request):
    devices = ["Android", "webOS", "iPhone", "iPad", "iPod", "BlackBerry", "IEMobile", "Opera Mini"]
    result = False
    try:
        if any (device in request.environ["HTTP_USER_AGENT"] for device in devices): 
            result = True 
        # print("REQUEST AGENT:", request.environ["HTTP_USER_AGENT"], result)
        return result
    except Exception as e:
        modules.log_function("error", e)
        return result
    
    
def USERNAME_PROFANITY_CHECK(word, testing=False): #todo: this is particular to username
    print("CHECKING USERNAME FOR BADWORDS: ", type(word), {word})
    
    if testing:
        f = open("bad_words_username.txt", "r")
    else:
        f = open("Python/bad_words_username.txt", "r")
        
    
 # print(word[0])
        
    # NO IDEA WTF IS GOING ON WITH THE LIST SHIT
    # word = word[0] #TODO: MUST BE ON 
    # print("word:", word)
    # BASIC CHECK IF == TO ANY
    bad_words = f.read().split(",")
    for i in bad_words:
        if i != "" and i != " ":
            if i in word:
                print(F"FOUND {i} in {word} {len(i)}")
                return True
            else:
                pass
                #print("NOT FOUND",i, {len(i)})
    # 1. my word check
    if word.lower() in bad_words:
        print("it is in list of bad words")
        return True
        
    # 2. simple profanity check
    if profanity.contains_profanity(word):
        print("DETECTED BY PROFTANITY LIBRARY")
        return True
        
    # 3. spaces check
    if ' ' in word:
        print("THERE IS A SPACE IN ", word)
        return True
        
    # 4: 20 CHARS
    if len(word) > 20:
        print(f"{word} TOO LONG: {len(word)}")
        return True       
    
    #5 ALPHANUMERIC
    if any(not c.isalnum() for c in word):
        print(f"{word} has non alphanumeric chracters, cant in name")
        return True
    
    return False