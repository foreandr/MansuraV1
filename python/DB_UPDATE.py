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
 
