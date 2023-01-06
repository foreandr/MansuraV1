try:    
    import python.MODULES as modules
except:
    import MODULES as modules
    
def DROP_TABLE_X(table_name):
    try:
        cursor, conn = modules.create_connection()
        cursor.execute(f"""
            DROP TABLE 
            IF EXISTS %(table_name)s
        """, {'table_name': table_name})
        modules.close_conn(cursor, conn)
    except Exception as e:
        cursor.execute("ROLLBACK")
        modules.log_function("error", e, function_name=F"{inspect.stack()[0][3]}") 
    
if __name__ == '__main__':
    DROP_TABLE_X("DISLIKES")
    