import os
import shutil
from pathlib import Path
from sqlite3 import DatabaseError
# from django.db import transaction, DatabaseError
from PIL import Image
import datetime
import json


from psycopg2 import Error
import Python.procedures as procedures
# from Python.db_connection import connection
from  Python.helpers import print_green, print_title, print_error, turn_pic_to_hex, check_and_save_dir, print_warning
import Python.db_connection as connection
import Python.big_reset_file as big_reset_file


def validate_user_from_session(email, password):
    conn = connection.test_connection()
    print(f"VALIDATE {email} | {password}")  # GET THIS FROM JAVASCRIPT
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT * 
    FROM USERS
    WHERE email = '{email}'
    AND password = '{password}'
    """)
    tables = cursor.fetchall()
    user = ""
    user_id = ""
    for i in tables:
        # print(i)
        user_id = i[0]
        user = i[1]

    if len(tables) > 0:
        print("SIGNING IN")
        return [True, user_id, user, email, password]
    else:
        print("NOT SIGNING IN")
        return [False]


def GET_USER_ID(username):
    
    conn = connection.test_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"""
            SELECT GET_USER_ID('{username}'); 
            """)
        tables = cursor.fetchall()
        user_id = 0
        for i in tables:
            # print(i)

            user_id = i[0] # THE TUPLE (1, foreandr) as string
            user_id = user_id[1:-1].split(",")[0] # remove both ends, split by comma, grab 1
        cursor.close()
        conn.close()
        
        # print_green('GOT_USER_ID')
        
        return user_id
    except Exception as e:
        print(f"FAILED TO INSERT {username}")
        print(e)


def EXISTS_EMAIL(email="foreandr@gmail.com"):
    conn = connection.test_connection()
    table_name = "USERS"
    cursor = conn.cursor()
    cursor.execute(
        f"""
            SELECT *
            FROM {table_name}
            WHERE email = '{email}'
        """)

    tables = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(tables) > 0:
        return True
    else:
        return False


def CHECK_IF_NAME_EXISTS(username):
    conn = connection.test_connection()
    table_name = "USERS"
    cursor = conn.cursor()
    cursor.execute(
        f"""
            SELECT *
            FROM {table_name}
            WHERE username = '{username}'
        """)

    tables = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(tables) > 0:
        return True
    else:
        return False


def USER_CREATE_TABLE():
    conn = connection.test_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
                f"""
                CREATE TABLE USERS 
                (
                    User_Id SERIAL PRIMARY KEY,
                    username varchar(20) UNIQUE,
                    password varchar(200),
                    email varchar(200) UNIQUE,
                    paypal_email varchar UNIQUE,
                    creation_date timestamp,
                    balance decimal
                );
                """)
        conn.commit()

        print_green("USER CREATE COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        print_error("\nHAD TO ROLLBACK USER CREATION" + str(e) )
    
    cursor.close()
    conn.close()


def USER_INSERT(username, password, email, paypal_email, balance=0):
    conn = connection.test_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO USERS
            (username, password, email, paypal_email, creation_date, balance)
            VALUES
            ('{username}', '{password}', '{email}', '{paypal_email}', NOW(),{balance});
            """)
        conn.commit()

        print_green(F"{username} REGISTER COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        print(e)
    
    cursor.close()
    conn.close()


def USER_INSERT_MULTIPLE():
    conn = connection.test_connection()

    # Change the current working directory
    try:
        os.chdir("/mansura")
        shutil.rmtree('static/#UserData/')
    except Exception as e:
        print("could not remove static/#UserData/", e)

    full_register('admin', 'password', 'admin@gmail.com', 'admin@gmail.com', 5)
    full_register('foreandr', 'password', 'foreandr@gmail.com', 'foreandr@gmail.com', 5)
    full_register('andrfore', 'password', 'andrfore@gmail.com', 'andrfore@gmail.com', 5)
    full_register('cheatsie', 'password', 'cheatsieog@gmail.com', 'cheatsieog@gmail.com', 5)
    full_register('dnutty', 'password', 'dnutty@gmail.com', 'dnutty@gmail.com', 5)
    
    # ====

    big_reset_file.GIANT_USER_REGISTER()
 
    # --

    print_green("USER MULTI INSERT COMPLETED\n")


def USER_INSERT_MULTPLE_FILES():
    big_reset_file.GIANT_FILE_INSERT()
    print_green("USER INSERT MULTPLE FILES COMPLETED\n")


def CONNECTION_CREATE_TABLE():
    conn = connection.test_connection()

    cursor = conn.cursor()
    cursor.execute(
        f"""
            CREATE TABLE CONNECTIONS
            (
                Friendship_Id SERIAL PRIMARY KEY,
                User_Id1 INT,
                User_Id2 INT,
                
                FOREIGN KEY (User_Id1) REFERENCES USERS(User_Id),
                FOREIGN KEY (User_Id2) REFERENCES USERS(User_Id)
            );
        """)
    conn.commit()
    cursor.close()
    conn.close()
    print_green("CONNECTION TABLE CREATE COMPLETED\n")


def CONNECTION_INSERT(user_id1, user_id2):
    conn = connection.test_connection()

    # print("INSERTING CONNECTION SERVER SIDE", user_id1, "->", user_id2)
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"""
            INSERT INTO CONNECTIONS (User_Id1, User_Id2)
                VALUES({user_id1}, {user_id2})
            """)
        conn.commit()
    except Exception as e:
         cursor.execute("ROLLBACK")
         print("ERROR:  [INSERT INTO CONNECTIONS] " + str(e))
    
    cursor.close()
    conn.close()
    # print_green('CONNECTION INSERT COMPLETED')


def CONNECTION_REMOVE(user_id_first, user_id_second):
    conn = connection.test_connection()
    
    cursor = connection.cursor()
    cursor.execute(
        f"""
        CALL CUSTOM_DELETION({user_id_first}, {user_id_second});
        """)
    conn.commit()
    
    cursor.close()
    conn.close()
    print_green('CONNECTION DELETION COMPLETED')


def CONNECTION_INSERT_MULTIPLE():
    CONNECTION_INSERT( user_id1=1, user_id2=2)
    CONNECTION_INSERT( user_id1=1, user_id2=3)
    print_green("USER MULTI INSERT CONNECTIONS COMPLETED\n")


def FILE_VOTE_CREATE_TABLE():
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"""
            CREATE TABLE FILE_VOTES(
            File_Vote_Id SERIAL PRIMARY KEY,
            File_id INT,
            Vote_Type varchar,
            Voter_Username varchar(50),
            Date_Time timestamp, 
            FOREIGN KEY (File_id) REFERENCES FILES(File_id)
        )
        """)
    conn.commit()
    print_green("VOTE CREATE TABLE COMPLETED")

    cursor.execute("""
    ALTER TABLE FILE_VOTES
    ADD CHECK( 
        Vote_Type = 'Daily'
        OR Vote_Type = 'Monthly' 
        OR Vote_Type = 'Yearly'
    )
    """)
    conn.commit()


    cursor.close()
    conn.close()
    print_green("VOTE CREATE TABLE CONSTRAINT COMPLETED")


def GET_NUM_FILE_VOTES_LEFT(username, my_vote_type):
    conn = connection.test_connection()
    cursor = conn.cursor()
    subscribed = CHECK_DATE(username)
    if subscribed:
        date_criteria = ""
    
        if my_vote_type == "Daily":
            date_criteria = "day"
        elif my_vote_type == "Monthly":
            date_criteria = "month"
        elif my_vote_type == "Yearly":
            date_criteria = "year"
    
        
        cursor.execute(f""" SELECT COUNT(*)
            FROM FILE_VOTES csv 
            WHERE Vote_Type = '{ my_vote_type }'
            AND Voter_Username = '{username}'
            AND Date_Time >= date_trunc('{date_criteria}', now())::date
        """)
        conn.commit()
        results = cursor.fetchall()
        num = 0
        for value in results:
            #print(value)
            num = (value[0])

        # CLOSE CURSOR AND CONNECTION [MANDATORY]        
        cursor.close()
        conn.close()
                
        if num == 1:
            #print(f"{username} HAS 0 VOTES LEFT FOR {my_vote_type}")
            return 0
        elif num == 0: 
            #print(f"{username} HAS 1 VOTE LEFT FOR {my_vote_type}")
            return 1
    else:
        # CLOSE CURSOR AND CONNECTION [MANDATORY]        
        cursor.close()
        conn.close()
        return 0


def GET_NUM_FILE_VOTES_FOR_TYPE_TOTAL(file_id, my_vote_type):
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f""" SELECT COUNT(*) 
        FROM FILE_VOTES file 
        WHERE file.File_id = {file_id} 
        AND Vote_Type = '{ my_vote_type }'

    """)
    conn.commit()
    results = cursor.fetchall()
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()
    
    num = 0
    for value in results:
        num = (value[0])
    return num


def GET_NUM_FILE_VOTES_FOR_TYPE(username, file_id, my_vote_type):
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f""" SELECT COUNT(*) 
        FROM FILE_VOTES file 
        WHERE file.File_id = {file_id} 
        AND Vote_Type = '{ my_vote_type }'
        AND Voter_Username = '{username}'
        AND Date_Time >= date_trunc('month', now())::date
    """)
    conn.commit()
    results = cursor.fetchall()

    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()

    num = 0
    for value in results:
        num = (value[0])
    return num


def FILE_VOTE_INSERT(username, File_Id, vote_type):
    conn = connection.test_connection()
    cursor = conn.cursor()
    # CHECK IF SUBSCRIBED THIS MONTH
    is_already_subbed_this_month = CHECK_DATE(username)
    if (is_already_subbed_this_month):
        # CHECK IF THEY HAVE A VOTE OF TYPE X FOR THIS TIME PERIOD
        num_votes = GET_NUM_FILE_VOTES_LEFT(username, vote_type)
        if num_votes == 0:
            print_error("[{username}] HAS ALREADY VOTED FOR TIMEFRAME [{vote_type}]. [{num_votes} VOTES]") 
        else:
            # RUN THE INSERT
            try:
                cursor.execute(
                f"""
                    CALL ENTER_FILE_VOTE({File_Id}, '{vote_type}', '{username}');
                """)
                conn.commit()
                print_green(f"INSERTED {username} INTO FILE_VOTES [{vote_type}]")
            except Exception as e:
                cursor.execute("ROLLBACK")
                print_error(f"\nHAD TO ROLLBACK ENTER_FILE_VOTE for: {username}: {e}")
            
    else:
        print_error(f"{username} IS NOT SUBSCRIBED, SUBSCRIBE TO VOTE")
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()

    
def FILE_VOTE_INSERT_DEMO():
    #FILE_VOTE_INSERT( 'foreandr', 1,  'Daily')
    FILE_VOTE_INSERT( 'foreandr', 1,  'Monthly')
    FILE_VOTE_INSERT( 'foreandr', 1,  'Monthly')
    FILE_VOTE_INSERT( 'foreandr', 2,  'Yearly')

    big_reset_file.GIANT_FILE_VOTE_INSERT()

    print_green("VOTE_INSERT_DEMO COMPLETED\n")


def CHECK_DATE(my_username):
    conn = connection.test_connection()

    # print("\nFUNC: CHECK DATE")
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT Username, Subscribed, Date_Time
        FROM SUBSCRIPTIONS_MENSURA
        WHERE Username = '{my_username}'
    """)
    results = cursor.fetchall()
    list_of_months = []
    dates = []
    for value in results:
        # print(value[2])
        list_of_months.append(value[2])
        dates.append(value)
    # CHECK THERE IS AN EXISTENCE FOR A SUB OF THIS YEAR/MONTH
    current_date = GET_CURRENT_DATE()
    #print("CURRENT DATE: ", type,(current_date), current_date)
    already_subbed = False
    for i in range(len(list_of_months)):        
        if list_of_months[i].year == current_date.year and list_of_months[i].month == current_date.month: # CHANGED FROM MONTH TO MINUTE FOR TESTING PURPOSES
            # print(i, current_date)
            already_subbed = True
        else:
            already_subbed = False
            # print(f"{my_username} IS NOT SUBSCRIBED FOR THIS MONTH")
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()
    
    return already_subbed


def USER_SUBSCRIBE_INSERT(username):
    conn = connection.test_connection()
    cursor = conn.cursor()
    try:
        is_already_subbed_this_month = CHECK_DATE(username)            
        
        if  is_already_subbed_this_month:
            print_error(f"{username} are already subscribed this month, cant sorry")
            
            # CLOSE CURSOR AND CONNECTION [MANDATORY]        
            cursor.close()
            conn.close()
            
            return False
        else:     
            cursor.execute(f"""
            INSERT INTO SUBSCRIPTIONS_MENSURA(Username, Subscribed, Date_Time)
            VALUES('{username}' , TRUE, NOW())
            """)
            conn.commit()
            
            # CLOSE CURSOR AND CONNECTION [MANDATORY]        
            cursor.close()
            conn.close()

            return True

    except Exception as e:
            cursor.execute("ROLLBACK")
            print_error(str(e))
            
            # CLOSE CURSOR AND CONNECTION [MANDATORY]        
            cursor.close()
            conn.close()

            return False


def MANSURA_SUBSCRIBE(username):
    conn = connection.test_connection()
    # print("FUNC: MANSURA_SUBSCRIBE")
    try:
        user_balance = GET_USER_BALANCE_SIMPLE(username) # GET BALANCE
        # print(username, user_balance, type(user_balance))
        
        if isinstance(user_balance, float) or isinstance(user_balance, int):
        
            if user_balance >= 5.00:                        # CHECK BALANCE      
                USER_SUBSCRIBE_FULL(username)
                return True
            else:
                print(f"{username} did not have enough to subscribe")
                
                # CLOSE CURSOR AND CONNECTION [MANDATORY]        
                conn.close()

                return False
        else:
            print(f"USER BALANCE CHECK FAILED:\nUSERNAME:{username}\tBALANCE:{user_balance}\tTYPE:{type(user_balance)}")
            
            # CLOSE CURSOR AND CONNECTION [MANDATORY]        
            conn.close()
            
            return False
    except Exception as e:
        print("SUBSCRIBE FAILED: ",e)
    
        
        
def GET_USER_BALANCE(username):
    conn = connection.test_connection()
    # print("FUNC: GET_USER_BALANCE")
    cursor = conn.cursor()
    try:
        cursor.execute(f"""SELECT GET_USER_BALANCE('{username}')""")
        results = cursor.fetchall()
        for result in  results:
            # print(result)
            result = result[0][1:-1]
            result = result.split(",")

            # CLOSE CURSOR AND CONNECTION [MANDATORY]        
            cursor.close()
            conn.close()

            return float(result[2])
    except Exception as e:
        print(e)
        # CLOSE CURSOR AND CONNECTION [MANDATORY]        
        cursor.close()
        conn.close()


def FUNCTION_AND_PROCEDURES():
    
    # CREATE OR REPLACE [PROCEDURES & FUNCTIONS] 
    procedures.FUNCTION_GET_USER_ID()  
    # procedures.FUNCTION_GET_ALL_DATASETS()
    # procedures.FUNCTION_WHICH_PAGES()  
    procedures.FUNCTION_GET_FOLLOWING() 
    procedures.FUNCTION_GET_FOLLOWERS() 
    procedures.FUNCTION_GET_MODELS_BY_FILE_ID() 
    # procedures.FUNCTION_GET_USER_BALANCE()  
    procedures.FUNCTION_MODEL_GET_NUM_VOTES_BY_MODEL_ID()
    procedures.FUNCTION_GET_FILES()
    procedures.FUNCTION_GET_FILE_VOTE_COUNT() 
    procedures.FUNCTION_GET_FILE_VOTE_COUNT_TYPED()
    
    procedures.FUNCTION_GET_CALCULATED_UPLOAD_VOLUME_BY_MONTH()

    # ---
    procedures.PROCEDURE_USER_MONTHLY_SUBSCRIPTION_FEE() 
    #procedures.PROCEDURE_ENTER_MODEL_VOTE(conn) 
    procedures.PROCEDURE_ENTER_FILE_VOTE() 
    # procedures.PROCEDURE_CUSTOM_MODEL_INSERT(conn) 
    procedures.PROCEDURE_CHANGE_PASSWORD()
    procedures.PROCEDURE_CUSTOM_DELETION()


def SET_TIME_ZONE():
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute("""ALTER DATABASE defaultdb SET timezone TO 'EST';""")
    conn.commit()
    print_green("SET TIME ZONE")
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()


def MANSURA_SUBSCRIBE_INSERT_MULTIPLE_DEMO():
    conn = connection.test_connection()

    #TODO:THINK ABOUT DATA VALIDATNG THE USERNAME, PRBABLY WONT NEED
    # MANSURA_SUBSCRIBE( 'foreandr')
    MANSURA_SUBSCRIBE( 'andrfore')
    # MANSURA_SUBSCRIBE( 'bigfrog')
    MANSURA_SUBSCRIBE( 'cheatsie')
    
    big_reset_file.GIANT_SUBSCRIBE()



    print_green("SUBSCRIBED USERS\n")


def REMOVE_ALL_USER_DIRECTORIES():
    dirpath = 'static/#UserData/'
    # print(os.getcwd())
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            # os.remove(filepath)
            print(OSError)


def USER_FULL_RESET():
    print_title("\nEXECUTING FULL RESET\n")
    
    # SET TIMEZONE
    # SET_TIME_ZONE(conn)
    FUNCTION_AND_PROCEDURES()

    # DROPPING ALL TABLES
    DROP_ALL_TABLES()
    REMOVE_ALL_USER_DIRECTORIES()

    # CREATE TABLES
    USER_CREATE_TABLE()
    CREATE_PAYOUTS_TABLE()
    FILE_CREATE_TABLE()   
    FILE_VOTE_CREATE_TABLE() 
    CONNECTION_CREATE_TABLE()
    CREATE_MANSURA_TABLE()
    SEARCH_ALGO_CREATE_TABLE()

    USER_INSERT_MULTIPLE()
    CONNECTION_INSERT_MULTIPLE()
    MANSURA_SUBSCRIBE_INSERT_MULTIPLE_DEMO()
    USER_INSERT_MULTPLE_FILES()
    FILE_VOTE_INSERT_DEMO() # VOTES ON CSVS
    SEARCH_ALGO_INSERT_DEMO_MULTIPLE()
    # EQUITY CAN GO LAST, DOESN'T INTERFERE WITH ANYTHING
    EQUITY_CREATE_TABLE()
    TRANSFER_EQUITY("admin", "foreandr", 2)

    # MODEL_MULTIPLE_INSERT(conn) # MODELS
    # MODEL_VOTE_INSERT_DEMO(conn) # VOTES ON MODELS \
    #TODO:EQUITY INSIRT
    


    print_title("USER FULL RESET COMPLETED")


def DROP_ALL_TABLES():
    conn = connection.test_connection()
    print_title("\nDROPPING TABELS..")
    cursor = conn.cursor()
    try:
        
        try:
            cursor.execute(f"DROP TABLE IF EXISTS SEARCH_ALGORITHMS;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS SEARCH_ALGORITHMS;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print_error("[SEARCH_ALGORITHMS] " + str(e))

        try:
            cursor.execute(f"DROP TABLE IF EXISTS EQUITY;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS EQUITY;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print_error("[EQUITY] " + str(e))

        try:
            cursor.execute(f"DROP TABLE IF EXISTS SUBSCRIPTIONS_MENSURA;")
            cursor.execute(f"DROP TABLE IF EXISTS SUBSCRIPTIONS_MENSURA;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS SUBSCRIPTIONS_MENSURA;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print_error("[SUBSCRIPTIONS_MENSURA] " + str(e))
               
        try:
            cursor.execute(f"DROP TABLE IF EXISTS MODEL_VOTES;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS MODEL_VOTES;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print_error("[MODEL VOTES] " + str(e))
            
        try:
            cursor.execute(f"DROP TABLE IF EXISTS MODEL;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS MODEL;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print_error("[MODEL] " + str(e))
                 
        try:
            cursor.execute(f"DROP TABLE IF EXISTS FILE_VOTES;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS FILE_VOTES;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print_error("[FILE_VOTES] " + str(e) )

        try:
            cursor.execute(f"DROP TABLE IF EXISTS FILES;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS FILES;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print_error("[FILES] " + str(e))

        try:
            cursor.execute(f"DROP TABLE IF EXISTS CONNECTIONS;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS CONNECTIONS;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print_error("[CONNECTIONS]" + str(e))

        try:        
            cursor.execute(f"DROP TABLE IF EXISTS USERS;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS USERS;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print_error("[USERS]: " + str(e)) 
    except:
        print_error("FAILED TO DROP ALL TABLES\n")
    print_title("DROPPED ALL TABLES\n")
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()


def FILE_CREATE_TABLE():
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS FILES""")
    cursor.execute(
        f"""
        CREATE TABLE FILES
        (
        File_id SERIAL PRIMARY KEY,   
        File_PATH varchar UNIQUE,
        Uploader varchar,
        UserId BIGINT,
        Post_foreign_id_source varchar,
        Post_total_size INT,
        Date_Time timestamp,      
        FOREIGN KEY (UserId) REFERENCES USERS(User_Id)
        );
        """)
    conn.commit()
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()
    
    print("FILES CREATE COMPLETED\n")

#TODO: i really need to simplify this lmao
def FILE_INSERT(uploader, uploaderId, size, post_foreign_id_source="None", 
                file_path="N-A", post_file="", 
                post_text="", age_18="", 
                external_link=""):
    """
    REALLY COMPLICATED NIGHTMARE BUT IT WORKS
    
    """
    
    #1. CHECK THAT THE POST FOREIGN ID ACTUALLY EXISTS
    if post_foreign_id_source == "None" or post_foreign_id_source == "":
        pass
    else:
        if not (CHECK_FILE_EXISTS(post_foreign_id_source)):
            
            print("FAILED TO INSERT FILE BECAUSE FOREIGN FILE DOESNT EXIST")
            #print(F"UPLOADER: {uploader}")
            #print(F"post_foreign_id_source: {post_foreign_id_source}")
            #print(F"uploaderId: {uploaderId}")
            #print(F"UPLOADER: {uploader}")
            return False
        else:
            pass
            # print(F"{post_foreign_id_source}: IS A FILE THAT EXISTS")


    conn = connection.test_connection()
    cursor = conn.cursor()

    #CHECK EMPTY   
    if post_file == "":
        filename = ""
    else: 
        filename = post_file.filename

    # BEGINNING EXOCUTION
    
    ''' #TODO: CAN PROBABLY DELETE THIS WHOLE FILE SIZE CHECK THING THIS SECTION IS CHECKING FILE SIZED
    file_path = file_path + uploader + "temp"
    cursor = conn.cursor()
    cursor.execute(F"""SELECT GET_CALCULATED_UPLOAD_VOLUME_BY_MONTH({uploaderId})""") # checking upload limit
    count = cursor.fetchall()
    num = ""
    for i in count: #1. CHECK VOLUME
        num = i[0]
    # print(f"SUM OF UPLOADED FILES FOR ID {uploaderId} IS {num}")
    
    if not(isinstance(num, int)): # check if there is an int 
        num = 0
    if num > 10737418240:
        fail_size_string = "COULD NOT RUN [FILE_INSERTFILE_INSERT], too much file volume this month, cap 10 gigs"
        print(fail_size_string)
        
        # CLOSE CURSOR AND CONNECTION [MANDATORY]        
        cursor.close()
        conn.close()

        return fail_size_string
        '''
    try:
    # 1. INSERTING INTO DATABASE
        cursor.execute(
            f"""
            INSERT INTO FILES
            (File_PATH,  Uploader, UserId, Post_foreign_id_source, Post_total_size, Date_Time)
            VALUES
            ('{file_path}', '{uploader}','{uploaderId}', '{post_foreign_id_source}', {size}, CURRENT_TIMESTAMP );
            """)
        conn.commit()
            
            
            # 2. UPDATING PATH IN DB TO RELEVANT FILE_ID            
        cursor.execute(f"""
            SELECT File_id
            FROM FILES
            WHERE uploader = '{uploader}'
            ORDER BY Date_Time DESC
            LIMIT 1
        """)
        results = cursor.fetchall()
        CURRENT_FILE_ID = ""
        for i in results: 
            CURRENT_FILE_ID = i[0]
            # print("FILE ID", i)
            
        # CHANGE FILEPATH IN DB TO CORRECT ONE
        new_path = str(uploader) + "-" + str(CURRENT_FILE_ID) 
        cursor.execute(f"""
            UPDATE FILES
            SET File_PATH = '{new_path}'
            WHERE File_Id = {CURRENT_FILE_ID}

        """)
        conn.commit()
            
        # 3. MAKE NEW DIRECTORY FOR USER POST BY FILE_ID
        new_dir = f'static/#UserData/{uploader}/files/{new_path}'
        #path = os.path.join(os.getcwd(), new_dir)
        path = new_dir
        os.mkdir(path)  
            
        # 4. save the picture if there is one
        if filename != "":
            try:
                target = rf'static/#UserData/{uploader}/files/{new_path}/pic.jpg'#TODO: DIFFERENTIATE DIFFERENT EXTENSIONS
                post_file.save(target)
                # print("ENTERED INTO TARGET", target)
            except Exception as e:
                print(str(e) + "FILE ERROR ENTRY OF SOME KIND!!!!!")    
           
        # 5. INSERT INTO FILE SYSTEM           
        FILE_INSERT_STORAGE(
            username = uploader, 
            path_name=new_path, 
            text=post_text, 
            age_18=age_18,
            external_source=external_link                                   
        )

        print_green(f"FILE INSERT COMPLETED {uploader}, {new_path}")
            
        # CLOSE CURSOR AND CONNECTION [MANDATORY]        
        cursor.close()
        conn.close()

         # return new_path #TODO: not sure if this needs to return anything
    except Exception as e:
            print(e)
            cursor.execute("ROLLBACK")
            print_error(F"USER:{uploader} FILE INSEERT FAILED")
            
            # CLOSE CURSOR AND CONNECTION [MANDATORY]        
            cursor.close()
            conn.close()            


def register_user_files(username):
    #todo:MIGHT NEED TO BE LOGIC FOR NEW USERS, NOT SURE IF IT WIILL BREAK
    # Change the current working directory
    # os.chdir('/mansura')

    check_and_save_dir(f"static/#UserData/{username}/profile")
    check_and_save_dir(f"static/#UserData/{username}/files")
    # check_and_save_dir(f"static/#UserData/{username}/config.json")
    check_and_save_dir(f"static/#UserData/{username}/search_algorithms")

    config_json = {
        'age':"",
        'bio':f"Hello my name is {username}"
    }
    jsonString = json.dumps(config_json)
    jsonFile = open(f"static/#UserData/{username}/config.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

    my_path = f"static/#UserData/{username}/profile"
    my_path_with_file = f"static/#UserData/{username}/profile/profile_pic.jpg"  # PREVIOUSLY USED file.filename, should use with other types

    jpgfile = Image.open("#DemoData/DEFAULT_PROFILE.png")
    check_and_save_dir(my_path)
    jpgfile.save(my_path_with_file)


def full_register(username, password, email, paypal_email, balance):
    # print_green(F"INSERT VALUES: \nUSERNAME: {username}\nPASSWORD: {password}\nEMAIL: {email}")
    # DELETING A PARTCIULAR USER
    # try:
    #    DELETE_USER_FILES(username)
    # except:
    #    print_error("User doesn't exist")
    USER_INSERT(username, password, email, paypal_email, balance)
    register_user_files(username)
    # FILE_INSERT(connection
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        


def DELETE_USER_FILES(user):
    file_location = f"../static/#UserData/{user}/profile"
    file_location2 = f"../static/#UserData/{user}/files"
    file_location3 = f"../static/#UserData/{user}/photos"

    user_folders = [file_location, file_location2, file_location3]
    ## Try to remove tree; if failed show an error using try...except on screen
    for i in user_folders:
        try:
            shutil.rmtree(i)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))


def CHANGE_PASSWORD(email, password):
    conn = connection.test_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"""
                CALL CHANGE_PASSWORD_FOR_EMAIL('{email}', '{password}');
            """)
        conn.commit()
        cursor.close()
        print_green('CHANGE_PASSWORD COMPLETED')
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("ERROR:  [CHANGE_PASSWORD] " + str(e))
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()


def MODEL_GET_NUM_VOTES_BY_MODEL_ID(model_id):
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT MODEL_GET_NUM_VOTES_BY_MODEL_ID({model_id});")
    count = cursor.fetchall()
    num = ""
    for i in count:
        num = i[0]
    print(F'NUM VOTES FOR MODEL: {model_id} = {num}')
        
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()
    
    return num


def GET_FOLLOWING(username):
    conn = connection.test_connection()

    # print('GET FOLLOWING: ', username)
    cursor = conn.cursor()
    cursor.execute(f"SELECT GET_FOLLOWING('{username}');")
    user_friends = []
    friends = cursor.fetchall()
    for friend in friends:
        values = friend[0].split(",")
        user_friends.append(values[3][:-1])  
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()
    
    return user_friends, len(user_friends)


def GET_FOLLOWERS(username):
    conn = connection.test_connection()
    
    print('GET FOLLOWERS: ', username)
    cursor = conn.cursor()
    cursor.execute(f"SELECT GET_FOLLOWERS('{username}');")
    user_friends = []
    friends = cursor.fetchall()
    for friend in friends:
        values = friend[0].split(",")
        user_friends.append(values[3][:-1])  

    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()

    return user_friends, len(user_friends)


def GET_ALL_DATASETS(page_no, vote_type, how_many):
    conn = connection.test_connection()
    
    print(f"GETTING DATASETs: DETAILS:\n")
    cursor = conn.cursor()
    cursor.execute(f"SELECT GET_ALL_DATASETS({page_no} , '{vote_type}', {how_many});")
    user_info = []
    files = cursor.fetchall()
    for details in files:
        # print(details)
        details = details[0][1:-1]        
        
        details = details.split(",")
        name = details[0]
        path = details[1]
        description = details[2]
        date = details[3]
        size = details[4]
        file_id = details[5]
        user_info.append([name, path, description, date, size, file_id])

    # for i in user_info:
    #    print(i)
    file_ids = ""
    names = ""
    files = ""
    descriptions = ""
    dates = ""
    sizes = ""
    num_votes_Daily = ""
    num_votes_Monthly = ""
    num_votes_Yearly = ""
    num_total_votes = ""
    for i in user_info:
        # print(i)
        file_ids += i[5] + "//"
        
        names += i[0] + "//"

        filename = i[1].split('//')[-1]
        files += filename + "//"

        descriptions += i[2] + "//"

        dates += str(i[3]) + "//"

        sizes += str(i[4]) + "//"
        
        Daily = str(GET_NUM_FILE_VOTES_FOR_TYPE_TOTAL(i[5],  'Daily'))
        Monthly = str(GET_NUM_FILE_VOTES_FOR_TYPE_TOTAL(i[5],  'Monthly'))
        Yearly = str(GET_NUM_FILE_VOTES_FOR_TYPE_TOTAL(i[5],  'Yearly'))

        total_votes = int(Daily) + int(Monthly) + int(Yearly)
        # print(total_votes)

        num_votes_Daily += str(Daily) + "//";
        num_votes_Monthly += str(Monthly) + "//";
        num_votes_Yearly += str(Yearly) + "//";
        num_total_votes += str(total_votes) + "//";


   
    #print(f"NAMES:             {names}")
    #print(f"files: {files}")
    # print(f"dates: {dates}")
    #print(f"sizes:             {sizes}")
    #print(f"num_votes_Daily:   {num_votes_Daily}")
    #print(f"num_votes_Monthly: {num_votes_Monthly}")
    #print(f"num_votes_Yearly:  {num_votes_Yearly}")
    #print(f"num_votes_TOTAL:   {num_total_votes}")

    daily_pool = GET_DAILY_PAYOUTS()
    monthly_pool = GET_MONTHLY_PAYOUTS()
    yearly_pool = GET_YEARLY_PAYOUTS()

    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()

    return file_ids, names, files, descriptions, dates, sizes, num_votes_Daily, num_votes_Monthly, num_votes_Yearly, num_total_votes, daily_pool, monthly_pool, yearly_pool


def GET_MODELS_BY_FILE_ID(file_id):
    conn = connection.test_connection()

    cursor = conn.cursor()
    cursor.execute(f"SELECT GET_MODELS_BY_FILE_ID({file_id});")
    file_results = cursor.fetchall()

    model_ids = ""
    local_paths = ""
    model_descriptions = ""
    dates = ""
    foreign_file_id = ""
    model_uploaders = ""
    model_user_ids = ""
    csv_file_paths = ""
    file_sizes = ""
    csv_user_id = ""
    csv_upload_date = ""
    num_model_votes = ""
    for i in file_results:
        print(i)
        i = i[0][1:-1].split(",")
        model_ids += str(i[0]) + "//" #
        local_paths += str(i[1]) + "//"
        model_descriptions += str(i[2]) + "//"
        dates += str(i[3]) + "//"
        foreign_file_id += str(i[4]) + "//"
        model_uploaders += str(i[5]) + "//"
        model_user_ids += str(i[6]) + "//"
        csv_file_paths += str(i[7]) + "//"
        file_sizes = str(i[8]) + " BYTES"
        csv_user_id += str(i[9]) + "//"
        csv_upload_date = str(i[10])
        num_model_votes += str(MODEL_GET_NUM_VOTES_BY_MODEL_ID(i[0])) + "//" 

    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()

    return model_ids, local_paths, model_descriptions, dates, foreign_file_id, model_uploaders, model_user_ids, csv_file_paths, file_sizes, csv_user_id, csv_upload_date, num_model_votes


def GET_FILE_ID_W_USERNAME(username, file_name):
    conn = connection.test_connection()
    
    cursor = conn.cursor()
    cursor.execute(f"SELECT GET_FILE_ID('{username}', '{file_name}');")
    id = None
    user_results = cursor.fetchall()
    for result in user_results:
        id = result[0]  # friend index is 8
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()
    
    return id


def GET_FILES(username):
    conn = connection.test_connection()

    print('GET FILES: ', username)
    cursor = conn.cursor()
    cursor.execute(f"SELECT GET_FILES('{username}');")
    user_files = []
    files = cursor.fetchall()
    for file in files:
        file = file[0][1:-1].split(",")
        user_files.append([file[1], file[3], file[5], file[2]])  # friend index is 8
    file_names = ""
    descriptions = ""
    dates = ""
    sizes = ""
    for i in user_files:
        filename = i[0].split('/')[-1]  # split the string by / and get the last for filename\
        file_names += filename + "//"

        description = i[1]
        descriptions += str(description) + "//"

        t = str(i[2])
        dates += t + "//"

        size = str(i[3])
        sizes += size + "//"

    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()

    return file_names, descriptions, dates, sizes


def CHECK_IF_ALREADY_FOLLOWING(asker, target):
    following_array = GET_FOLLOWING(asker)
    if target in following_array:      
        return True
    else:
        return False


def CREATE_MANSURA_TABLE():
    conn = connection.test_connection()
    cursor = conn.cursor()
    # cursor.execute("""DROP TABLE IF EXISTS SUBSCRIPTIONS_MENSURA;""")
    cursor.execute(
        f"""
        CREATE TABLE SUBSCRIPTIONS_MENSURA
        (
        mansura_Subscription_Id SERIAL PRIMARY KEY,   
        Username varchar,        
        Subscribed boolean,
        Date_Time timestamp,-- NOT NULL DEFAULT CURRENT_DATE      
        FOREIGN KEY (Username) REFERENCES USERS(Username)
        );
        """)
    conn.commit()
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()

    # print_green("SUBSCRIPTIONS_MENSURA\n")

# generally reset related --------------------------

def GET_CURRENT_DATE():
    conn = connection.test_connection()

    cursor = conn.cursor()
    cursor.execute(f"""SELECT 
        CURRENT_TIMESTAMP;
    """)
    results = cursor.fetchall()
    month = ""
    for i in results:
        # print("current month", i)
        month = i
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()
    
    return month[0]


def USER_SUBSCRIBE_FEE(username):
    conn = connection.test_connection()
    
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
        CALL USER_MONTHLY_SUBSCRIPTION_FEE('{username}') -- USER PAYMENT
        """)
        conn.commit()

        # CLOSE CURSOR AND CONNECTION [MANDATORY]        
        cursor.close()
        conn.close()
        # print(f"TOOK MONEY FROM -- {username}")
        return True
    except Exception as e:
        cursor.execute("ROLLBACK")
        print(f"ERROR:  [USER_SUBSCRIBE_FEE] {username}" + str(e))   
        
        # CLOSE CURSOR AND CONNECTION [MANDATORY]        
        cursor.close()
        conn.close()

        return False


def TEST_SELECT_ALL_PAYOUTS():
    conn = connection.test_connection()
    
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * FROM PAYOUTS
    """)
    results = cursor.fetchall()
    print()
    for value in results:
        daily = value[1]
        monthly = value[2]
        yearly = value[3]

        print("DAILY POOL  :",daily)
        print("MONTHLY POOL:",monthly)
        print("YEARLY POOL :",yearly)
        print()
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()


def USER_SUBSCRIBE_UPDATE_PAYOUTS():
    conn = connection.test_connection()
    
    cursor = conn.cursor()
    try: # decimal cast is so there is a round function available 
        # https://stackoverflow.com/questions/58731907/error-function-rounddouble-precision-integer-does-not-exist
        cursor.execute(f"""
        UPDATE PAYOUTS
        SET Daily = ROUND((Daily + 0.8)::Decimal, 2), Monthly=ROUND((Monthly+ 4.0)::Decimal, 2), Yearly = ROUND((Yearly + 0.2)::Decimal, 2) 
        
        """)
        conn.commit()
        TEST_SELECT_ALL_PAYOUTS()
               
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("ERROR:  [USER_SUBSCRIBE_UPDATE_PAYOUTS " + str(e))        
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()        


def USER_SUBSCRIBE_FULL(username):
    conn = connection.test_connection()
    # print("FUNC: USER_SUBSCRIBE_FULL")
    cursor = conn.cursor()
    if USER_SUBSCRIBE_INSERT( username):
            # STEP 2
        if USER_SUBSCRIBE_FEE(username):
                # STEP 3 
            USER_SUBSCRIBE_UPDATE_PAYOUTS()
            return True
        else:
            print(F"STEP 2 USER_SUBSCRIBE_FEE {username} failed")
            
            # CLOSE CURSOR AND CONNECTION [MANDATORY]        
            cursor.close()
            conn.close()
            return False
    else:
        print(F"STEP 1 USER SUBSCRIBE INSERT {username} failed")
        return False


def CREATE_PAYOUTS_TABLE():
    conn = connection.test_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""DROP TABLE IF EXISTS PAYOUTS;""")
        cursor.execute(
                f"""
                CREATE TABLE PAYOUTS
                (
                    Payout_Id SERIAL PRIMARY KEY,
                    Daily real,
                    Monthly real,
                    Yearly real                 
                );
                """)
        conn.commit()
        
        print("created")
        # print_green("CREATE_PAYOUTS_TABLE\n")
        
        # INITAL 0'S INSERT
        cursor.execute(f"""
            INSERT INTO PAYOUTS(Daily, Monthly, Yearly)
            VALUES (0.0, 0.0, 0.0)
            """)
        conn.commit()
        cursor.close()
    except Exception as e:
        cursor.execute("ROLLBACK")
        print_error("\nHAD TO ROLLBACK [CREATE_PAYOUTS_TABLE]: ", e)
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close() 


def GET_TOTAL_DATASET_MARKET_SHARE_BY_TIME(type):
    conn = connection.test_connection()
    
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
        SELECT count(*) 
        FROM FILES as F
        
        INNER JOIN FILE_VOTES votes
        ON F.File_Id = votes.File_id

        WHERE votes.Vote_Type = '{type}'

        
        """)
        conn.commit()

        results = cursor.fetchall()
        num_votes = 0
        for value in results:
            # print(F"TOTAL {type} VOTES: ", value[0])
            num_votes = value[0]
        
        # CLOSE CURSOR AND CONNECTION [MANDATORY]        
        cursor.close()
        conn.close()

        return num_votes
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("ERROR:  [USER_SUBSCRIBE_FULL] " + str(e))
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()


def GET_DAILY_PAYOUTS():
    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * FROM PAYOUTS
    """)
    results = cursor.fetchall()
    print()
    for value in results:
        daily = value[1]
        #monthly = value[2]
        #yearly = value[3]

        print("DAILY POOL  :",daily)

    CLOSE_CURSOR_AND_CONN(cursor, conn)
    return daily 


def GET_MONTHLY_PAYOUTS():
    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * FROM PAYOUTS
    """)
    results = cursor.fetchall()
    print()
    for value in results:
        #daily = value[1]
        monthly = value[2]
        #yearly = value[3]

        print("MONTHLY POOL  :", monthly)
    CLOSE_CURSOR_AND_CONN(cursor, conn)

    return monthly  


def GET_YEARLY_PAYOUTS():
    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * FROM PAYOUTS
    """)
    results = cursor.fetchall()
    print()
    for value in results:
        #daily = value[1]
        #monthly = value[2]
        yearly = value[3]

        print("YEARLY POOL  :", yearly)
    CLOSE_CURSOR_AND_CONN(cursor, conn)
    return yearly 


def GET_USER_BALANCE_SIMPLE(username):
    conn = connection.test_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            SELECT balance 
            FROM USERS
            WHERE username = '{username}'
        
        """)
        results = cursor.fetchall()
        for value in results:
            # print(value[0])
            CLOSE_CURSOR_AND_CONN(cursor, conn)
            return float(value[0])
    except Exception as e:
        cursor.execute("ROLLBACK")
        print(e)
    CLOSE_CURSOR_AND_CONN(cursor, conn)


def TRANSFER_EQUITY(buyer, seller, amount):
    # print_green(F"\nTRANSFERING EQUITY FROM {seller} -> {buyer} : {amount}")
    conn = connection.test_connection()
    cursor = conn.cursor()
    
    
    cursor.execute(f"""
    -- TRANSACTION
    BEGIN;
        INSERT INTO EQUITY (username, percentage)
        VALUES('{buyer}', 0)       
        ON CONFLICT DO NOTHING;   
            
        UPDATE EQUITY SET percentage = percentage + {amount}
        WHERE username = '{buyer}';
            
        UPDATE EQUITY SET percentage = percentage - {amount}
        WHERE username = '{seller}';
            
        COMMIT;
        """)
    conn.commit()
    CLOSE_CURSOR_AND_CONN(cursor, conn)

def EQUITY_INSERT():
        
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
            INSERT INTO EQUITY(username, percentage)
            VALUES ('foreandr', 100)
    """)
    conn.commit()

def EQUITY_CREATE_TABLE():
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS EQUITY;")
    cursor.execute(f"""
    CREATE TABLE EQUITY 
    (
        username varchar(200) UNIQUE,
        percentage Decimal,
        FOREIGN KEY (username) REFERENCES USERS(username)
    );
    """)

    cursor.execute(
        f"""
        INSERT INTO EQUITY  (username, percentage)
        VALUES('foreandr', 100)
        """)
    conn.commit()

    CLOSE_CURSOR_AND_CONN(cursor, conn)



def home_dataset_function(page_no, sort_time_frame, how_many, session_username='None'):
    conn = connection.test_connection()
    cursor = conn.cursor() 
    cursor.execute(f"""
        SELECT 
            U.username, --0
            (                   --1
                SELECT balance
                FROM USERS 
                WHERE username = '{session_username}'
             
            ),  
            F.File_PATH, --2
            F.Date_Time, --3
            F.Post_total_size, --4
            F.Post_foreign_id_source,--5
            F.File_id,--6
                   
            ( --7
                SELECT COUNT(*) -- daily num votes LEFT
                FROM FILE_VOTES file_vote 
                WHERE Vote_Type = 'Daily'
                AND Voter_Username = '{session_username}'
                AND Date_Time >= date_trunc('day', now())::date
            ),
            ( --8
                SELECT COUNT(*) -- monthly num votes LEFT
                FROM FILE_VOTES file_vote
                WHERE Vote_Type = 'Monthly'
                AND Voter_Username = '{session_username}'
                AND Date_Time >= date_trunc('month', now())::date
            ),
            (   --9
                SELECT COUNT(*) -- yearly num votes LEFT
                FROM FILE_VOTES file_vote
                WHERE Vote_Type = 'Yearly'
                AND Voter_Username = '{session_username}'
                AND Date_Time >= date_trunc('year', now())::date
            ),
            (   --10
                SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
                FROM FILE_VOTES file 
                WHERE file.File_id = F.File_id 
                AND Vote_Type = 'Daily'
            ),
            (   --11
                SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
                FROM FILE_VOTES file 
                WHERE file.File_id = F.File_id 
                AND Vote_Type = 'Monthly'
            ),
            (   --12
                SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
                FROM FILE_VOTES file 
                WHERE file.File_id = F.File_id 
                AND Vote_Type = 'Yearly'
            ), 
            (SELECT Daily FROM PAYOUTS) -- 13 PAYMENT INFO                                                   
        FROM FILES F
        
        INNER JOIN USERS U
        on U.username = F.Uploader

        ORDER BY GET_FILE_VOTE_COUNT_TYPED(F.File_Id, '{sort_time_frame}') DESC

        OFFSET (({page_no} - 1) * 100) 
        LIMIT {how_many}; 
    """)


    File_ids = ""
    usernames = ""
    paths = ""
    dates = ""
    Post_total_size = ""
    post_sources = ""
    day_votes = ""
    month_votes = ""
    year_votes = ""
    total_votes = ""
    dailypool = ""
    monthlypool = ""
    yearlypool = ""
    daily_left = ""
    monthly_left = ""
    yearly_left = ""
    user_balance = ""

    home_dataset_info = cursor.fetchall()
    for i in home_dataset_info:
        #print(i)
        usernames += i[0] + "//"
        user_balance = str(i[1])
        paths += str(i[2]) + "//"
        dates += str(i[3]) + "//"
        Post_total_size += str(i[4]) + "//"
        post_sources += str(i[5]) + "//"
        File_ids += str(i[6]) + "//"      
        daily_left = str(i[7])
        monthly_left = str(i[8])
        yearly_left = str(i[9])

        day_votes += str(i[10]) + "//"
        month_votes +=  str(i[11]) + "//"
        year_votes +=  str(i[12]) + "//"
        total_votes_ = i[10] + i[11] + i[12]
        total_votes += str(total_votes_) + "//"
        
    if CHECK_DATE( session_username):
        #print(session_username, " IS SUBSCRIBED")
        daily_left =  1 if (int(daily_left) == 0) else 0
        monthly_left = 1 if (int(monthly_left) == 0) else 0
        yearly_left = 1 if (int(yearly_left) == 0) else 0
    else:
        daily_left, monthly_left, yearly_left = 0, 0, 0

    cursor.execute(f"""
    SELECT * 
    FROM PAYOUTS
    """)
    pools = cursor.fetchall()
    for i in pools:
        # print(i, len(i))
        dailypool = i[1]
        monthlypool = i[2]
        yearlypool = i[3]
    
    '''
    print(f"""\nHOME DETAILS:
        0:  {usernames}
        1:  {user_balance}
        2:  {paths}
        3:  {dates}
        4:  {Post_total_size}
        5:  {File_ids}
        6:  {post_sources}
        7:  {daily_left}    {session_username} DAILY VOTES LEFT
        8:  {monthly_left}    {session_username} MONTHLY VOTES LEFT
        9:  {yearly_left}    {session_username} YEARLY VOTES LEFT
        10: {day_votes}
        11: {month_votes}
        12: {year_votes}
        13: {total_votes}
        14: {dailypool}
        15: {monthlypool}
        16: {yearlypool}
        """)
    '''        
    
    CLOSE_CURSOR_AND_CONN(cursor, conn)
    return File_ids, usernames, paths, dates, Post_total_size, post_sources, daily_left, monthly_left, yearly_left, day_votes, month_votes, year_votes, total_votes, dailypool, monthlypool, yearlypool


def profile_dataset_function(session_username):
    conn = connection.test_connection()
    cursor = conn.cursor() 
    cursor.execute(f"""
        SELECT 
            U.username, --0
            (                   --1
                SELECT balance
                FROM USERS 
                WHERE username = '{session_username}'
             
            ),  
            F.File_PATH, --2
            F.Date_Time, --3
            F.Post_total_size, --4
            F.Post_foreign_id_source,--5
            F.File_id,--6
                   
            ( --7
                SELECT COUNT(*) -- daily num votes LEFT
                FROM FILE_VOTES file_vote 
                WHERE Vote_Type = 'Daily'
                AND Voter_Username = '{session_username}'
                AND Date_Time >= date_trunc('day', now())::date
            ),
            ( --8
                SELECT COUNT(*) -- monthly num votes LEFT
                FROM FILE_VOTES file_vote
                WHERE Vote_Type = 'Monthly'
                AND Voter_Username = '{session_username}'
                AND Date_Time >= date_trunc('month', now())::date
            ),
            (   --9
                SELECT COUNT(*) -- yearly num votes LEFT
                FROM FILE_VOTES file_vote
                WHERE Vote_Type = 'Yearly'
                AND Voter_Username = '{session_username}'
                AND Date_Time >= date_trunc('year', now())::date
            ),
            (   --10
                SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
                FROM FILE_VOTES file 
                WHERE file.File_id = F.File_id 
                AND Vote_Type = 'Daily'
            ),
            (   --11
                SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
                FROM FILE_VOTES file 
                WHERE file.File_id = F.File_id 
                AND Vote_Type = 'Monthly'
            ),
            (   --12
                SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
                FROM FILE_VOTES file 
                WHERE file.File_id = F.File_id 
                AND Vote_Type = 'Yearly'
            ), 
            (SELECT Daily FROM PAYOUTS) -- 13 PAYMENT INFO
                                                   
        FROM FILES F
        
        INNER JOIN USERS U
        on U.username = F.Uploader

        WHERE U.username = '{session_username}'
        
        ORDER BY F.Date_Time
    """)


    File_ids = ""
    usernames = ""
    paths = ""
    dates = ""
    Post_total_size = ""
    post_sources = ""
    day_votes = ""
    month_votes = ""
    year_votes = ""
    total_votes = ""
    daily_left = ""
    monthly_left = ""
    yearly_left = ""
    user_balance = ""

    home_dataset_info = cursor.fetchall()
    for i in home_dataset_info:
        # print(i)
        usernames += i[0] + "//"
        user_balance = str(i[1])
        paths += str(i[2]) + "//"
        dates += str(i[3]) + "//"
        Post_total_size += str(i[4]) + "//"
        post_sources += str(i[5]) + "//"
        File_ids += str(i[6]) + "//"      
        daily_left = str(i[7])
        monthly_left = str(i[8])
        yearly_left = str(i[9])

        day_votes += str(i[10]) + "//"
        month_votes +=  str(i[11]) + "//"
        year_votes +=  str(i[12]) + "//"
        total_votes_ = i[10] + i[11] + i[12]
        total_votes += str(total_votes_) + "//"
    
    if CHECK_DATE(session_username):
        # NULLS CAUSE PROBLEMS HERE
        print(session_username, " IS SUBSCRIBED")
        if daily_left != "":
            daily_left =  1 if (int(daily_left) == 0) else 0
        else:
             daily_left = GET_NUM_FILE_VOTES_LEFT(session_username, 'Daily')
        
        if monthly_left != "":
            monthly_left =  1 if (int(daily_left) == 0) else 0
        else:
             monthly_left = GET_NUM_FILE_VOTES_LEFT(session_username, 'Monthly')
        
        if yearly_left != "":
            yearly_left =  1 if (int(daily_left) == 0) else 0
        else:
            yearly_left = GET_NUM_FILE_VOTES_LEFT(session_username, 'Yearly')
             
    else:
        daily_left, monthly_left, yearly_left = 0,0,0

    cursor.execute(f"""
    SELECT * 
    FROM PAYOUTS
    """)
    pools = cursor.fetchall()
    for i in pools:
        # print(i, len(i))
        dailypool = i[1]
        monthlypool = i[2]
        yearlypool = i[3]
  
    '''
        print(f"""\nHOME DETAILS:
    0:  {usernames}
    1:  {user_balance}
    2:  {paths}
    3:  {dates}
    4:  {Post_total_size}
    5:  {File_ids}
    6:  {post_sources}
    7:  {daily_left}    {session_username} DAILY VOTES LEFT
    8:  {monthly_left}    {session_username} MONTHLY VOTES LEFT
    9:  {yearly_left}    {session_username} YEARLY VOTES LEFT
    10: {day_votes}
    11: {month_votes}
    12: {year_votes}
    13: {total_votes}
    """)
    '''
    CLOSE_CURSOR_AND_CONN(cursor, conn)
    return File_ids, usernames, paths, dates, Post_total_size, post_sources, daily_left, monthly_left, yearly_left, day_votes, month_votes, year_votes, total_votes, user_balance, dailypool, monthlypool, yearlypool


def FILE_INSERT_STORAGE(username, path_name, text, age_18, external_source):
    # print(f"username: {username}\npath_name: {path_name}\ntext: {text}\nmy_file: {my_file}\nage_18: {age_18}\nexternal_source: {external_source}")
    
    try:
        target = rf'static/#UserData/{username}/files/{path_name}/post_text.txt' # WRITING TEXT PART   
        with open(target, 'w') as f:
            f.write(text)
    except Exception as e:
        print(str(e) + " TEXT")
    
        
    try:
        target = rf'static/#UserData/{username}/files/{path_name}/age_18.txt' # WRITING TEXT PART   
        with open(target, 'w') as f:
            f.write(age_18)
    except Exception as e:
        print(str(e) + " 18")
        
        
    try:
        target = rf'static/#UserData/{username}/files/{path_name}/external_source.txt' # WRITING TEXT PART   
        with open(target, 'w') as f:
            f.write(external_source)
    except Exception as e:
        print(str(e) + " SOURCE?")


def CHECK_FILES_NOT_OVER_LIMIT(page_no):
    conn = connection.test_connection()
    print("CHECK_FILES_NOT_OVER_LIMIT", page_no)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT * 
        FROM FILES 
        OFFSET (({page_no} - 1) * 100)

        """)
    results = cursor.fetchall()
    # print(len(results))
    if (len(results)) > 1:
        CLOSE_CURSOR_AND_CONN(cursor, conn)
        return True
    else:
        CLOSE_CURSOR_AND_CONN(cursor, conn)
        return False


def CLOSE_CURSOR_AND_CONN(cursor, conn):
    cursor.close()
    conn.close()


def GET_SINGLE_DATASET_INFO(filename):
    # print(f"GET_SINGLE_DATASET_INFO [\t{filename}]\n")
    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT file.Uploader, file.File_PATH, file.UserId, file.Post_foreign_id_source, file.Date_Time, file.File_id
        FROM FILES file
        WHERE file.File_PATH = '{filename}'
    """)
    
    info_array = []
    info = cursor.fetchall() 

    for i in info: # SHOULD ONLY ITER ONCE SO COMPLEXITY NOT AN ISSUE
        # print(i[0])
        for j in i:
            # print(j)
            info_array.append(j)
    #for i in info_array:
    #    print(i)
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    CLOSE_CURSOR_AND_CONN(cursor, conn)

    return info_array[0], info_array[1], info_array[2], info_array[3], info_array[4], info_array[5]


def GET_NUM_REPLIES(file_id):
    # print(f"GET_NUM_REPLIES [{file_id}]\n")
    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COUNT(*)
        FROM FILES file
        WHERE file.Post_foreign_id_source = '{file_id}'
    """)

    info = cursor.fetchall() 
    for i in info:
        num = i[0]
    # print(num)
    CLOSE_CURSOR_AND_CONN(cursor, conn)
    return num


def GET_ALL_REPLIES(file_id):
    # print(f"GET_ALL_REPLIES [{file_id}]\n")
    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT file.Uploader, file.File_PATH, file.UserId, file.Post_foreign_id_source, file.Date_Time, file.File_id
        FROM FILES file
        WHERE file.Post_foreign_id_source = '{file_id}'
    """)
    info_array = []
    info = cursor.fetchall() 
    for i in info:
        # print(i)
        info_array.append(i)
    
    #for i in info_array:
    #     print(i)

    CLOSE_CURSOR_AND_CONN(cursor, conn)
    return info_array


def GET_NUM_VOTES_FOR_EACH_TYPE(file_id): # this might be a dupe butI'm not going to check right now
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT 
                (   --10
                    SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
                    FROM FILE_VOTES file 
                    WHERE file.File_id = F.File_id 
                    AND Vote_Type = 'Daily'
                ),
                (   --11
                    SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
                    FROM FILE_VOTES file 
                    WHERE file.File_id = F.File_id 
                    AND Vote_Type = 'Monthly'
                ),
                (   --12
                    SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
                    FROM FILE_VOTES file 
                    WHERE file.File_id = F.File_id 
                    AND Vote_Type = 'Yearly'
                )
                                                   
        FROM FILES F

        WHERE F.File_Id = '{file_id}'
    """)

    
    info_array = []
    results = cursor.fetchall()
    for i in results:
        #print("RESULTS-----", i)
        info_array.append(i)
    CLOSE_CURSOR_AND_CONN(cursor, conn)
    return info_array
    

def GET_UPLOAD_DATES_BY_ID(file_id):
    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT file.Date_Time
        FROM FILES file
        WHERE file.Post_foreign_id_source = '{file_id}'
    """)
    info_array = []
    info = cursor.fetchall() 
    for i in info:
        info_array.append(i)
        #print("DATE GOTTEN1",info_array)
        #print("DATE GOTTEN2",info_array[0])
        #print("DATE GOTTEN3", info_array[0][0] )
        return info_array[0][0] 

    CLOSE_CURSOR_AND_CONN(cursor, conn)


def post_dataset_function(file_id, session_username):
    conn = connection.test_connection()
    cursor = conn.cursor() 
    # GETTING INFO FOR MULTIPLE 
    cursor.execute(f"""
        SELECT 
            F.File_PATH, --0
            F.Date_Time, --1
            F.Post_total_size, --2
            F.Post_foreign_id_source,--3
            F.File_id,--4
                   
            ( --5
                SELECT COUNT(*) -- daily num votes LEFT
                FROM FILE_VOTES file_vote 
                WHERE Vote_Type = 'Daily'
                AND Voter_Username = '{session_username}'
                AND Date_Time >= date_trunc('day', now())::date
            ),
            ( --6
                SELECT COUNT(*) -- monthly num votes LEFT
                FROM FILE_VOTES file_vote
                WHERE Vote_Type = 'Monthly'
                AND Voter_Username = '{session_username}'
                AND Date_Time >= date_trunc('month', now())::date
            ),
            (   --7
                SELECT COUNT(*) -- yearly num votes LEFT
                FROM FILE_VOTES file_vote
                WHERE Vote_Type = 'Yearly'
                AND Voter_Username = '{session_username}'
                AND Date_Time >= date_trunc('year', now())::date
            ),
            (   --8
                SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
                FROM FILE_VOTES file 
                WHERE file.File_id = F.File_id 
                AND Vote_Type = 'Daily'
            ),
            (   --9
                SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
                FROM FILE_VOTES file 
                WHERE file.File_id = F.File_id 
                AND Vote_Type = 'Monthly'
            ),
            (   --10
                SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
                FROM FILE_VOTES file 
                WHERE file.File_id = F.File_id 
                AND Vote_Type = 'Yearly'
            ), 
            (
                SELECT U.balance -- yearly num votes LEFT
                FROM USERS U
                WHERE Username = '{session_username}'
            ),
            (SELECT Daily FROM PAYOUTS), 
            (SELECT Monthly FROM PAYOUTS), 
            (SELECT Yearly FROM PAYOUTS),
            (   
                    SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
                    FROM FILE_VOTES file 
                    WHERE file.File_id = F.File_id 
                    AND Vote_Type = 'Daily'
            ), 
            (   --11
                    SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
                    FROM FILE_VOTES file 
                    WHERE file.File_id = F.File_id 
                    AND Vote_Type = 'Monthly'
            ),
            (   --12
                    SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
                    FROM FILE_VOTES file 
                    WHERE file.File_id = F.File_id 
                    AND Vote_Type = 'Yearly'
            )


                                                   
        FROM FILES F

        WHERE F.Post_foreign_id_source = '{file_id}'
        
        ORDER BY F.Date_Time
    """)

    File_ids = ""
    #usernames = ""
    paths = ""
    dates = ""
    Post_total_size = ""
    post_sources = ""

    day_votes = ""
    month_votes = ""
    year_votes = ""
    total_votes = ""
    
    daily_left = ""
    monthly_left = ""
    yearly_left = ""

    user_balance = ""

    dailypool =""
    monthlypool = ""
    yearlypool = ""

    daily_dataset_votes = ""
    monthly_dataset_votes = ""
    yearly_dataset_votes = ""
    home_dataset_info = cursor.fetchall()
    for i in home_dataset_info:
        # print(i)
        #usernames += i[0] + "//"
        user_balance = str(i[11])
        paths += str(i[0]) + "//"
        dates += str(i[1]) + "//"
        Post_total_size += str(i[2]) + "//"
        post_sources += str(i[3]) + "//"
        File_ids += str(i[4]) + "//"      
        daily_left = str(i[5])
        monthly_left = str(i[6])
        yearly_left = str(i[7])

        day_votes += str(i[8]) + "//"
        month_votes +=  str(i[9]) + "//"
        year_votes +=  str(i[10]) + "//"
        total_votes_ = i[8] + i[9] + i[10]
        total_votes += str(total_votes_) + "//"
        dailypool = str(i[12])
        monthlypool = str(i[13])
        yearlypool = str(i[14])
        
        daily_dataset_votes = str(i[15])
        monthly_dataset_votes = str(i[16])
        yearly_dataset_votes = str(i[17])
    
    if CHECK_DATE(session_username):
        # NULLS CAUSE PROBLEMS HERE
        print(session_username, " IS SUBSCRIBED")
        if daily_left != "":
            daily_left =  1 if (int(daily_left) == 0) else 0
        else:
             daily_left = GET_NUM_FILE_VOTES_LEFT(session_username, 'Daily')
        
        if monthly_left != "":
            monthly_left =  1 if (int(daily_left) == 0) else 0
        else:
             monthly_left = GET_NUM_FILE_VOTES_LEFT(session_username, 'Monthly')
        
        if yearly_left != "":
            yearly_left =  1 if (int(daily_left) == 0) else 0
        else:
            yearly_left = GET_NUM_FILE_VOTES_LEFT(session_username, 'Yearly')       
    else:
        daily_left, monthly_left, yearly_left = 0,0,0
    
    print(f"""\npost:
            0:  paths
            1:  dates
            2:  sizes
            3:  {File_ids}
            4:  {post_sources}
            5:  {daily_left}    {session_username} DAILY VOTES LEFT
            6:  {monthly_left}    {session_username} MONTHLY VOTES LEFT
            7:  {yearly_left}    {session_username} YEARLY VOTES LEFT
            8:  dailyvotes  :{day_votes}
            9:  monthlyvotes:{month_votes}
            10: yearlyvotes :{year_votes}
            11: totalvotes  :{total_votes}
            12: daily:{dailypool}
            13: monthly:{monthlypool}
            14: yearly:{yearlypool}
            15: BALANCE: {user_balance} 
            16: MAIN VOTES D:{daily_dataset_votes}
            17: MAIN VOTES M:{monthly_dataset_votes}
            18: MAIN VOTES Y:{yearly_dataset_votes}
    """)
    
    CLOSE_CURSOR_AND_CONN(cursor, conn)
    return File_ids, paths, dates, Post_total_size, post_sources, daily_left, monthly_left, yearly_left, day_votes, month_votes, year_votes, total_votes, user_balance, dailypool, monthlypool, yearlypool, daily_dataset_votes, monthly_dataset_votes, yearly_dataset_votes


def GET_USERNAME_BY_EMAIL(paypal_email):
    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT username
        FROM USERS 
        WHERE paypal_email = '{paypal_email}'
    """)
    try:
        result = cursor.fetchall()
        list_of_names = []
        if result == []: #EMPTY FOR SOME REASON
            print(F"I SUSPECT THIS [ {paypal_email} ] doesn't exist but it could be something else")

            cursor.close()
            conn.close()

            return "NO EMAIL"
        for i in result:
            print(i[0])
            return i[0]
            
            cursor.close()
            conn.close()
        # return list_of_names
    except Exception as e:
        print(e)

        cursor.close()
        conn.close()

        return "NO EMAIL"


def SUBSCRIBE_FROM_PAYAPL_BUY(buyer_email):
    print(F"SUBSCRIBING {buyer_email}")
    username = GET_USERNAME_BY_EMAIL(buyer_email)
    if username == "NO EMAIL":
        return f"CANNOT SUBSCRIBE {buyer_email}"
    
    ADD_SUB_FUNDS_5(username)
    MANSURA_SUBSCRIBE(username)


def ADD_SUB_FUNDS_5(username, amount=5):
    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        UPDATE USERS 
        SET balance = balance + {amount}
        WHERE username = '{username}';
    """)

    conn.commit()
    cursor.close()
    conn.close()

    
def WITHDRAWL_FUNCTION(username, withdrawl_amount=2):
    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        UPDATE USERS 
        SET balance = balance - {withdrawl_amount}
        WHERE username = '{username}';
    """)

    conn.commit()   
    cursor.close()
    conn.close()


def CHECK_FILE_EXISTS(File_id_):
        
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT File_Id FROM FILES WHERE File_id = {File_id_}""")
    num = 0
    for i in cursor.fetchall():
        print(i)
        num+=1
    # print(f"found {num} files")

    cursor.close()
    conn.close()

    if num > 0:
        return True
    else:
        return False


def SEARCH_ALGO_CREATE_TABLE():
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS SEARCH_ALGORITHMS""")
    cursor.execute(
        f"""
        CREATE TABLE SEARCH_ALGORITHMS
        (
        Search_id SERIAL PRIMARY KEY,   
        Username varchar,
        Search_Path varchar UNIQUE,
        Algorithm_Name varchar UNIQUE,
        Date_Time timestamp,      
        FOREIGN KEY (Username) REFERENCES USERS(Username)
        );
        """)
    conn.commit()
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()


def SEARCH_ALGO_INSERT(username, Algorithm_Name, order_by_clause, where_clause):
    conn = connection.test_connection()
    cursor = conn.cursor() 
    # 1. GET NUM FILES 
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM SEARCH_ALGORITHMS
    """)  
    count = cursor.fetchone()[0] + 1
    new_path = username + "-" + str(count) 
    # print(count)

    # 2. INSERT INTO TABLE
    cursor.execute(
    f"""
    INSERT INTO SEARCH_ALGORITHMS
        (Username, Search_Path, Algorithm_Name, Date_Time)
    VALUES
        ('{username}', '{new_path}', '{Algorithm_Name}', CURRENT_TIMESTAMP );
    """)        
    conn.commit()

    # 3. SAVE ORDER AND WHERE CLAUSE INTO FOLDER

    my_path = F"/root/mansura/static/#UserData/{username}/search_algorithms/{new_path}.json" 
    config_json = {
        'ORDER_BY_CLAUSE':f"{order_by_clause}",
        'WHERE_CLAUSE'   :f"{where_clause}"
    }
    jsonString = json.dumps(config_json)
    jsonFile = open(f"{my_path}", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()

    #TODO: EVENTUALLY I SHOULD RUN THESE AGAINST A TESTNET OR SOMETHING AUTOMATICALLY AND JUST SEE IF THEY PRODUCE A RESULT
    #TODO: FOR NOW I WILL JUST CHECK THEM MANUALLY
    

def SEARCH_ALGO_INSERT_DEMO_MULTIPLE():
    SEARCH_ALGO_INSERT('foreandr', 'foreandr-basic-top-month', "ORDER BY U.username DESC", "")
    SEARCH_ALGO_INSERT('andrfore', 'andrfore-basic-top-month', "ORDER BY U.username ASC", f"AND U.username LIKE 'foreandr%'")
    print_green("SEARCH_ALGO_INSERT_DEMO_MULTIPLE()")


def universal_dataset_function(search_type, search_algo_path="foreandr-1", page_no="1", search_user="None", file_id="None", profile_username="None"):
    conn = conn = connection.test_connection()
    cursor = conn.cursor()
    """
    search type options rn ["home", "prof", "post"]
    return PARAMETER back to the browser in a list so the frontend has all the options when conducting another search(changing pages and whatnot)
    Todo: it might be worth explicitly setting the other things to their requisite values universally even though it's less elegant
    """
    POST_SEARCH_QUERIES = f"""
        (   
            SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
            FROM FILE_VOTES file 
            WHERE file.File_id = {file_id}
            AND Vote_Type = 'Daily'
        ), 
        (  
            SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
            FROM FILE_VOTES file 
            WHERE file.File_id = {file_id}
            AND Vote_Type = 'Monthly'
        ),
        (   
            SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
            FROM FILE_VOTES file 
            WHERE file.File_id = {file_id}
            AND Vote_Type = 'Yearly'
        )
        
        """
    '''
    print("QUERY DETAIL-------------------------")
    print("search_type           :", search_type)
    print("search_algo_path      :", search_algo_path)
    print("page_no               :", page_no)
    print("search_user           :", search_user)
    print("file_id               :", file_id)
    print("profile_username      :", profile_username)
    '''
    if search_type != "post":
        #payouts because small table, wasnt sure if size would effect query time
        POST_SEARCH_QUERIES = "(SELECT count(*) FROM PAYOUTS WHERE 1 = 0)" 
        foreign_id_text_entry = F"AND U.username = U.username" # a meaningless statement        
        if search_type == "prof":
            profile_search_clause = F"AND U.username = '{profile_username}'"      
        else:
            profile_search_clause = F"AND U.username = U.username"
    else:
        foreign_id_text_entry = F"AND F.Post_foreign_id_source = '{file_id}'"
        profile_search_clause = F"AND U.username = U.username"




    order_by_clause, where_clause = GRAB_SEARCH_ALGO(search_algo_path)

    cursor.execute(f"""
        SELECT
            F.File_id, 
            U.username, 
            (               
                SELECT balance 
                FROM USERS 
                WHERE username = '{search_user}'
             
            ),  
            F.File_PATH, 
            F.Date_Time, 
            F.Post_foreign_id_source, 

                   
            ( 
                SELECT COUNT(*) -- daily num votes LEFT 
                FROM FILE_VOTES file_vote 
                WHERE Vote_Type = 'Daily'
                AND Voter_Username = '{search_user}'
                AND Date_Time >= date_trunc('day', now())::date
            ),
            ( 
                SELECT COUNT(*) -- monthly num votes LEFT
                FROM FILE_VOTES file_vote
                WHERE Vote_Type = 'Monthly'
                AND Voter_Username = '{search_user}'
                AND Date_Time >= date_trunc('month', now())::date
            ),
            (  
                SELECT COUNT(*) -- yearly num votes LEFT FOR X USER
                FROM FILE_VOTES file_vote
                WHERE Vote_Type = 'Yearly'
                AND Voter_Username = '{search_user}'
                AND Date_Time >= date_trunc('year', now())::date
            ),
            (   
                SELECT COUNT(*) -- DAILY VOTESFOR ALL DATASETS!
                FROM FILE_VOTES file 
                WHERE file.File_id = F.File_id 
                AND Vote_Type = 'Daily'
            ),
            (   
                SELECT COUNT(*) -- MONTHLY VOTES FOR ALL DATASETS!
                FROM FILE_VOTES file 
                WHERE file.File_id = F.File_id 
                AND Vote_Type = 'Monthly'
            ),
            (   
                SELECT COUNT(*) -- YEARLY VOTES FOR ALL DATASETS!
                FROM FILE_VOTES file 
                WHERE file.File_id = F.File_id 
                AND Vote_Type = 'Yearly'
            ), 

            --PAYOUT info
            (SELECT Daily FROM PAYOUTS),
            (SELECT Monthly FROM PAYOUTS),
            (SELECT Yearly FROM PAYOUTS),
            {POST_SEARCH_QUERIES}

        FROM FILES F
        
        INNER JOIN USERS U
        on U.username = F.Uploader

        WHERE U.username = U.username -- DO THIS SO ALL OTHERC ALUSES CAN BE AND CLAUSES
        {foreign_id_text_entry}
        {profile_search_clause}
        {where_clause}



        {order_by_clause}

        OFFSET (({page_no} - 1) * 100)
        LIMIT 100; 
    """)
    # -- ORDER BY GET_FILE_VOTE_COUNT_TYPED(F.File_Id, '{sort_time_frame}') DESC
    dataset_arguments = [search_type, search_algo_path, page_no, search_user, file_id]
    # print(F"ARGS: {dataset_arguments}")

    file_ids_list = []
    usernames_list = []
    paths_list = []
    dates_list = []
    post_sources_list = []
    day_votes = []
    month_votes = []
    year_votes = []
    total_votes = []

    #INDIVIDUAL USER
    daily_left = ""
    monthly_left = "" 
    yearly_left = ""
    user_balance = ""
    dailypool = ""
    monthlypool = ""
    yearlypool = ""

    daily_votes_singular = ""
    monthly_votes_singular = "" 
    yearly_votes_singular = ""

    for i in cursor.fetchall():
        # print(i)
        # POST INFOS
        file_ids_list.append(i[0])
        usernames_list.append(i[1])
        paths_list.append(i[3])
        dates_list.append(i[4])
        post_sources_list.append(i[5])
        day_votes.append(i[9])
        month_votes.append(i[10])
        year_votes.append(i[11])
        
        # SINGLE INFO
        user_balance = i[2]
        daily_left = i[6]
        monthly_left = i[7]
        yearly_left = i[8]
        dailypool = i[12]
        monthlypool = i[13]
        yearlypool = i[14]
        try:
            daily_votes_singular = (i[15])
            monthly_votes_singular = (i[16])
            yearly_votes_singular = (i[17])
        except:
            pass

    if daily_left != "":
        if CHECK_DATE(search_user):
            #print(session_username, " IS SUBSCRIBED")
            daily_left =  1 if (int(daily_left) == 0) else 0
            monthly_left = 1 if (int(monthly_left) == 0) else 0
            yearly_left = 1 if (int(yearly_left) == 0) else 0
        else:
            daily_left, monthly_left, yearly_left = 0, 0, 0
    '''
    print("\nCUSTOM QUERY               :", where_clause, order_by_clause)
    print("PROFILE SEARCH CLAUSE      :",profile_search_clause)
    print("FOREIGN ID                 :", foreign_id_text_entry)
    print("=============     QUERY RESULTS       ============")
    print("file_ids_list              :", file_ids_list)
    print("USERNAMES                  :", usernames_list)
    print("paths_list                 :", paths_list)
    # print("dates_list           :", dates_list)
    print("post_sources_list          :", post_sources_list)
    print("day_votes                  :", day_votes)
    print("month_votes                :", month_votes)
    print("year_votes                 :", year_votes)
    print("user_balance               :", user_balance)
    print("daily_left                 :", daily_left)
    print("monthly_left               :", monthly_left)
    print("yearly_left                :", yearly_left)
    print("dailypool                  :", dailypool)
    print("monthlypool                :", monthlypool)
    print("yearlypool                 :", yearlypool )
    
    print("POST_PAGE MAIN_DAILY       :", daily_votes_singular)
    print("POST_PAGE MAIN_MONTHLY     :", monthly_votes_singular)
    print("POST_PAGE MAIN_YEARLY      :", yearly_votes_singular)
    '''
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()

    return file_ids_list, usernames_list, paths_list, dates_list, post_sources_list, daily_left, monthly_left, yearly_left, day_votes, month_votes, year_votes, user_balance, dailypool, monthlypool, yearlypool, daily_votes_singular,  monthly_votes_singular, yearly_votes_singular


def GRAB_SEARCH_ALGO(search_algo_path):
    # THIS PRESUPPOSED THE ALGO HAS BEEN CHECKED ON TEST NETs
    
    # SHOULD HAVE SOME DEFAULT PUBLIC ORDER BY CLAUSES AS WELL
    # MAYBE IN THE BEGINNING, LET PEOPLE COMPOSE FUNCTIONS BEFORE I LET PEOPLE WRITE THEM
    # ON THE FUNCTIONS BEING COMPOSE, ATTACH A MODAL THAT YOU CAN CLICK TO ACTUALLY SEE THE CODE
    # SAME MONETIZATION METHOD
    # ALLOW PEOPLE TO SUGGEST THAT I IMPLEMENT A FUNCTION?
    # WHERE_CLAUSE = "WHERE NUM_ACCOUNTS_BLOCKING_USER(U.username) < 2" #or something like this
    # HAVE A NUMBER OF PUBLIC ALGORITHMS TO THE RIGHT THAT CAN BE ADDED AND MIXED UP IN ALL KINDS OF WAYS!!
    # NONE OF X, LOTS OF X

    #OPEN JSON FROM SEARCH ALGO PATH
    # print("SEARCH PATH:", search_algo_path)
    username = search_algo_path.split("-")[0]
    f = open(f'/root/mansura/static/#UserData/{username}/search_algorithms/{search_algo_path}.json')
    data = json.load(f)
    f.close()


    ORDER_BY_CLAUSE = data["ORDER_BY_CLAUSE"]
    WHERE_CLAUSE = data["WHERE_CLAUSE"]
    return [ORDER_BY_CLAUSE, WHERE_CLAUSE]


def GET_VOTES_AND_BALANCE_AND_PAYOUTS(username):
    conn = conn = connection.test_connection()
    cursor = conn.cursor()
    """
    REPLACING:

    daily_votes_left = database.GET_NUM_FILE_VOTES_LEFT( session["user"], "Daily")
    monthly_votes_left = database.GET_NUM_FILE_VOTES_LEFT( session["user"], "Monthly") 
    yearly_votes_left = database.GET_NUM_FILE_VOTES_LEFT( session["user"], "Yearly")
    balance = database.GET_USER_BALANCE_SIMPLE( session["user"])

    """
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT
        (               
            SELECT balance 
            FROM USERS 
            WHERE username = '{username}'
        ),  
        (
            SELECT COUNT(*)
            FROM FILE_VOTES csv 
            WHERE Vote_Type = 'Daily'
            AND Voter_Username = '{username}'
            AND Date_Time >= date_trunc('day', now())::date
        ),
        (
            SELECT COUNT(*)
            FROM FILE_VOTES csv 
            WHERE Vote_Type = 'Monthly'
            AND Voter_Username = '{username}'
            AND Date_Time >= date_trunc('month', now())::date
        ),
        (
            SELECT COUNT(*)
            FROM FILE_VOTES csv 
            WHERE Vote_Type = 'Yearly'
            AND Voter_Username = '{username}'
            AND Date_Time >= date_trunc('year', now())::date
        ),
        (SELECT Daily FROM PAYOUTS),
        (SELECT Monthly FROM PAYOUTS),
        (SELECT Yearly FROM PAYOUTS)


    """)
    conn.commit()
    results = cursor.fetchall()

    balance = ""
    daily_votes_left = ""
    monthly_votes_left = ""
    yearly_votes_left = ""
    daily_pool = ""
    monthly_pool = ""
    yearly_pool = ""

    for value in results:
        balance = value[0]
        daily_votes_left = value[1]
        monthly_votes_left = value[2]
        yearly_votes_left = value[3]
        daily_pool = value[4]
        monthly_pool = value[5]
        yearly_pool = value[6]
    
    return balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool
