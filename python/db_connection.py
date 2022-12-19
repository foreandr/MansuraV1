# import pyodbc
import psycopg2

def test_connection():
    global conn
    conn = ""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="mansura",
            user="postgres",
            password="cooldood"
            )
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
