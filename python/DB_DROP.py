try:    
    import python.MODULES as modules
except:
    import MODULES as modules
    
def DROP_TABLE_X(table_name):
    
    cursor, conn = modules.create_connection()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    modules.close_conn(cursor, conn)
if __name__ == '__main__':
    DROP_TABLE_X("DISLIKES")
    