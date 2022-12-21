import hashlib
import inspect

try:    
    import python.MODULES as modules
except:
    import MODULES as modules


def INSERT_USER(Username, Password, Email):
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO USERS
            (Username, Password, Profile_pic, Email, Date_time)
            VALUES
            ('{Username}', '{hashlib.sha256(Password.encode('utf-8')).hexdigest()}', {modules.psycopg2.Binary(modules.load_default_profile_pic())}, '{Email}', NOW());
            """)
        conn.commit()

        modules.print_green(F"{Username} INSERT COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=f"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn)  

def INSERT_PERSON(Person_name):
    cursor, conn = modules.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO PEOPLE
            (Person_name)
            VALUES
            ('{Person_name}');
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

        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
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
            """)
        conn.commit()
        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    modules.close_conn(cursor, conn) 
     
def INSERT_COMMENTS(Post_id, User_id, Comment_text, Replying_to_id="NULL"):

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
    
def INSERT_VIEWS(Post_id, User_id):

    cursor, conn = modules.create_connection()
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
        modules.print_green(F"{inspect.stack()[0][3]} COMPLETED")
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
    
    