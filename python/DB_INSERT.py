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
            (%(username)s, %(password)s, %(pic)s, %(email)s, NOW())
            
            ON CONFLICT DO NOTHING
            """, {'username': username,
                  'password': hashlib.sha256(password.encode('utf-8')).hexdigest(), 
                  'pic':modules.psycopg2.Binary(modules.load_default_profile_pic()), 
                  'email':Email}
            )
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
            (%(Person_name)s)
            ON CONFLICT DO NOTHING
            """, {'Person_name': Person_name}
            )
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
            (%(Post_title)s, %(Post_description)s, %(Post_link)s, %(Post_html)s, %(User_id)s, NOW());
            """, {'Post_title': Post_title,
                  'Post_description': Post_description, 
                  'Post_link':Post_link, 
                  'Post_html':Post_html, 
                  'User_id':User_id
                  }
            )
            
            
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
            (%(Post_id)s, %(Person_id)s)
            """, {'Post_id': Post_id,
                  'Person_id': Person_id}
            )
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
            (%(Subject_name)s, %(Subject_type)s, %(Post_id)s)
            """, {
                'Post_id': Post_id,
                'Subject_type': Subject_type,
                'Subject_name': Subject_name
                }
            )
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
            (%(Post_id)s, %(User_id)s, NOW())
            """, {
                'Post_id': Post_id,
                'User_id': User_id
                }
            )
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
            (%(Comment_id)s, %(User_id)s, %(Vote_type)s, NOW())
            
            ON CONFLICT DO NOTHING
            """, {
                'Comment_id': Comment_id,
                'User_id': User_id,
                'Vote_type': Vote_type,
                })
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
            (%(Post_id)s, %(User_id)s, NOW())
            """, {'Post_id': Post_id,
                  'User_id': User_id
                  }

            )
        conn.commit()

        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)

def INSERT_FAVOURITES(Post_id, User_id):
    print(Post_id, User_id)
    cursor, conn =modules. create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO FAVOURITES
            (Post_id, User_id, Date_time)
            VALUES
            (%(Post_id)s, %(User_id)s, NOW())
            ON CONFLICT DO NOTHING
            """, {'Post_id': Post_id,
                  'User_id': User_id
                  }
            
            )
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
        if Replying_to_id == "NULL":
            cursor.execute(
                f"""
                INSERT INTO COMMENTS
                (Post_id, User_id, Comment_text, Date_time)
                VALUES
                (%(Post_id)s, %(User_id)s, %(Comment_text)s, NOW())
                """, {
                    'Post_id': Post_id,
                    'User_id': User_id,
                    'Comment_text': Comment_text
                    }
                
                )
        else:
            cursor.execute(
                f"""
                INSERT INTO COMMENTS
                (Post_id, User_id, Replying_to_id, Comment_text, Date_time)
                VALUES
                (%(Post_id)s, %(User_id)s, %(Replying_to_id)s, %(Comment_text)s, NOW())
                """, {
                    'Post_id': Post_id,
                    'User_id': User_id,
                    'Replying_to_id': int(Replying_to_id),
                    'Comment_text': Comment_text
                    }
                
                )
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
        WHERE views.Post_id = %(Post_id)s
        AND views.User_id = %(User_id)s
        
        -- TO GET THE MOST RECENT
        ORDER BY Date_time DESC
        LIMIT 2
        """, {
            'Post_id': Post_id,
            'User_id': User_id
              }
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
        # print('SECONDS BETWEEN RECENT VIEW AND NOW: ', now_seconds)
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
    #TODO: i would like to put some kind of sleep functionality here os people cant see thier view right away
    
    cursor, conn = modules.create_connection()
    can_view = CHECK_IF_BEEN_30s_SINCE_LAST_VIEW(Post_id, User_id)
    if not can_view:
        modules.close_conn(cursor, conn)
        # print("TIME BETWEEN VIEWS TOO SHORT") 
    else:
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                INSERT INTO VIEWS
                (Post_id, User_id, Date_time)
                VALUES
                (%(Post_id)s, %(User_id)s, NOW())
                """, {
                    'Post_id': Post_id,
                    'User_id': User_id
                    }
                
                )
            conn.commit()
            modules.print_green(F"{inspect.stack()[0][3]} {Post_id, User_id} COMPLETED")
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
                VALUES(%(user_id1)s, %(user_id2)s, NOW())
            """, {'user_id1': user_id1,
                  'user_id2': user_id2}
            )
        conn.commit()
        modules.print_green(f"CONNECTED {user_id1} -> {user_id2}")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
    
    modules.close_conn(cursor, conn) 
    
def INSERT_BLOCKS(user_id1, user_id2):

    cursor, conn = modules.create_connection()
    try:
        cursor.execute(f"""
            INSERT INTO BLOCKS (User_Id1, User_Id2, Date_time)
            VALUES(%(user_id1)s, %(user_id2)s, NOW())
            """, {'user_id1': user_id1,
            'user_id2': user_id2}
        )
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
            (%(Address)s, %(User_id)s)
            """, {'Address': Address,
                  'User_id': User_id
                  }
            )
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
            (%(Creator_id)s, %(Room_name)s)
            """, {'Creator_id': Creator_id,
                  'Room_name': Room_name}
            )
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
            (%(User_id)s, %(Room_id)s)
            """, {'User_id': User_id,
                  'Room_id': Room_id
                }
            )
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
            (%(word)s)
            ON CONFLICT DO NOTHING
            """, {'word': word})
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
     
def INSERT_TRIBUNAL_WORD_VOTE(word_id, voter_id, vote_type):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
        INSERT INTO TRIBUNAL_WORD_VOTE(Tribunal_word_id, User_id, Vote_Type)
        VALUES(%(word_id)s, %(voter_id)s, %(vote_type)s)
        ON CONFLICT DO NOTHING          
    """, {'word_id': word_id,
          'voter_id': voter_id,
          'vote_type': vote_type}
    )
    conn.commit()
    modules.print_green(f"{inspect.stack()[0][3]} {word_id, voter_id, vote_type} COMPLETED")
    modules.close_conn(cursor, conn)    
     
def INSERT_DEMO_PEOPLE():
    word_list = modules.GET_ORIGINAL_PEOPLE_LIST()
    for i in range(len(word_list)):
        INSERT_PERSON(word_list[i])

if __name__ == "__main__":
    INSERT_USER("coomerdoomer", "password", "coomerdoomer@gmail.com")
    INSERT_CONNECTION(1, 2)
    # INSERT_TRIBUNAL_WORD("faggotere")