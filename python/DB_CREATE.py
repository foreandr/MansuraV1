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
                    Email varchar(200) UNIQUE,
                    Date_time timestamp
                );
                """)
        conn.commit()
        modules.print_green("CREATE_TABLE_USER COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)    
    
    
def CREATE_TABLE_CATEGORIES(server="false"):
    cursor, conn = modules.create_connection()
    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3]) 
        cursor.execute(
            f"""
            CREATE TABLE CATEGORIES
            (
            Category_id SERIAL PRIMARY KEY,       
            Category_name varchar
            );
            """)
        conn.commit()
        modules.print_green("CREATE_TABLE_CATEGORIES COMPLETED\n")
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
            Post_link varchar, 
            Post_html varchar,
            User_id BIGINT,
            Date_Time timestamp,      
            FOREIGN KEY (User_id) REFERENCES USERS(User_id)
            );
            """)
        conn.commit()
        modules.print_green("CREATE_TABLE_POST COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    modules.close_conn(cursor, conn)
      
        
def CREATE_TABLE_POST_CATEGORY(server="false"):
    cursor, conn = modules.create_connection()
    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        # Path varchar,
        cursor.execute(
            f"""
            CREATE TABLE POST_CATEGORY
            (
            Post_id BIGINT,  
            Category_id BIGINT,     
            FOREIGN KEY (Post_id ) REFERENCES POSTS(Post_id),
            FOREIGN KEY (Category_id) REFERENCES CATEGORIES(Category_id)
            );
            """)
        conn.commit()
        modules.print_green("CREATE_TABLE_POST_CATEGORY COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    modules.close_conn(cursor, conn)


def CREATE_TABLE_TAGS(server="false"):
    cursor, conn = modules.create_connection()
    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
            f"""
            CREATE TABLE TAGS
            (
            Tag_id SERIAL PRIMARY KEY,       
            Tag_name varchar,
            Tag_type varchar,
            Post_id BIGINT, 
            FOREIGN KEY (Post_id) REFERENCES POSTS(Post_id),
            
            CHECK( Tag_type = 'HARD' OR Tag_type = 'SOFT'), 
                
                
                
            UNIQUE (Tag_name, Tag_type)
            );
            """)
        conn.commit()
        modules.print_green("CREATE_TABLE_TAGS COMPLETED\n")
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

        modules.print_green("LIKES CREATE COMPLETED\n")
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

        modules.print_green("FAVOURITES CREATE COMPLETED\n")
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

        modules.print_green("COMMENT CREATE COMPLETED\n")
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

        modules.print_green("VIEWS CREATE COMPLETED\n")
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
        modules.print_green("CONNECTION TABLE CREATE COMPLETED\n")
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
        modules.print_green("CONNECTION TABLE CREATE COMPLETED\n")
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

        modules.print_green("IP_ADRESSES CREATE COMPLETED\n")
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
                    FOREIGN KEY (Creator_id) REFERENCES USERS(User_id)
                );
                """)
        conn.commit()

        modules.print_green("CHAT_ROOMS CREATE COMPLETED\n")
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

        modules.print_green("CHAT_ADMINS CREATE COMPLETED\n")
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

        modules.print_green("CHAT_ADMINS CREATE COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)
    
    
def CREATE_TABLE_REQUESTS(server="false"):
    cursor, conn = modules.create_connection()

    try:
        modules.SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE REQUESTS(
                    User_id BIGINT,
                    Request_type varchar,
                    Request_content varchar,
                    Date_time timestamp,
                    
                    FOREIGN KEY (User_id) REFERENCES USERS(User_id),
                    
                    CHECK( Request_type = 'CATEGORY' 
                    OR Request_type = 'TAG'
                    OR Request_type = 'POST')
                );
                """)
        conn.commit()

        modules.print_green("CHAT_ADMINS CREATE COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")

    modules.close_conn(cursor, conn)    

 
