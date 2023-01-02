try:    
    import python.MODULES as modules
except:
    import MODULES as modules
    
import inspect

def DELETE_LIKE(Post_id, User_id):
    cursor, conn = modules.create_connection()
    
    try:
        cursor.execute(
            f"""
                DELETE FROM LIKES 
                WHERE Post_id = '{Post_id}' AND User_id = '{User_id}'
            """)
        conn.commit()
        modules.print_green(f"REMOVED LIKED {User_id} from post  {Post_id}")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
    
    modules.close_conn(cursor, conn) 

def DELETE_FAVOURITE(Post_id, User_id):
    cursor, conn = modules.create_connection()
    
    try:
        cursor.execute(
            f"""
                DELETE FROM FAVOURITES
                WHERE Post_id = '{Post_id}' AND User_id = '{User_id}'
            """)
        conn.commit()
        modules.print_green(f"REMOVED FAVOURITE {User_id} from post  {Post_id}")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
    
    modules.close_conn(cursor, conn) 
    
def DELETE_SEARCH_FAVOURITE(Search_algorithm_id, User_id):
    cursor, conn = modules.create_connection()
    try:
        cursor.execute(
            f"""
                DELETE FROM SEARCH_ALGORITM_SAVE
                WHERE Search_algorithm_id = '{Search_algorithm_id}' AND User_id = '{User_id}'
            """)
        conn.commit()
        modules.print_green(f"REMOVED SEARCH FAVOURITE {User_id} from post {Search_algorithm_id}")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
    
    modules.close_conn(cursor, conn) 

def DELETE_CONNECTION(user_id1, user_id2):
    # DELETE FROM films USING producers
    cursor, conn = modules.create_connection()
    try:
        cursor.execute(
            f"""
                DELETE FROM CONNECTIONS 
                WHERE user_id1 = %(user_id1)s 
                AND user_id2 = %(user_id2)s
            """, {'user_id1':user_id1,
                  'user_id2':user_id2
                  }
            )
        conn.commit()
        modules.print_green(f"REMOVED {user_id1} -> {user_id2}")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
    
    modules.close_conn(cursor, conn) 
    

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

def DELETE_TRIBUNAL_WORD_VOTE(word_id, voter_id):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
        DELETE FROM TRIBUNAL_WORD_VOTE
        WHERE User_id = %(word_id)s
        AND Tribunal_word_id = %(voter_id)s
    """, {'voter_id': voter_id,
          'word_id': word_id
        }
    )
    conn.commit()
    modules.close_conn(cursor, conn) 
    
if __name__ == "__main__":
    DELETE_CONNECTION(1, 2)