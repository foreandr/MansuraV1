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
    return 1

def GET_CATEGORY_ID_BY_NAME(Category):
    return 1

def GET_POSTS_BY_CATEGORY(Category):
    return 1 

def GET_POSTS_BY_TAG(Category):
    return 1 

def UNIVERSAL_FUNCTION(cat_id):
    cursor, conn = modules.create_connection()
    
    
    
    query = f"""
    SELECT posts.Post_title, posts.Post_description, posts.Post_html 
    FROM POSTS posts
    
    INNER JOIN POST_CATEGORY post_cat
    ON post_cat.Post_id = posts.Post_id
    
    INNER JOIN CATEGORIES cat
    ON cat.Category_id = post_cat.Category_id
    
    WHERE cat.Category_id = '{cat_id}'
    """
    cursor.execute(query)
    posts = []
    
    for i in cursor.fetchall():
        posts.append(i)
        
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
    GET_PROFILE_IMAGE_BY_USER("Andre")
