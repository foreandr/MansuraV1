import io
from PIL import Image

try:
    from python.MODULES import *
except:
    from MODULES import *


def GET_ALL_USERS():
    cursor, conn = create_connection()
    query = """
        SELECT * FROM USERS
    """
    cursor.execute(query)
    
    for i in cursor.fetchall():
        print(i)
        
    close_conn(cursor, conn)
    
    
def GET_PROFILE_IMAGE_BY_USER(username):
    cursor, conn = create_connection()
    query = f"""
        SELECT Profile_pic 
        FROM USERS
        WHERE username = '{username}'
    """
    cursor.execute(query)
    byte_array = ""
    for i in cursor.fetchall():
        byte_array = bytes(i[0])
    
    print(type(byte_array))
    image = Image.open(io.BytesIO(byte_array))
    close_conn(cursor, conn)
    
def GET_POST_ID_BY_LINK_AND_USER_ID(User_id, Post_link):
    return 1
def GET_CATEGORY_ID_BY_NAME(Category):
    return 1

if __name__ == "__main__": 
    # GET_ALL_USERS()
    GET_PROFILE_IMAGE_BY_USER("Andre")
