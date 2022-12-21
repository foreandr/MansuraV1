try:    
    import python.MODULES as modules
except:
    import MODULES as modules


    
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
        
        elif function == "CREATE_TABLE_TRIBUNAL_WORD":
            cursor.execute("""DROP TABLE IF EXISTS TRIBUNAL_WORD CASCADE""")
            modules.print_segment()
        
        elif function == "CREATE_TABLE_TRIBUNAL_WORD_VOTE":
            cursor.execute("""DROP TABLE IF EXISTS TRIBUNAL_WORD_VOTE CASCADE""")
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
     
