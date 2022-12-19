from dbconnection import *
from helpers import *

    
def SERVER_CHECK(server, function):
    # print()
    cursor, conn = create_connection()
    if server == "false":
        if function == "CREATE_TABLE_USER":
            cursor.execute("""DROP TABLE IF EXISTS USERS CASCADE""")
            print_segment()
        
        elif function == "CREATE_TABLE_CATEGORIES":
            cursor.execute("""DROP TABLE IF EXISTS CATEGORIES CASCADE""")
            print_segment()
        
        elif function == "CREATE_TABLE_POST":
            cursor.execute("""DROP TABLE IF EXISTS POSTS CASCADE""")
            print_segment()
        
        elif function == "CREATE_TABLE_TAGS":
            cursor.execute("""DROP TABLE IF EXISTS TAGS CASCADE""")
            print_segment()
        
        elif function == "CREATE_TABLE_LIKES":
            cursor.execute("""DROP TABLE IF EXISTS LIKES CASCADE""")
            print_segment()
        
        elif function == "CREATE_TABLE_DISLIKES":
            cursor.execute("""DROP TABLE IF EXISTS DISLIKES CASCADE""")
            print_segment()
        
        elif function == "CREATE_TABLE_COMMENTS":
            cursor.execute("""DROP TABLE IF EXISTS COMMENTS CASCADE""")
            print_segment()
        
        elif function == "CREATE_TABLE_VIEWS":
            cursor.execute("""DROP TABLE IF EXISTS VIEWS CASCADE""")
            print_segment()
        
        elif function == "CREATE_TABLE_CONNECTIONS":
            cursor.execute("""DROP TABLE IF EXISTS CONNECTIONS CASCADE""")
            print_segment()
        
        elif function == "CREATE_TABLE_IP_ADRESSES":
            cursor.execute("""DROP TABLE IF EXISTS IP_ADRESSES CASCADE""")
            print_segment()
            
        elif function == "CREATE_TABLE_CHAT_ROOMS":
            cursor.execute("""DROP TABLE IF EXISTS CHAT_ROOMS CASCADE""")
            print_segment()
        
        elif function == "CREATE_TABLE_CHAT_ADMINS":
            cursor.execute("""DROP TABLE IF EXISTS CHAT_ADMINS CASCADE""")
            print_segment()
            
        conn.commit()
        print_green(F"CASCADE DROPPED TABLE {function}")