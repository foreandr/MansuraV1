from Python.database import *

"""THIS IS BASICALLY TO ALLOW YOU TO RESET THE DATABASE OR MAKE EMEGENCY CHANGES"""

#test hello world
def UPDATE_USER_BALANCE(user):
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
    UPDATE USERS SET balance = 10
    WHERE Username = '{user}'
    """)
    conn.commit()
    conn.close()
    cursor.close()

    
def RESET_DATABASE():
    print("hello world")
    USER_FULL_RESET("small")


def DEMO_ACCOUNTS_REGISTER():
    full_register('dailyinsights', hashlib.sha256("hellodailyinsights123!".encode('utf-8')).hexdigest(), 'dailyinsights@gmail.com', 'dailyinsights@gmail.com', 5)
    full_register('royalkilla', hashlib.sha256("helloroyalkilla123!".encode('utf-8')).hexdigest(), 'royalkilla@gmail.com', 'royalkilla@gmail.com', 5)
    full_register('ghost_lover2021', hashlib.sha256("helloghost_lover2021123!".encode('utf-8')).hexdigest(), 'ghost_lover2021@gmail.com', 'ghost_lover2021@gmail.com', 5)
    full_register('johnlocke', hashlib.sha256("hellojohnlocke123!".encode('utf-8')).hexdigest(), 'johnlocke@gmail.com', 'johnlocke@gmail.com', 5)
    full_register('Twomanriot', hashlib.sha256("helloTwomanriot123!".encode('utf-8')).hexdigest(), 'Twomanriot@gmail.com', 'Twomanriot@gmail.com', 5)
    full_register('xerihm', hashlib.sha256("helloxerihm123!".encode('utf-8')).hexdigest(), 'xerihm@gmail.com', 'xerihm@gmail.com', 5)
    full_register('Ludus', hashlib.sha256("helloLudus123!".encode('utf-8')).hexdigest(), 'Ludus@gmail.com', 'Ludus@gmail.com', 5)


def DEMO_ACCOUNTS_SUBSCRIBE():
    MANSURA_SUBSCRIBE('foreandr')
    MANSURA_SUBSCRIBE('dailyinsights')
    MANSURA_SUBSCRIBE('royalkilla')
    MANSURA_SUBSCRIBE('ghost_lover2021')
    MANSURA_SUBSCRIBE('johnlocke')
    MANSURA_SUBSCRIBE('Twomanriot')
    MANSURA_SUBSCRIBE('xerihm')


def INSERT_TIKTOKS():
    DEMO_FILE_INSERT_TIKTOKS()

  
def DELETE_FILES_BY_ID(file_id):
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
    DELETE FROM FILES
    WHERE File_Id = '{file_id}'
    """)
    
    conn.commit()
    conn.close()
    cursor.close()


def DELETE_FILES_BY_NAME(user):
    conn = connection.test_connection()
    cursor = conn.cursor()
    
    
    cursor.execute(f"""
    DELETE FROM FILES
    WHERE uploader = '{user}'
    """)
    
    conn.commit()
    conn.close()
    cursor.close()


def GET_FILES():
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT * FROM FILES
    """)
    
    for i in cursor.fetchall():
        print(i)

    conn.close()
    cursor.close()


def GET_FILES_BY_ID(file_id):
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT * FROM FILES
    WHERE File_Id = '{file_id}'
    """)
    
    for i in cursor.fetchall():
        print(i)

    conn.close()
    cursor.close()


def GET_FILES_BY_USER(username):
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT * FROM FILES
    WHERE uploader = '{username}'
    """)
    
    for i in cursor.fetchall():
        print(i)

    conn.close()
    cursor.close()


def GET_KEYWORDS():
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT * FROM KEYWORDS
    """)
    
    for i in cursor.fetchall():
        print(i)

    conn.close()
    cursor.close()
    
    
def GET_FILE_KEYWORDS():
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT * FROM FILE_KEYWORDS
    """)
    
    for i in cursor.fetchall():
        print(i)

    conn.close()
    cursor.close()
 
 
def GET_ALL_USERS():
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT * FROM USERS
    """)
    
    for i in cursor.fetchall():
        print(i)

    conn.close()
    cursor.close()


def DELETE_SPECIFIC_KEYWORD(KEYWORD):
    conn = connection.test_connection()
    cursor = conn.cursor()
    
    
    cursor.execute(f"""
    DELETE FROM KEYWORDS
    WHERE uploader = '{KEYWORD}'
    """)
    
    conn.commit()
    conn.close()
    cursor.close()
    
    
def DELETE_SPECIFIC_FILE_KEYWORD(KEYWORD):
    
    conn = connection.test_connection()
    cursor = conn.cursor()
    
    
    cursor.execute(f"""
    DELETE FROM FILE_KEYWORDS
    WHERE key_name = '{KEYWORD}'
    """)
    
    conn.commit()
    conn.close()
    cursor.close()

RESET_DATABASE()