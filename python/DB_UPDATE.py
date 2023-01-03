try:    
    import python.MODULES as modules
except:
    import MODULES as modules
    
import hashlib
import inspect 

def CHANGE_PASSWORD(email, password):
    
    cursor, conn = modules.create_connection()
    new_password = hashlib.sha256(f"{password}".encode('utf-8')).hexdigest()
    cursor.execute(f"""
        UPDATE USERS SET Password = %(password)s
        WHERE email = %(email)s
    """, {'password': password,
            'email': email
            }
    )
    conn.commit()
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()
    print(f"CHANGED PASSWORD")
    print(f"OG {password}")
    print(f"HASHED {new_password}")
    
def UPDATE_TRIBUNAL_WORD_VOTE(word_id, voter_id, vote_Type):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
        UPDATE TRIBUNAL_WORD_VOTE
        SET Vote_type = %(word_id)s
        WHERE User_id = %(voter_id)s
        AND Tribunal_word_id = %(vote_Type)s
    """, {'word_id': word_id,
          'voter_id': voter_id,
          'vote_Type': vote_Type
        }
    
    )
    conn.commit()
    modules.print_green(f"{inspect.stack()[0][3]} {word_id, voter_id, vote_Type} COMPLETED\n")
    modules.close_conn(cursor, conn)
 
def UPDATE_POST_HTML_BY_ID(Post_id, embed_link):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
        UPDATE POSTS
        SET Post_html = '{modules.translate_RUBMLE_LINK(embed_link)}'
        WHERE Post_id = '{Post_id}'
    """)
    conn.commit()
    modules.print_green(f"{inspect.stack()[0][3]} {Post_id, embed_link} COMPLETED\n")
    modules.close_conn(cursor, conn)

def UPDATE_PERSON_TO_LIVE(Person_Id):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
        UPDATE PEOPLE
        SET Person_live = 'True'
        WHERE Person_Id = '{Person_Id}'
    """)
    conn.commit()
    modules.print_green(f"{inspect.stack()[0][3]} {Person_Id} COMPLETED\n")
    modules.close_conn(cursor, conn)       

def UPDATE_POST_TO_LIVE(Post_id):
    Person_Id = modules.GET_PERSON_ID_BY_POST_ID(Post_id)
    modules.UPDATE_PERSON_TO_LIVE(Person_Id)

    cursor, conn = modules.create_connection()
    cursor.execute(f"""
        UPDATE POSTS
        SET Post_live = 'True'
        WHERE Post_id = '{Post_id}'
    """)
    conn.commit()
    modules.print_green(f"{inspect.stack()[0][3]} {Post_id} COMPLETED\n")
    modules.close_conn(cursor, conn)    

def UPDATE_CURRENT_SEARCH_BY_USER_ID(Search_algorithm_id, User_id):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
    INSERT INTO CURRENT_USER_SEARCH_ALGORITHM AS algo
    (Search_algorithm_id, User_id) 
    VALUES 
    ('{Search_algorithm_id}', '{User_id}')
    
    ON CONFLICT (User_id) DO 
    
    UPDATE 
    SET Search_algorithm_id = '{Search_algorithm_id}'
    WHERE algo.User_id = '{User_id}'
    
    """)
    conn.commit()
    modules.print_green(f"{inspect.stack()[0][3]} {Search_algorithm_id, User_id} COMPLETED\n")
    modules.close_conn(cursor, conn)
    
def UPDATE_USER_STRIKES(User_id):
    cursor, conn = modules.create_connection()
    cursor.execute(f"""
        UPDATE USER_STATUS
        SET User_Strikes = User_Strikes + 1
        WHERE User_id = '{User_id}'
    """)
    conn.commit()
    modules.print_green(f"{inspect.stack()[0][3]} {User_id} COMPLETED\n")
    modules.close_conn(cursor, conn)    

