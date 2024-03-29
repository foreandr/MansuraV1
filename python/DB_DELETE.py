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
    
def DELETE_SUBSCRIBE(Person_id, User_id):
    cursor, conn = modules.create_connection()
    
    try:
        cursor.execute(
            f"""
                DELETE FROM SUBSCRIPTIONS
                WHERE Person_id = '{Person_id}' AND User_id = '{User_id}'
            """)
        conn.commit()
        modules.print_green(f"REMOVED SUB {User_id} from post  {Person_id}")
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

def DELETE_FROM_COMMENT_LIKES(Comment_id, User_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            DELETE FROM COMMENT_VOTES
            WHERE Comment_id = %(Comment_id)s
            AND User_id = %(User_id)s
        """, {'Comment_id': Comment_id,
            'User_id':User_id
            }
        )
        conn.commit() 
        modules.close_conn(cursor, conn) 
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

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
    try:
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
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
    
def DELETE_FROM_POST_PERSON(post_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            DELETE FROM POST_PERSON
            WHERE Post_id = %(post_id)s
        """, {'post_id': post_id
            }
        )
        conn.commit()
        modules.close_conn(cursor, conn)
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n") 
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
    
def DELETE_FROM_POST_PERSON_REQUEST(post_id,User_id,Person_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            DELETE FROM POST_PERSON_REQUEST
            WHERE Post_id = %(post_id)s
            AND Person_id = %(Person_id)s
            AND User_id = %(User_id)s
        """, {'post_id': post_id,
              'User_id': User_id,
              'Person_id': Person_id
            }
        )
        conn.commit()
        modules.close_conn(cursor, conn)
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n") 
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 


def DELETE_FROM_VIEWS(post_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            DELETE FROM VIEWS
            WHERE Post_id = %(post_id)s
        """, {'post_id': post_id
            }
        )
        conn.commit()
        modules.close_conn(cursor, conn)  
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def DELETE_FROM_COMMENTS(post_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            DELETE FROM COMMENTS
            WHERE Post_id = %(post_id)s
        """, {'post_id': post_id
            }
        )
        conn.commit() 
        modules.close_conn(cursor, conn) 
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def DELETE_FROM_LIKES(post_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            DELETE FROM LIKES
            WHERE Post_id = %(post_id)s
        """, {'post_id': post_id
            }
        )
        conn.commit() 
        modules.close_conn(cursor, conn) 
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
    
def DELETE_FROM_COMMENTS(post_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            DELETE FROM COMMENTS
            WHERE Post_id = %(post_id)s
        """, {'post_id': post_id
            }
        )
        conn.commit() 
        modules.close_conn(cursor, conn) 
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}")     

def DELETE_FROM_POSTS(post_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            DELETE FROM POSTS
            WHERE Post_id = %(post_id)s
        """, {'post_id': post_id
            }
        )
        conn.commit() 
        modules.close_conn(cursor, conn) 
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def DELETE_FROM_FAVOURITES(post_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            DELETE FROM FAVOURITES
            WHERE Post_id = %(post_id)s
        """, {'post_id': post_id
            }
        )
        conn.commit() 
        modules.close_conn(cursor, conn) 
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def DELETE_POST(post_id):
    DELETE_FROM_LIKES(post_id)
    DELETE_FROM_VIEWS(post_id)
    DELETE_FROM_COMMENTS(post_id)
    DELETE_FROM_FAVOURITES(post_id)
    DELETE_FROM_POST_PERSON(post_id)
    DELETE_FROM_POSTS(post_id)
    
def DELETE_USER(User_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            DELETE FROM USERS
            WHERE User_id = %(User_id)s
        """, {'User_id': User_id
            }
        )
        conn.commit()
        modules.close_conn(cursor, conn)
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def GET_ALL_POST_IDS_BY_PERSON_ID(Person_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            SELECT posts.Post_id
            FROM POSTS posts
            
            INNER JOIN POST_PERSON post_person
            ON posts.Post_id = post_person.Post_id
            
            WHERE post_person.Person_id = '{Person_id}'
        """)
        results = [] 
        for i in cursor.fetchall():
            results.append(i[0])
        modules.close_conn(cursor, conn)
        return results
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
     
def DELETE_PERSON(Person_id):
    try:
        post_ids = modules.GET_ALL_POST_IDS_BY_PERSON_ID(Person_id)
        for i in post_ids:
            DELETE_POST(i)
            
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            DELETE FROM PEOPLE people
            WHERE people.Person_id = %(Person_id)s
        """, {'Person_id':Person_id
            }
        )
        conn.commit()
        modules.close_conn(cursor, conn) 
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def LEAVE_CHAT_ROOM(User_id, Room_id):
    
    creator_id = modules.GET_CREATOR_OF_ROOM(Room_id)
    if creator_id == User_id:
        modules.REMOVE_CREATOR_FROM_ROOM(Room_id)
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            DELETE FROM CHAT_USERS
            WHERE User_id = '{User_id}'
            AND Room_id = '{Room_id}'
        """
        )
        conn.commit()
        modules.close_conn(cursor, conn) 
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")   
    except Exception as e:
        print("error as e", e)

def DELETE_CHAT_INVITE(User_id, Room_id):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            DELETE FROM CHAT_ROOM_INVITES
            WHERE User_id = %(User_id)s
            AND Room_id = %(Room_id)s
        """, {'User_id': User_id,
            'Room_id': Room_id
            }
        )
        conn.commit()
        modules.close_conn(cursor, conn)  
        modules.print_green(f"{inspect.stack()[0][3]} COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 

def KICK_FROM_CHAT_ROOM(Room_id, User_id):
    creator_id = modules.GET_CREATOR_OF_ROOM(Room_id)
    if creator_id != User_id:
        try:
            cursor, conn = modules.create_connection()
            cursor.execute(f"""
                DELETE FROM CHAT_USERS
                WHERE User_id = '{User_id}'
                AND Room_id = '{Room_id}'
            """
            )
            conn.commit()
            modules.close_conn(cursor, conn) 
            modules.print_green(f"{inspect.stack()[0][3]} {Room_id, User_id} COMPLETED\n")   
        except Exception as e:
            print("error as e", e)
    else:
        return "CAN'T KICK YOURSELF IDIOT"

def EMERGENCY_DELETE_ALL_POSTS():
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            DELETE FROM VIEWS
        """
        )
        conn.commit()
        modules.close_conn(cursor, conn) 
        
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            DELETE FROM POST_PERSON
        """
        )
        conn.commit()
        modules.close_conn(cursor, conn) 
        
        
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            DELETE FROM POSTS
        """
        )
        conn.commit()
        modules.close_conn(cursor, conn) 
            
    except Exception as e:
            print("error as e", e)


if __name__ == "__main__":
    # EMERGENCY_DELETE_ALL_POSTS()
    DELETE_PERSON(329)


    
    pass