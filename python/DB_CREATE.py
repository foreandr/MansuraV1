from db_connection import *
from helpers import *
from log import *
import inspect

def SERVER_CHECK(server, function):
    # print()
    cursor, conn = create_connection()
    if server == "false":
        if function == "CREATE_TABLE_USER":
            cursor.execute("""DROP TABLE IF EXISTS USERS CASCADE""")
        
        elif function == "CREATE_TABLE_CATEGORIES":
            cursor.execute("""DROP TABLE IF EXISTS CATEGORIES CASCADE""")
        
        elif function == "CREATE_TABLE_POST":
            cursor.execute("""DROP TABLE IF EXISTS POSTS CASCADE""")
        
        elif function == "CREATE_TABLE_TAGS":
            cursor.execute("""DROP TABLE IF EXISTS TAGS CASCADE""")
        
        elif function == "CREATE_TABLE_LIKES":
            cursor.execute("""DROP TABLE IF EXISTS LIKES CASCADE""")
        
        elif function == "CREATE_TABLE_DISLIKES":
            cursor.execute("""DROP TABLE IF EXISTS DISLIKES CASCADE""")
        
        elif function == "CREATE_TABLE_COMMENTS":
            cursor.execute("""DROP TABLE IF EXISTS COMMENTS CASCADE""")
        
        elif function == "CREATE_TABLE_VIEWS":
            cursor.execute("""DROP TABLE IF EXISTS VIEWS CASCADE""")
        
        conn.commit()
        print_green(F"CASCADE DROPPED TABLE {function}")
        
        
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
        cursor.execute(
            f"""
            CREATE TABLE POSTS
            (
            Post_id SERIAL PRIMARY KEY,   
            Path varchar,
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
            FOREIGN KEY (Post_id) REFERENCES POSTS(Post_id)
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
                    Like_Id SERIAL PRIMARY KEY,
                    Post_id BIGINT,
                    Liker_id BIGINT,
                    Date_time timestamp, 
                    FOREIGN KEY (Post_id) REFERENCES POSTS(Post_id),
                    FOREIGN KEY (Liker_id) REFERENCES USERS(User_id),
                    UNIQUE (Post_id,  Liker_id)
                );
                """)
        conn.commit()

        print_green("LIKES CREATE COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name="HAD TO ROLLBACK LIKES TABLE CREATION")

    close_conn(cursor, conn)
    
    
def CREATE_TABLE_DISLIKES(server="false"):
    cursor, conn = create_connection()

    try:
        SERVER_CHECK(server, inspect.stack()[0][3])
        cursor.execute(
                f"""
                CREATE TABLE DISLIKES(
                    Dislike_Id SERIAL PRIMARY KEY,
                    Post_id BIGINT,
                    Disliker_id BIGINT,
                    Date_time timestamp,
                    FOREIGN KEY (Post_id) REFERENCES POSTS(Post_id),
                    FOREIGN KEY (Disliker_id) REFERENCES USERS(User_id),
                    
                    UNIQUE (Post_id,  Disliker_id)
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
                    Comment_Id SERIAL PRIMARY KEY,
                    Post_id BIGINT,
                    Commenter_id BIGINT,
                    Date_time timestamp,
                    FOREIGN KEY (Post_id) REFERENCES POSTS(Post_id),
                    FOREIGN KEY (Commenter_id) REFERENCES USERS(User_id)
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
                    Comment_Id SERIAL PRIMARY KEY,
                    Post_id BIGINT,
                    Viewer_id BIGINT,
                    Date_time timestamp,
                    FOREIGN KEY (Post_id) REFERENCES POSTS(Post_id),
                    FOREIGN KEY (Viewer_id) REFERENCES USERS(User_id)
                );
                """)
        conn.commit()

        print_green("VIEWS CREATE COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name="HAD TO ROLLBACK VIEWS TABLE CREATION")

    close_conn(cursor, conn)
    
CREATE_TABLE_USER()
CREATE_TABLE_CATEGORIES()
CREATE_TABLE_POST()
CREATE_TABLE_TAGS()
CREATE_TABLE_LIKES()
CREATE_TABLE_DISLIKES()
CREATE_TABLE_VIEWS()