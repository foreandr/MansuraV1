import io
from PIL import Image

try:    
    import python.MODULES as modules
except:
    import MODULES as modules


#


def GET_ALL_USERS():
    cursor, conn = modules.create_connection()
    query = """
        SELECT * FROM USERS
    """
    cursor.execute(query)
    
    for i in cursor.fetchall():
        print(i)
        
    modules.close_conn(cursor, conn)
    
def GET_ALL_POSTS():
    cursor, conn = modules.create_connection()
    query = """
        SELECT * FROM POSTS
    """
    cursor.execute(query)
    
    for i in cursor.fetchall():
        print(i)
        
    modules.close_conn(cursor, conn) 

def GET_ALL_PEOPLE():
    cursor, conn = modules.create_connection()
    query = """
        SELECT people.Person_id, 
        people.Person_name,        
        (   
            SELECT COUNT(*) 
            FROM POST_PERSON post_person
            WHERE post_person.Person_id = people.Person_id
        ) 
        
        FROM PEOPLE people
        
    """
    cursor.execute(query)
    results = []
    for i in cursor.fetchall():
        results.append([i[0],i[1],i[2]])
        
    modules.close_conn(cursor, conn) 
    return results
     
    
def GET_PROFILE_IMAGE_BY_USER(username):
    cursor, conn = modules.create_connection()
    query = f"""
        SELECT Profile_pic 
        FROM USERS
        WHERE username = '{username}'
    """
    cursor.execute(query)
    byte_array = ""
    for i in cursor.fetchall():
        byte_array = bytes(i[0])
    
    #print(type(byte_array))
    #print(byte_array)
    # image = Image.open(io.BytesIO(byte_array))
    modules.close_conn(cursor, conn)
    return byte_array
    
    
def GET_POST_ID_BY_LINK_AND_USER_ID(User_id, Post_link):
    cursor, conn = modules.create_connection()
    query = f"""
        SELECT Post_id
        FROM POSTS
        WHERE User_id = '{User_id}'
        AND Post_link = '{Post_link}'
    """
    cursor.execute(query)
    
    for i in cursor.fetchall():
        post_link = i[0]
    
    modules.close_conn(cursor, conn)
    return post_link

def GET_PERSON_ID_BY_NAME(Person):
    cursor, conn = modules.create_connection()
    query = f"""
        SELECT Person_id 
        FROM PEOPLE
        WHERE Person_name = '{Person}'
    """
    cursor.execute(query)
    
    for i in cursor.fetchall():
        category = i[0]
    
    modules.close_conn(cursor, conn)
    return category

def GET_POSTS_BY_PERSON(Person):
    return 1 

def GET_POSTS_BY_TAG(Person):
    return 1 
 
def UNIVERSAL_FUNCTION(cat_id=""):
    cursor, conn = modules.create_connection()
    cat = modules.PERSON_SEARCH(cat_id)
    
    
    query = f"""
    SELECT posts.Post_title, posts.Post_description, posts.Post_html, posts.Date_time, people.Person_name, people.Person_id
    FROM POSTS posts
    
    INNER JOIN POST_PERSON post_person
    ON post_person.Post_id = posts.Post_id
    
    INNER JOIN PEOPLE people
    ON cat.Person_id = post_person.Person_id
    
    WHERE 1 =1 
    {cat}
    """
    cursor.execute(query)
    posts = []
    
    for i in cursor.fetchall():
        posts.append([i[0], i[1], i[2], i[3], i[4], i[5]])
        # print(i)
        
    modules.close_conn(cursor, conn)
    return posts

def GET_FOLLOWERS_BY_USER_ID(User_id):
    cursor, conn = modules.create_connection()
    query = f"""
        SELECT User_id1 
        FROM CONNECTIONS
        WHERE User_id2 = '{User_id}'
    """
    cursor.execute(query)
    followers = []
    for i in cursor.fetchall():
        # print(i)
        followers.append(i[0])
        
    modules.close_conn(cursor, conn)
    return followers


if __name__ == "__main__": 
    
    
    # GET_ALL_USERS()
    # GET_ALL_USERS()
    #GET_PROFILE_IMAGE_BY_USER("Andre")
    GET_ALL_POSTS()
