import hashlib
import inspect

from dbconnection import *
from log import *


def INSERT_USER(Username, Password, Email):
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

        print_green(F"{Username} INSERT COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name=f"{inspect.stack()[0][3]}")
    
    cursor.close()
    conn.close()

def INSERT_CATEGORY(Category_name):
    cursor, conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO USERS
            (Category_name)
            VALUES
            ('{Category_name}');
            """)
        conn.commit()

        print_green(F"{Category_name} INSERT COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function("error", e, function_name=F"{inspect.stack()[0][3]}")
    
    cursor.close()
    conn.close()