from base64 import encode
import hashlib
import inspect
import datetime
 
try:    
    import python.MODULES as modules
except:
    import MODULES as modules


def INSERT_USER(username, password, Email):
    check_profanity_user  = modules.USERNAME_PROFANITY_CHECK(username)
    check_injection_pass = modules.CHECK_INJECTION(password)
    check_injection_user = modules.CHECK_INJECTION(username)
    
    if not (check_profanity_user and check_injection_pass and check_injection_user):
        return False
    
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO USERS
            (Username, Password, Profile_pic, Email,User_Strikes, Date_time, User_first_time)
            VALUES
            (%(username)s, %(password)s, %(pic)s, %(email)s, 0, NOW(), 'True')
            
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
    
def INSERT_PERSON(Person_name, Person_live="True"):
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO PEOPLE
            (Person_name, Person_live)
            VALUES
            (%(Person_name)s, %(Person_live)s)
            ON CONFLICT DO NOTHING
            """, {'Person_name': Person_name,
                  'Person_live': Person_live,
                  }
            )
        conn.commit()

        modules.print_green(F"{Person_name} INSERT COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)  
    
def INSERT_POST_ADMIN(User_id):
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO MODERATION_ADMINS
            (User_id)
            VALUES
            ('{User_id}')
            ON CONFLICT DO NOTHING
            """
            )
        conn.commit()

        modules.print_green(F"{User_id} INSERT COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)  
   
def INSERT_POST(Post_title, Post_description, Post_link, Post_live, Person, User_id=1):
    # print(Person)
    if not modules.CHECK_ACCOUNT_STATUS(User_id):
        print(User_id, F"is suspended for now. CANT {inspect.stack()[0][3]}")
        return ""
        
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
            (Post_title, Post_description, Post_link, Post_html, Post_live, User_id, Date_Time)
            VALUES
            (%(Post_title)s, %(Post_description)s, %(Post_link)s, %(Post_html)s, %(Post_live)s, %(User_id)s, NOW());
            """, {'Post_title': Post_title,
                  'Post_description': Post_description, 
                  'Post_link':Post_link, 
                  'Post_html':Post_html,
                  'Post_live':Post_live,
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
   
def INSERT_SUBJECTS(Subject_name):
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO SUBJECTS
            (Subject_name)
            VALUES
            (%(Subject_name)s)
            """, {

                'Subject_name': Subject_name
                }
            )
        conn.commit()

        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn) 

def INSERT_POST_SUBJECTS(Subject_id, Post_id):
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO POST_SUBJECTS
            (Subject_id, Post_id)
            VALUES 
            ('{Subject_id}', '{Post_id}')
            """)
        conn.commit()

        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

def LIKE_LOGIC(Post_id, User_id):
    already_liked = modules.CHECK_LIKE_EXISTS(Post_id, User_id)
    if already_liked:
        #print( User_id, "has already liked",Post_id)
        modules.DELETE_LIKE(Post_id, User_id)
    else:
        modules.INSERT_LIKE(Post_id, User_id)
        
def COMMENT_LIKE_LOGIC(Comment_id, User_id):
    already_liked_comment = modules.CHECK_COMMENT_LIKE_EXISTS(Comment_id, User_id)
    if already_liked_comment:
        #print( User_id, "has already liked",Post_id)
        modules.DELETE_FROM_COMMENT_LIKES(Comment_id, User_id)
    else:
        modules.INSERT_COMMENT_VOTE(Comment_id, User_id)

def CONNECTION_LOGIC(User_id1, User_id2):
    already_following = modules.CHECK_CONNECTION_EXISTS(User_id1, User_id2)
    if already_following:
        #print( User_id, "has already liked",Post_id)
        modules.DELETE_CONNECTION(User_id1, User_id2)
    else:
        modules.INSERT_CONNECTION(User_id1, User_id2)

def FAVE_LOGIC(Post_id, User_id):
    already_liked = modules.CHECK_FAVE_EXISTS(Post_id, User_id)
    if already_liked:
        #print( User_id, "has already faved",Post_id)
        modules.DELETE_FAVOURITE(Post_id, User_id)
    else:
        modules.INSERT_FAVOURITES(Post_id, User_id)
    
def SEARCH_FAVE_LOGIC(Search_algorithm_id, User_id):
    already_saved = modules.CHECK_SEARCH_FAVE_EXISTS(Search_algorithm_id, User_id)
    # print(already_saved)
    if already_saved:
        #print( User_id, "has already faved",Post_id)
        modules.DELETE_SEARCH_FAVOURITE(Search_algorithm_id, User_id)
    else:
        modules.INSERT_SEARCH_FAVOURITES(Search_algorithm_id, User_id)

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

def INSERT_COMMENT_VOTE(Comment_id, User_id):
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO COMMENT_VOTES
            (Comment_id, User_id, Date_time)
            VALUES
            (%(Comment_id)s, %(User_id)s, NOW())
            
            ON CONFLICT DO NOTHING
            """, {
                'Comment_id': Comment_id,
                'User_id': User_id,
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
    # print(Post_id, User_id)
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
    
def INSERT_SEARCH_FAVOURITES(Search_algorithm_id, User_id):
    # print(Search_algorithm_id, User_id)
    cursor, conn =modules. create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO SEARCH_ALGORITM_SAVE
            (Search_algorithm_id, User_id, Date_time)
            VALUES
            (%(Search_algorithm_id)s, %(User_id)s, NOW())
            ON CONFLICT DO NOTHING
            """, {'Search_algorithm_id': Search_algorithm_id,
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
    if not modules.CHECK_ACCOUNT_STATUS(User_id):
        print(User_id, F"is suspended for now. CANT {inspect.stack()[0][3]}")
        return ""
        
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
    
    if not modules.CHECK_POST_IS_LIVE(Post_id):
        return False
        
    cursor, conn = modules.create_connection()
    can_view = CHECK_IF_BEEN_30s_SINCE_LAST_VIEW(Post_id, User_id)
    if not can_view:
        modules.close_conn(cursor, conn)
        return False
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

def INSERT_CHAT_REQUEST(user_name, room_id):
    user_id = modules.GET_USER_ID_FROM_NAME(user_name)
    cursor, conn = modules.create_connection()
    
    if modules.CHECK_USER_ID_ROOM_CREATOR(user_id, room_id):
        # print("This user is the creator")
        modules.INSERT_CHAT_ROOMS_USER(user_id, room_id)
        return ""
    
    cursor.execute(f"""
        INSERT INTO CHAT_ROOM_INVITES(Room_id, User_id,Date_time)
        VALUES 
        ('{room_id}', '{user_id}', NOW())  
        ON CONFLICT DO NOTHING
    """)
    conn.commit()
    modules.close_conn(cursor, conn)
    modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
     
def INSERT_CHAT_ROOMS(Creator_id, Room_name, list_of_names):

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
        room_id = modules.GET_ROOM_ID_BY_TITLE_AND_USER_ID(User_id=Creator_id, Room_name=Room_name)
        # print(list_of_names)
        #for i in list_of_names:
        #    print(i)
        
        for i in list_of_names:
            INSERT_CHAT_REQUEST(user_name=i, room_id=room_id)
            
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
            (%(User_id)s, %(Room_id)s)
            """, {'User_id': User_id,
                  'Room_id': Room_id
                })
        conn.commit()
        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn) 
    
def INSERT_REQUEST(User_id, Post_title, Description, Link, Person_name):
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO REQUESTS
            (User_id, Post_title, Description, Link, Person_name, Date_time)
            VALUES
            (%(User_id)s,%(Post_title)s, %(Description)s, %(Link)s,%(Person_name)s, NOW())
            """, {'User_id': User_id,
                  'Post_title':Post_title,
                  'Description':Description,
                  'Link':Link,
                  'Person_name':Person_name
                }
            )
        conn.commit()
        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)

def INSERT_SUBJECT_REQUEST(User_id, Subject,Post_id):
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO SUBJECT_REQUESTS
            (User_id, Subject,Post_id)
            VALUES
            (%(User_id)s, %(Subject)s, %(Post_id)s)
            """, {'User_id': User_id,
                  'Subject':Subject,
                  'Post_id':Post_id,
                }
            )
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

def INSERT_TRIBUNAL_WORD(word, User_id=1):
    if not CHECK_NEW_BANNED_WORD_IS_NOT_STUPID(word):
        return "" # exit function if stupid
    
    if not modules.CHECK_ACCOUNT_STATUS(User_id):
        print(User_id, F"is suspended for now. CANT {inspect.stack()[0][3]}")
        return ""
        
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
      
def INSERT_DEMO_WORD_LIST():
    word_list = modules.GET_ORIGINAL_PROFANITY_LIST()
    all_words = input("do you want all the words?")
   
    if all_words.lower() == "yes" or all_words.lower() == "y":
        max = 1000
    else: 
        max = 10
        
    for i in range(len(word_list)):
        if i > max:
            break  # 10 is just for demo testing functionality
        INSERT_TRIBUNAL_WORD(word_list[i])
        for j in range(10):
            INSERT_INTO_PROFANITY_LIST_VOTES(i, 1, "DOWN")
            
def INSERT_INTO_PROFANITY_LIST_VOTES(word_id, voter_id, vote_Type):
    if not modules.CHECK_ACCOUNT_STATUS(voter_id):
        print(voter_id, F"is suspended for now. CANT {inspect.stack()[0][3]}")
        return ""
    if voter_id == 1: # SO that on my account i can vote infinitely
        modules.INSERT_TRIBUNAL_WORD_VOTE(word_id, voter_id, vote_Type)     
        return ""
    if modules.CHECK_IF_WORD_VOTE_EXISTS(word_id, voter_id):
        modules.UPDATE_TRIBUNAL_WORD_VOTE(word_id, voter_id, vote_Type)
    else:
        modules.INSERT_TRIBUNAL_WORD_VOTE(word_id, voter_id, vote_Type)
     
def INSERT_TRIBUNAL_WORD_VOTE(word_id, voter_id, vote_type):
    if not modules.CHECK_ACCOUNT_STATUS(voter_id):
        print(voter_id, F"is suspended for now. CANT {inspect.stack()[0][3]}")
        return ""
    
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
        INSERT_PERSON(word_list[i], Person_live="True")
        
def brute_force_replace(string):
    new_string = ""
    for i in string:
        if i  == "'":
            # print("found apostrophe") 
            new_string += "\\'"
        else:
            new_string +=i    
    return new_string
            
def INSERT_SEARCH_ALGORITHM(Search_algorithm_name, Search_where_clause, Search_order_clause, User_id):
    #Search_where_clause = Search_where_clause.replace("'", "\'")
    #Search_order_clause = Search_order_clause.replace("'", "sadhgfajhsdgfkjahdfsgkjdfahsg")
    # Search_where_clause= brute_force_replace(Search_where_clause)
    if not modules.CHECK_ACCOUNT_STATUS(User_id):
        print(User_id, F"is suspended for now. CANT {inspect.stack()[0][3]}")
        return ""
    
    Search_algorithm_name = f"{modules.GET_USER_NAME_FROM_ID(User_id)}-{Search_algorithm_name}"
    modules.GET_USER_ID_FROM_NAME
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            INSERT INTO SEARCH_ALGORITHMS(Search_algorithm_name, Search_where_clause, Search_order_clause, User_id, Date_time)
            VALUES ('{Search_algorithm_name}', '{Search_where_clause}', '{Search_order_clause}', '{User_id}', NOW() )  
            ON CONFLICT DO NOTHING 
        """)
    
        conn.commit()
        modules.print_green(f"{inspect.stack()[0][3]} {Search_algorithm_name, Search_where_clause, Search_order_clause, User_id} COMPLETED")
        modules.close_conn(cursor, conn) 
    except Exception as e:
        print(e)

def INSERT_SEARCH_VOTE(Search_algorithm_id, User_id):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
        INSERT INTO SEARCH_ALGORITM_VOTES(Search_algorithm_id, User_id, Date_time)
        VALUES ('{Search_algorithm_id}', '{User_id}',  NOW())  
        ON CONFLICT DO NOTHING 
    """)
    
    conn.commit()
    modules.print_green(f"{inspect.stack()[0][3]} {User_id, Search_algorithm_id} COMPLETED")
    modules.close_conn(cursor, conn) 
    
def INSERT_CHAT_MESSAGE(User_id, Room_id, Message):
    cursor, conn = modules.create_connection()
    
    cursor.execute(f"""
        INSERT INTO CHAT_MESSAGES(User_id, Room_id, Date_time, Message)
        VALUES 
        (%(User_id)s, %(Room_id)s, NOW(), %(Message)s)  
    """, {'User_id': User_id,
          'Room_id': Room_id,
          'Message': Message})
    conn.commit()
    modules.close_conn(cursor, conn)
    modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    
def XOR_ENCRYPTION(text):
    # performing XOR operation on each value of bytearray
    text2 = bytearray(text,'utf-8')
    key = 1 
    for index, values in enumerate(text2):
        text2[index] = values ^ key 
           
    text2 = str(text2)
    text2 = text2.replace("bytearray(b'", "")
    text2 = text2[:-2]
    
    return text2
    
if __name__ == "__main__":
    text= 'hello world'
    text2 = XOR_ENCRYPTION(text)
    print(text2)
    
    text3 = XOR_ENCRYPTION(text2)
    print(text3)




