import hashlib
import inspect
import datetime
 
try:    
    import python.MODULES as modules
except:
    import MODULES as modules


def INSERT_USER(username, password, Email):
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO USERS
            (Username, Password, Profile_pic, Email, Date_time)
            VALUES
            ('{username}', '{hashlib.sha256(password.encode('utf-8')).hexdigest()}', {modules.psycopg2.Binary(modules.load_default_profile_pic())}, '{Email}', NOW());
            """)
        conn.commit()

        modules.print_green(F"{username} INSERT COMPLETED")
        modules.close_conn(cursor, conn) 
        return True
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=f"{inspect.stack()[0][3]}")
        
    modules.close_conn(cursor, conn)  
    return False
    

def INSERT_PERSON(Person_name):
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO PEOPLE
            (Person_name)
            VALUES
            ('{Person_name}')
            ON CONFLICT DO NOTHING
            """)
        conn.commit()

        modules.print_green(F"{Person_name} INSERT COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)  
    
def INSERT_POST(Post_title, Post_description, Post_link, Person, User_id=1):
    
    cursor, conn = modules.create_connection()
    try:
        Post_html = modules.translate_link_to_html(Post_link)
        Post_title = modules.clean_title(Post_title)
        Post_description = modules.clean_description(Post_description)
        
        Person_id = modules.GET_PERSON_ID_BY_NAME(Person)
        
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO POSTS
            (Post_title, Post_description, Post_link, Post_html, User_id, Date_Time)
            VALUES
            ('{Post_title}', '{Post_description}', '{Post_link}', '{Post_html}', '{User_id}', NOW());
            """)
        conn.commit()
        
        Post_id = modules.GET_POST_ID_BY_LINK_AND_USER_ID(User_id, Post_link)
        INSERT_POST_PERSON(Post_id, Person_id)
        
        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn) 
     
def INSERT_POST_PERSON(Post_id, Person_id):
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO POST_PERSON
            (Post_id, Person_id)
            VALUES
            ('{Post_id}', '{Person_id}')
            """)
        conn.commit()

        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn) 
   
def INSERT_SUBJECTS(Subject_name, Subject_type, Post_id):
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO SUBJECTS
            (Subject_name, Subject_type, Post_id)
            VALUES
            ('{Subject_name}', '{Subject_type}', '{Post_id}')
            """)
        conn.commit()

        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn) 

def LIKE_LOGIC(Post_id, User_id):
    already_liked = modules.CHECK_LIKE_EXISTS(Post_id, User_id)
    if already_liked:
        #print( User_id, "has already liked",Post_id)
        modules.DELETE_LIKE(Post_id, User_id)
    else:
        modules.INSERT_LIKE(Post_id, User_id)

def FAVE_LOGIC(Post_id, User_id):
    already_liked = modules.CHECK_FAVE_EXISTS(Post_id, User_id)
    if already_liked:
        #print( User_id, "has already faved",Post_id)
        modules.DELETE_FAVOURITE(Post_id, User_id)
    else:
        modules.INSERT_FAVOURITES(Post_id, User_id)


def INSERT_LIKE(Post_id, User_id):
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO LIKES
            (Post_id, User_id, Date_time)
            VALUES
            ('{Post_id}', '{User_id}', NOW())
            """)
        conn.commit()

        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED {Post_id, User_id}")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn) 

def INSERT_COMMENT_VOTE(Comment_id, User_id, Vote_type):
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO COMMENT_VOTES
            (Comment_id, User_id, Vote_type, Date_time)
            VALUES
            ('{Comment_id}', '{User_id}', '{Vote_type}', NOW())
            
            ON CONFLICT DO NOTHING
            """)
        conn.commit()

        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED {Comment_id, User_id}")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn) 


def INSERT_DISLIKE(Post_id, User_id):
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO DISLIKES
            (Post_id, User_id, Date_time)
            VALUES
            ('{Post_id}', '{User_id}', NOW())
            """)
        conn.commit()

        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)

def INSERT_FAVOURITES(Post_id, User_id):

    cursor, conn =modules. create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO FAVOURITES
            (Post_id, User_id, Date_time)
            VALUES
            ('{Post_id}', '{User_id}', NOW())
            ON CONFLICT DO NOTHING
            """)
        conn.commit()
        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn) 
    

def INSERT_COMMENTS(Post_id, User_id, Comment_text, Replying_to_id="NULL"):
    Comment_text = modules.COMMENT_TEXT_CHECK(Comment_text)
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO COMMENTS
            (Post_id, User_id, Replying_to_id, Comment_text, Date_time)
            VALUES
            ('{Post_id}', '{User_id}', {Replying_to_id}, '{Comment_text}', NOW())
            """)
        conn.commit()
        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn) 
    
def CHECK_IF_BEEN_30s_SINCE_LAST_VIEW(Post_id, User_id):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
        SELECT Comment_id, Date_time
        FROM VIEWS views
        WHERE views.Post_id = '{Post_id}'
        AND views.User_id = '{User_id}'
        
        -- TO GET THE MOST RECENT
        ORDER BY Date_time DESC
        LIMIT 2
        """
    )
    results = []
    for i in cursor.fetchall():
        results.append([i[0], i[1]])
    modules.close_conn(cursor, conn)
    
    if len(results) != 2:
    # this means it returned 0 or 1 from the db, free to view 
        return True
    else:
        # SHOULD ADD LOGIC FOR BOT DETECTION LIKE
            # IF VIEW TIME DIFFERENCES ARE WITHIN 0.0010 MILISECONDS OR SOMETHING
        ct = datetime.datetime.now()
        now_seconds = (ct - results[0][1]).seconds
        print('SECONDS BETWEEN RECENT VIEW AND NOW: ', now_seconds)
        if now_seconds > 30:
            return True
        
        ''' WRONG LOGIC
        seconds = (results[0][1]-results[1][1]).seconds  # returns a timedelta object in seconds
        print('SECONDS BETWEEN VIEWS              : ', seconds)
        if seconds > 30:
            return True
        '''
        
    return False

    
def INSERT_VIEWS(Post_id, User_id):
    cursor, conn = modules.create_connection()
    can_view = CHECK_IF_BEEN_30s_SINCE_LAST_VIEW(Post_id, User_id)
    if not can_view:
        modules.close_conn(cursor, conn)
        print("TIME BETWEEN VIEWS TOO SHORT") 
    else:
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                INSERT INTO VIEWS
                (Post_id, User_id, Date_time)
                VALUES
                ('{Post_id}', '{User_id}', NOW())
                """)
            conn.commit()
            modules.print_green(F"{inspect.stack()[0][3]} {Post_id, User_id}COMPLETED")
        except Exception as e:
            cursor.execute("ROLLBACK")
            modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
        
        modules.close_conn(cursor, conn) 
    
    
def INSERT_CONNECTION(user_id1, user_id2):

    cursor, conn = modules.create_connection()
    try:
        cursor.execute(
            f"""
                INSERT INTO CONNECTIONS (User_Id1, User_Id2, Date_time)
                VALUES({user_id1}, {user_id2}, NOW())
            """)
        conn.commit()
        modules.print_green(f"CONNECTED {user_id1} -> {user_id2}")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
    
    modules.close_conn(cursor, conn) 
    

def INSERT_BLOCKS(user_id1, user_id2):

    cursor, conn = modules.create_connection()
    try:
        cursor.execute(
            f"""
                INSERT INTO BLOCKS (User_Id1, User_Id2, Date_time)
                VALUES({user_id1}, {user_id2}, NOW())
            """)
        conn.commit()
        modules.print_green(f"BLOCK {user_id1} -> {user_id2}")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
    
    modules.close_conn(cursor, conn)     


def INSERT_IP_ADRESSES(Address, User_id):

    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO IP_ADRESSES
            (Address, User_id)
            VALUES
            ('{Address}', '{User_id}')
            """)
        conn.commit()
        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)
    
    
def INSERT_CHAT_ROOMS(Creator_id, Room_name):

    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO CHAT_ROOMS
            (Creator_id, Room_name)
            VALUES
            ('{Creator_id}', '{Room_name}')
            """)
        conn.commit()
        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)
    
    
def INSERT_CHAT_ROOMS_USER(User_id, Room_id):

    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO CHAT_USERS
            (User_id, Room_id)
            VALUES
            ('{User_id}', '{Room_id}')
            """)
        conn.commit()
        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)
    
    
def INSERT_CHAT_ROOMS_ADMIN(User_id, Room_id):

    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO CHAT_ADMINS
            (User_id, Room_id)
            VALUES
            ('{User_id}', '{Room_id}')
            """)
        conn.commit()
        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn) 
    
    
def INSERT_REQUEST(User_id, Request_type, Request_content):

    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO REQUESTS
            (User_id, Request_type, Request_content, Date_time)
            VALUES
            ('{User_id}','{Request_type}', '{Request_content}', NOW())
            """)
        conn.commit()
        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)


def CHECK_NEW_BANNED_WORD_IS_NOT_STUPID(word):
    # TURN THIS INTO A FILE WITH A BIG LIST
    list_of_good_words = ["and", "or", "if"]
    if word in list_of_good_words:
        return False
    else:
        return True
def INSERT_TRIBUNAL_WORD(word):
    
    if not CHECK_NEW_BANNED_WORD_IS_NOT_STUPID(word):
        
        return "" # exit function if stupid
    
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO TRIBUNAL_WORD
            (Tribunal_word)
            VALUES
            ('{word}')
            ON CONFLICT DO NOTHING
            """)
        conn.commit()
        
        # CHECK IF WORD IN TXT FILE
        bad_words = modules.GET_ORIGINAL_PROFANITY_LIST()
        if word in bad_words:
            # print(word, "is a cuss word already")
            pass
        else:
            with open("/root/mansura/files/profanity_list.txt", "a") as f:
                f.write(f",{word}")
            # print(word, "is now in the cuss txt file")
        modules.print_green(F"{inspect.stack()[0][3]} [{word}] COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)        
      

          
def INSERT_DEMO_WORD_LIST(server="false"):
    word_list = modules.GET_ORIGINAL_PROFANITY_LIST()
    max = 10
    if server != "false":
        max = 1000 
        
    for i in range(len(word_list)):
        if i > max:
            break  # 10 is just for demo testing functionality
        INSERT_TRIBUNAL_WORD(word_list[i])
        for j in range(10):
            INSERT_INTO_PROFANITY_LIST_VOTES(i, 1, "DOWN")
            
         


def INSERT_INTO_PROFANITY_LIST_VOTES(word_id, voter_id, vote_Type):
    if voter_id == 1: # SO that on my account i can vote infinitely
        modules.INSERT_TRIBUNAL_WORD_VOTE(word_id, voter_id, vote_Type)     
        return ""
    

    if modules.CHECK_IF_WORD_VOTE_EXISTS(word_id, voter_id):
        modules.UPDATE_TRIBUNAL_WORD_VOTE(word_id, voter_id, vote_Type)
    else:
        modules.INSERT_TRIBUNAL_WORD_VOTE(word_id, voter_id, vote_Type)

     
           
def INSERT_TRIBUNAL_WORD_VOTE(word_id, voter_id, vote_Type):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
        INSERT INTO TRIBUNAL_WORD_VOTE(Tribunal_word_id, User_id, Vote_Type)
        VALUES('{word_id}', '{voter_id}', '{vote_Type}')
        ON CONFLICT DO NOTHING          
    """)
    conn.commit()
    modules.print_green(f"{inspect.stack()[0][3]} {word_id, voter_id, vote_Type} COMPLETED")
    modules.close_conn(cursor, conn)    
   
    
def INSERT_DEMO_PEOPLE():
    word_list = modules.GET_ORIGINAL_PEOPLE_LIST()
    for i in range(len(word_list)):
        INSERT_PERSON(word_list[i])


if __name__ == "__main__":
    INSERT_TRIBUNAL_WORD("faggotere")