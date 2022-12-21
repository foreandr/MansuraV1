try:    
    import python.MODULES as modules
except:
    import MODULES as modules

import random
import string

def CREATE_AND_SEND_ONE_TIME_PASS_EMAIL(email):
    conn = cursor, conn = modules.create_connection()
    cursor = conn.cursor()

    password = CREATE_ONE_TIME_PASS(length=10)

    if CHECK_FOR_A_ONE_TIME_PASS(email):
        cursor.execute(f"""
            UPDATE ONE_TIME_PASSWORDS
            SET Generated_Pass_Code = '{password}'
            WHERE Email = '{email}'
        """)
        conn.commit()
        print("SUCCESSFULLY UPDATED PRE EXISTING ONE")

    else:
        cursor.execute(f"""
            INSERT INTO ONE_TIME_PASSWORDS(email,Generated_Pass_Code)
            VALUES ('{email}', '{password}')
            ON CONFLICT DO NOTHING
        """)
        conn.commit()
        print("SUCCESSFULLY INSERTED NEW ONE")

    conn.close()
    cursor.close()
    
    modules.send_email(email, password)
    
def CREATE_ONE_TIME_PASS(length=10):

    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
    # print("Random string of length", length, "is:", result_str)
    
def GET_ONE_TIME_PASS(email):
    cursor, conn = modules.create_connection()
    cursor = conn.cursor()
    
    cursor.execute(f"""
        SELECT Generated_Pass_Code
        FROM ONE_TIME_PASSWORDS
        WHERE email = '{email}'
    """)
    one_time = ""
    for i in cursor.fetchall():
        # print(i)
        one_time= i[0]
        
    conn.commit()
    conn.close()
    
    return one_time

def CHECK_FOR_A_ONE_TIME_PASS(email):
    cursor, conn = modules.create_connection()

    cursor.execute(f"""
        SELECT * 
        FROM ONE_TIME_PASSWORDS
        WHERE email = '{email}'
    """)
    my_array = []
    for i in cursor.fetchall():
        # print(i)
        my_array.append(i)
        
    conn.commit()
    conn.close()
    
    if len(my_array) == 0: #empty
        return False
    else:
        return True