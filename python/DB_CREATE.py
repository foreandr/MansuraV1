from dbconnection import *
from helpers import *
from log import *
from DB_CHECK import *
import inspect

#post title, post description
# post source
# post html

# user profile picture
#link providing peaderboards, watches views likes etcv
#both for the poster and the intellectuals

#todo: add to a DB_CHECK FILES

        
        
def CREATE_TABLE_USER(server="false"):
    cursor, conn = create_connection()
    try:
        SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE USERS 
                (
                    User_id SERIAL PRIMARY KEY,
                    Username varchar(20) UNIQUE,
                    Password varchar(200),
                    Email varchar(200) UNIQUE,
                    Date_time timestamp
                );
                """)
        conn.commit()
        print_green("CREATE_TABLE_USER COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name="USER_CREATE_TABLE")
    
    close_conn(cursor, conn)    
    
    
def CREATE_TABLE_CATEGORIES(server="false"):
    cursor, conn = create_connection()
    try:
        SERVER_CHECK(server, inspect.stack()[0][3]) 
        cursor.execute(
            f"""
            CREATE TABLE CATEGORIES
            (
            Category_id SERIAL PRIMARY KEY,       
            Category_name varchar
            );
            """)
        conn.commit()
        print_green("CREATE_TABLE_CATEGORIES COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name="CATEGORIES_CREATE_TABLE")
    close_conn(cursor, conn)
      
        
def CREATE_TABLE_POST(server="false"):
    cursor, conn = create_connection()
    try:
        SERVER_CHECK(server, inspect.stack()[0][3])
        # Path varchar,
        cursor.execute(
            f"""
            CREATE TABLE POSTS
            (
            Post_id SERIAL PRIMARY KEY,  
            Post_link varchar, 
            Post_html varchar,
            User_id BIGINT,
            Category_id BIGINT,
            Date_Time timestamp,      
            FOREIGN KEY (User_id) REFERENCES USERS(User_id),
            FOREIGN KEY (Category_id) REFERENCES CATEGORIES(Category_id)
            );
            """)
        conn.commit()
        print_green("CREATE_TABLE_POST COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name="POST_CREATE_TABLE")
    
    close_conn(cursor, conn)


def CREATE_TABLE_TAGS(server="false"):
    cursor, conn = create_connection()
    try:
        SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
            f"""
            CREATE TABLE TAGS
            (
            Tag_id SERIAL PRIMARY KEY,       
            Tag_name varchar UNIQUE,
            Tag_type varchar,
            Post_id BIGINT, 
            FOREIGN KEY (Post_id) REFERENCES POSTS(Post_id),
            
            CHECK( 
                Tag_type = 'HARD'
                OR Tag_type = 'SOFT' 
            )
            );
            """)
        conn.commit()
        print_green("CREATE_TABLE_TAGS COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name="TAGS_CREATE_TABLE")
    
    close_conn(cursor, conn)
    

def CREATE_TABLE_LIKES(server="false"):
    cursor, conn = create_connection()

    try:
        SERVER_CHECK(server, inspect.stack()[0][3])
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

        print_green("LIKES CREATE COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name="HAD TO ROLLBACK LIKES TABLE CREATION")

    close_conn(cursor, conn)
    
    
def CREATE_TABLE_FAVOURITES(server="false"):
    cursor, conn = create_connection()

    try:
        SERVER_CHECK(server, inspect.stack()[0][3])
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

        print_green("FAVOURITES CREATE COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name="HAD TO ROLLBACK FAVOURITES TABLE CREATION")

    close_conn(cursor, conn)
    
  
def CREATE_TABLE_DISLIKES(server="false"):
    cursor, conn = create_connection()

    try:
        SERVER_CHECK(server, inspect.stack()[0][3])
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

        print_green("DISLIKES CREATE COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name="HAD TO ROLLBACK DISLIKES TABLE CREATION")

    close_conn(cursor, conn)
   
    
def CREATE_TABLE_COMMENTS(server="false"):
    cursor, conn = create_connection()

    try:
        SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE COMMENTS(
                    Comment_id SERIAL PRIMARY KEY,
                    Post_id BIGINT,
                    User_id BIGINT,
                    Date_time timestamp,
                    FOREIGN KEY (Post_id) REFERENCES POSTS(Post_id),
                    FOREIGN KEY (User_id) REFERENCES USERS(User_id)
                );
                """)
        conn.commit()

        print_green("COMMENT CREATE COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name="HAD TO ROLLBACK COMMENT TABLE CREATION")

    close_conn(cursor, conn)
    
    
def CREATE_TABLE_VIEWS(server="false"):
    cursor, conn = create_connection()

    try:
        SERVER_CHECK(server, inspect.stack()[0][3])
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

        print_green("VIEWS CREATE COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name="HAD TO ROLLBACK VIEWS TABLE CREATION")

    close_conn(cursor, conn)


def CREATE_TABLE_CONNECTIONS(server="false"):
    cursor, conn = create_connection()
    
    try:
        SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
            f"""
                CREATE TABLE CONNECTIONS
                (
                    Friendship_id SERIAL PRIMARY KEY,
                    User_id1 INT,
                    User_id2 INT,
                    creation_date timestamp,
                    
                    FOREIGN KEY (User_id1) REFERENCES USERS(User_id),
                    FOREIGN KEY (User_id2) REFERENCES USERS(User_id)
                );
            """)
        conn.commit()
        print_green("CONNECTION TABLE CREATE COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name="CONNECTION_CREATE_TABLE")
        
    close_conn(cursor, conn)


def CREATE_TABLE_IP_ADRESSES(server="false"):
    cursor, conn = create_connection()

    try:
        SERVER_CHECK(server, inspect.stack()[0][3])
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

        print_green("IP_ADRESSES CREATE COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name="HAD TO ROLLBACK IP_ADRESSES TABLE CREATION")

    close_conn(cursor, conn)
    
    
def CREATE_TABLE_CHAT_ROOMS(server="false"):
    cursor, conn = create_connection()

    try:
        SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE CHAT_ROOMS(
                    Room_id SERIAL PRIMARY KEY,
                    Creator_id BIGINT,
                    FOREIGN KEY (Creator_id) REFERENCES USERS(User_id)
                );
                """)
        conn.commit()

        print_green("CHAT_ROOMS CREATE COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name="HAD TO ROLLBACK CHAT_ROOMS TABLE CREATION")

    close_conn(cursor, conn)
    
    
def CREATE_TABLE_CHAT_ADMINS(server="false"):
    cursor, conn = create_connection()

    try:
        SERVER_CHECK(server, inspect.stack()[0][3])
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

        print_green("CHAT_ADMINS CREATE COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name="HAD TO ROLLBACK CHAT_ADMINS TABLE CREATION")

    close_conn(cursor, conn)

 
