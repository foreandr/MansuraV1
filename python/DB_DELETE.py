try:    
    import python.MODULES as modules
except:
    import MODULES as modules
    
import inspect

def DELETE_LIKE(Post_id, User_id):
    pass

def DELETE_FAVOURITE(Post_id, User_id):
    pass

def DELETE_CONNECTION(user_id1, user_id2):
    # DELETE FROM films USING producers
    cursor, conn = modules.create_connection()
    
    try:
        cursor.execute(
            f"""
                DELETE FROM CONNECTIONS 
                WHERE user_id1 = '{user_id1}' AND user_id2 = '{user_id2}'
            """)
        conn.commit()
        modules.print_green(f"REMOVED {user_id1} -> {user_id2}")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
    
    modules.close_conn(cursor, conn) 
    pass

def DELETE_COMMENT(Post_id, User_id):
    # JUST REMOVE THE TEXT
    # MAYBE CREATE A TABLE OF DELETED COMMENTS 
    
    pass

def DELETE_CHAT_ROOM(Creator_id, Room_name):
    # check if creator is deleting
    pass

def DELETE_USER_FROM_CHAT_ROOM(Creator_id, Admin_id, Room_name):

    pass


def DELETE_ADMIN_PRIVILAGE(Creator_id, Admin_id, Room_name):

    pass


def DELETE_ADMIN_PRIVILAGE(Creator_id, Admin_id, Room_name):

    pass