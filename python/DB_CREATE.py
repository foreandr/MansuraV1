try:    
    import python.MODULES as modules
except:
    import MODULES as modules

import inspect
      
def CREATE_TABLE_USER(server="false"):
    cursor, conn = modules.create_connection()
    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE USERS 
                (
                    User_id SERIAL PRIMARY KEY,
                    Username varchar(20) UNIQUE,
                    Password varchar(200),
                    Profile_pic BYTEA,
                    bio varchar,
                    Email varchar(200) UNIQUE,
                    Date_time timestamp,
                    User_Strikes INT,
                    User_mute_status varchar, 
                    User_timeout_status varchar,
                    User_ban_status varchar,
                    User_post_priority INT,
                    User_first_time varchar
                    
                );
                """)
        conn.commit()
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)    

def CREATE_TABLE_MODERATION_ADMINS(server="false"):
    cursor, conn = modules.create_connection()
    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE MODERATION_ADMINS
                (
                User_id BIGINT,
                FOREIGN KEY (User_id) REFERENCES USERS(User_id)
                );
                """)
        conn.commit()
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)   
    
def CREATE_TABLE_PEOPLE(server="false"):
    cursor, conn = modules.create_connection()
    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3]) 
        cursor.execute(
            f"""
            CREATE TABLE PEOPLE
            (
            Person_id SERIAL PRIMARY KEY,       
            Person_name varchar UNIQUE,
            Person_live varchar CHECK (Person_live = 'True'  OR Person_live = 'False' ),
            Person_description varchar
            )
            """)
        conn.commit()
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    modules.close_conn(cursor, conn)
           
def CREATE_TABLE_POST(server="false"):
    cursor, conn = modules.create_connection()
    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        # post links unique?
        cursor.execute(
            f"""
            CREATE TABLE POSTS
            (
            Post_id SERIAL PRIMARY KEY, 
            Post_title varchar, 
            Post_description varchar,
            Post_link varchar UNIQUE, 
            Post_html varchar,
            Post_live varchar,
            User_id BIGINT,
            Date_Time timestamp,      
            FOREIGN KEY (User_id) REFERENCES USERS(User_id)
            );
            """)
        conn.commit()
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    modules.close_conn(cursor, conn)
          
def CREATE_TABLE_POST_PERSON(server="false"):
    cursor, conn = modules.create_connection()
    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        # Path varchar,
        cursor.execute(
            f"""
            CREATE TABLE POST_PERSON
            (
            Post_id BIGINT,  
            Person_id BIGINT,     
            FOREIGN KEY (Post_id) REFERENCES POSTS(Post_id),
            FOREIGN KEY (Person_id) REFERENCES PEOPLE(Person_id)
            );
            """)
        conn.commit()
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    modules.close_conn(cursor, conn)

def CREATE_TABLE_SUBJECTS(server="false"):
    cursor, conn = modules.create_connection()
    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
            f"""
            CREATE TABLE SUBJECTS
            (
            Subject_id SERIAL PRIMARY KEY,       
            Subject_name varchar UNIQUE 
            );
            """)
        conn.commit()
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)

def CREATE_TABLE_POST_SUBJECTS(server="false"):
    cursor, conn = modules.create_connection()
    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
            f"""
            CREATE TABLE POST_SUBJECTS
            (
            Subject_id BIGINT,       
            Post_id BIGINT 
            );
            """)
        conn.commit()
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)  

def CREATE_TABLE_LIKES(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE LIKES(
                    Like_id SERIAL PRIMARY KEY,
                    Post_id BIGINT,
                    User_id BIGINT,
                    Date_time timestamp, 
                    FOREIGN KEY (Post_id) REFERENCES POSTS(Post_id),
                    FOREIGN KEY (User_id) REFERENCES USERS(User_id),
                    UNIQUE (Post_id,  User_id)
                );
                """)
        conn.commit()

        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)
    
def CREATE_TABLE_SEARCH_ALGORITHMS(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE SEARCH_ALGORITHMS(
                    Search_algorithm_id SERIAL PRIMARY KEY,
                    Search_algorithm_name varchar UNIQUE,
                    Search_where_clause varchar,
                    Search_order_clause varchar,
                    User_id BIGINT,
                    Date_time timestamp, 
                    FOREIGN KEY (User_id) REFERENCES USERS(User_id)
                );
                """)
        conn.commit()

        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)    
    
def CREATE_TABLE_SEARCH_ALGORITM_VOTES(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE SEARCH_ALGORITM_VOTES(
                    Search_vote_id SERIAL PRIMARY KEY,
                    Search_algorithm_id BIGINT,
                    User_id BIGINT,
                    Date_time timestamp, 
                    FOREIGN KEY (Search_algorithm_id) REFERENCES SEARCH_ALGORITHMS(Search_algorithm_id),
                    FOREIGN KEY (User_id) REFERENCES USERS(User_id)
                );
                """)
        conn.commit()

        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)
    
def CREATE_TABLE_SEARCH_ALGORITM_SAVE(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE SEARCH_ALGORITM_SAVE(
                    Search_save_id SERIAL PRIMARY KEY,
                    Search_algorithm_id BIGINT,
                    User_id BIGINT,
                    Date_time timestamp, 
                    FOREIGN KEY (Search_algorithm_id) REFERENCES SEARCH_ALGORITHMS(Search_algorithm_id),
                    FOREIGN KEY (User_id) REFERENCES USERS(User_id),
                    UNIQUE (User_id, Search_algorithm_id)
                );
                """)
        conn.commit()

        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)

def CREATE_TABLE_CURRENT_USER_SEARCH_ALGORITHM(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE CURRENT_USER_SEARCH_ALGORITHM(
                    Search_algorithm_id BIGINT,
                    User_id BIGINT UNIQUE,
                    FOREIGN KEY (Search_algorithm_id) REFERENCES SEARCH_ALGORITHMS(Search_algorithm_id),
                    FOREIGN KEY (User_id) REFERENCES USERS(User_id)
                );
                """)
        conn.commit()

        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)
          
'''
def CREATE_TABLE_DISLIKES(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE DISLIKES(
                    Dislike_id SERIAL PRIMARY KEY,
                    Post_id BIGINT,
                    User_id BIGINT,
                    Date_time timestamp,
                    FOREIGN KEY (Post_id) REFERENCES POSTS(Post_id),
                    FOREIGN KEY (User_id) REFERENCES USERS(User_id),
                    
                    UNIQUE (Post_id,  User_id)
                );
                """)
        conn.commit()

        modules.print_green("DISLIKES CREATE COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)
''' 
   
def CREATE_TABLE_FAVOURITES(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE FAVOURITES(
                    Favourite_id SERIAL PRIMARY KEY,
                    Post_id BIGINT,
                    User_id BIGINT,
                    Date_time timestamp, 
                    FOREIGN KEY (Post_id) REFERENCES POSTS(Post_id),
                    FOREIGN KEY (User_id) REFERENCES USERS(User_id),
                    UNIQUE (Post_id,  User_id)
                );
                """)
        conn.commit()

        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)
          
def CREATE_TABLE_COMMENTS(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE COMMENTS(
                    Comment_id SERIAL PRIMARY KEY,
                    Post_id BIGINT,
                    User_id BIGINT,
                    Replying_to_id BIGINT, 
                    Comment_text varchar,
                    Date_time timestamp,
                    FOREIGN KEY (Post_id) REFERENCES POSTS(Post_id),
                    FOREIGN KEY (User_id) REFERENCES USERS(User_id),
                    FOREIGN KEY (Replying_to_id) REFERENCES COMMENTS(Comment_id)
                );
                """)
        conn.commit()

        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)
  
def CREATE_TABLE_COMMENT_VOTES(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE COMMENT_VOTES(
                    Comment_vote_id SERIAL PRIMARY KEY,
                    Comment_id BIGINT,
                    User_id BIGINT,
                    Vote_type varchar,
                    Date_time timestamp, 
                    FOREIGN KEY (Comment_id) REFERENCES COMMENTS(Comment_id),
                    FOREIGN KEY (User_id) REFERENCES USERS(User_id),
                    UNIQUE (Comment_id,  User_id)
                );
                """)
        conn.commit()

        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)
        
def CREATE_TABLE_VIEWS(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE VIEWS(
                    Comment_id SERIAL PRIMARY KEY,
                    Post_id BIGINT,
                    User_id BIGINT,
                    Date_time timestamp,
                    FOREIGN KEY (Post_id) REFERENCES POSTS(Post_id),
                    FOREIGN KEY (User_id) REFERENCES USERS(User_id)
                );
                """)
        conn.commit()

        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)

def CREATE_TABLE_CONNECTIONS(server="false"):
    cursor, conn = modules.create_connection()
    
    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        # USERID1== FOLLOWER
        # USERID2== FOLLOWING
        cursor.execute(
            f"""
                CREATE TABLE CONNECTIONS
                (
                    Friendship_id SERIAL PRIMARY KEY,
                    User_id1 INT,
                    User_id2 INT,
                    Date_time timestamp,
                    
                    FOREIGN KEY (User_id1) REFERENCES USERS(User_id),
                    FOREIGN KEY (User_id2) REFERENCES USERS(User_id),
                    UNIQUE (User_id1,  User_id2)
                );
            """)
        conn.commit()
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
        
    modules.close_conn(cursor, conn)

def CREATE_TABLE_BLOCKS(server="false"):
    cursor, conn = modules.create_connection()
    
    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
            f"""
                CREATE TABLE BLOCKS
                (
                    Block_id SERIAL PRIMARY KEY,
                    User_id1 INT,
                    User_id2 INT,
                    Date_time timestamp,
                    
                    FOREIGN KEY (User_id1) REFERENCES USERS(User_id),
                    FOREIGN KEY (User_id2) REFERENCES USERS(User_id),
                    UNIQUE (User_id1,  User_id2)
                );
            """)
        conn.commit()
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
        
    modules.close_conn(cursor, conn)

def CREATE_TABLE_IP_ADRESSES(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE IP_ADRESSES(
                    Address_id SERIAL PRIMARY KEY,
                    Address varchar,
                    User_id BIGINT, 
                    FOREIGN KEY (User_id) REFERENCES USERS(User_id),
                    UNIQUE (Address,  User_id)
                );
                """)
        conn.commit()

        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)
       
def CREATE_TABLE_CHAT_ROOMS(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE CHAT_ROOMS(
                    Room_id SERIAL PRIMARY KEY,
                    Creator_id BIGINT,
                    Room_name varchar,
                    Date_time timestamp,
                    FOREIGN KEY (Creator_id) REFERENCES USERS(User_id),
                    UNIQUE(Creator_id, Room_name)
                );
                """)
        conn.commit()

        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)
    
def CREATE_TABLE_CHAT_ROOM_INVITES(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE CHAT_ROOM_INVITES(
                    Room_id BIGINT,
                    User_id BIGINT,
                    Date_time timestamp,
                    
                    FOREIGN KEY (Room_id) REFERENCES CHAT_ROOMS(Room_id),
                    FOREIGN KEY (User_id) REFERENCES USERS(User_id)
                );
                """)
        conn.commit()

        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)
    
def CREATE_TABLE_CHAT_ADMINS(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE CHAT_ADMINS(
                    User_id BIGINT,
                    Room_id BIGINT, 
                    FOREIGN KEY (User_id) REFERENCES USERS(User_id),
                    FOREIGN KEY (Room_id) REFERENCES CHAT_ROOMS(Room_id)
                );
                """)
        conn.commit()

        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)
     
def CREATE_TABLE_CHAT_USERS(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE CHAT_USERS(
                    User_id BIGINT,
                    Room_id BIGINT, 
                    FOREIGN KEY (User_id) REFERENCES USERS(User_id),
                    FOREIGN KEY (Room_id) REFERENCES CHAT_ROOMS(Room_id)
                );
                """)
        conn.commit()

        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)
    
def CREATE_TABLE_CHAT_MESSAGES(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE CHAT_MESSAGES(
                    User_id BIGINT,
                    Room_id BIGINT,
                    Date_time timestamp,
                    Message varchar,
                    FOREIGN KEY (User_id) REFERENCES USERS(User_id),
                    FOREIGN KEY (Room_id) REFERENCES CHAT_ROOMS(Room_id)
                );
                """)
        conn.commit()

        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)
    
def CREATE_TABLE_SUBJECT_REQUESTS(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE SUBJECT_REQUESTS(
                    User_id BIGINT,
                    Subject varchar,
                    Post_id BIGINT,

                    FOREIGN KEY (User_id) REFERENCES USERS(User_id),
                    FOREIGN KEY (Post_id) REFERENCES POSTS(Post_id)
                );
                """)
        conn.commit()

        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)  

def CREATE_TABLE_1_TIME_PASSWORDS(server="false"):
    cursor, conn = modules.create_connection()
    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute("""
            CREATE TABLE ONE_TIME_PASSWORDS
            (
                One_Time_id SERIAL PRIMARY KEY,
                Email varchar UNIQUE,
                Generated_Pass_Code varchar,
                FOREIGN KEY (Email) REFERENCES USERS(Email)
            );
        """)
        conn.commit()
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn) 
    
def CREATE_TABLE_TRIBUNAL_WORD(server="false"):
    cursor, conn = modules.create_connection()
    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute("""
            CREATE TABLE TRIBUNAL_WORD
            (
                Tribunal_word_id SERIAL PRIMARY KEY,
                Tribunal_word varchar UNIQUE
                
            );
        """)
        conn.commit()
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)  
    
def CREATE_TABLE_TRIBUNAL_WORD_VOTE(server="false"):
    cursor, conn = modules.create_connection()
    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute("""
            CREATE TABLE TRIBUNAL_WORD_VOTE
            (
                Tribunal_word_id BIGINT,
                User_id BIGINT,
                Vote_type varchar,
                CHECK(Vote_type = 'UP' OR Vote_type = 'DOWN')   
            );
        """)
        conn.commit()
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)         