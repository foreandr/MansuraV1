# import pyodbc
import psycopg2

def test_connection():
    global conn
    try:
        conn = psycopg2.connect(
            host="dunyacluster-do-user-11502072-0.b.db.ondigitalocean.com",
            database="defaultdb",
            user="doadmin",
            password="AVNS_PyzVOYIsOzm3TrfyGpa",
            port=25060)
        # print("MySQL Database connection successful")
    except psycopg2.Error as err:
        print(f"Error: '{err}'")
    return conn

def close_conn(cursor, conn):
    cursor.close()
    conn.close()
    
def create_connection():
    conn = test_connection()
    cursor = conn.cursor()
    return cursor, conn
