import hashlib


from dbconnection import *
from log import *


def USER_INSERT(Username, Password, Email):
    cursor, conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO USERS
            (Username, Password, Email, Date_time)
            VALUES
            ('{Username}', '{hashlib.sha256(Password.encode('utf-8')).hexdigest()}', '{Email}', NOW());
            """)
        conn.commit()

        print_green(F"{Username} REGISTER COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name="USER_INSERT")
    
    cursor.close()
    conn.close()