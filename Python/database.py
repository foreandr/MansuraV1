import os
import shutil
from pathlib import Path
from sqlite3 import DatabaseError
# from django.db import transaction, DatabaseError
from PIL import Image
import datetime
import json
import re
import hashlib

from psycopg2 import Error
import Python.procedures as procedures
# from Python.db_connection import connection
from  Python.helpers import print_green, print_title, print_error, turn_pic_to_hex, check_and_save_dir, print_warning, log_function, TURN_WHERE_CLAUSE_TO_STRING, NLP_KEYWORD_EXTRACTOR, CREATING_EMBED_STRUCTURE
import Python.db_connection as connection
import Python.big_reset_file as big_reset_file
import Python.my_email as my_email

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
        log_function("error", e)


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
        log_function("error", e)
    
    cursor.close()
    conn.close()


def USER_INSERT_MULTIPLE(size="small"):
    conn = connection.test_connection()

    # Change the current working directory
    try:
        os.chdir("/mansura")
        shutil.rmtree('static/#UserData/')
    except Exception as e:
        print("could not remove static/#UserData/", e)


    full_register('a', hashlib.sha256("password".encode('utf-8')).hexdigest(), 'MensuraHost@gmail.com', 'MensuraHost@gmail.com', 5)
    full_register('foreandr', hashlib.sha256("password".encode('utf-8')).hexdigest(), 'foreandr@gmail.com', 'foreandr@gmail.com', 5)
    full_register('andrfore', hashlib.sha256("password".encode('utf-8')).hexdigest(), 'andrfore@gmail.com', 'andrfore@gmail.com', 5)
    full_register('cheatsie', hashlib.sha256("password".encode('utf-8')).hexdigest(), 'cheatsieog@gmail.com', 'cheatsieog@gmail.com', 5)
    full_register('dnutty', hashlib.sha256("password".encode('utf-8')).hexdigest(), 'dnutty@gmail.com', 'dnutty@gmail.com', 5)
    
    # ====

    big_reset_file.GIANT_USER_REGISTER(size)
 
    # --

    print_green("USER MULTI INSERT COMPLETED\n")


def USER_INSERT_MULTPLE_FILES(size="small"):
    big_reset_file.GIANT_FILE_INSERT(size)
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
                creation_date timestamp,
                
                FOREIGN KEY (User_Id1) REFERENCES USERS(User_Id),
                FOREIGN KEY (User_Id2) REFERENCES USERS(User_Id)
            );
        """)
    conn.commit()
    cursor.close()
    conn.close()
    print_green("CONNECTION TABLE CREATE COMPLETED\n")

def CREATE_TABLE_1_TIME_PASSWORDS():
    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute("""DROP TABLE IF EXISTS ONE_TIME_PASSWORDS;""")
    cursor.execute("""
        CREATE TABLE ONE_TIME_PASSWORDS
        (
            One_Time_Id SERIAL PRIMARY KEY,
            Email varchar UNIQUE,
            Generated_Pass_Code varchar,
            FOREIGN KEY (Email) REFERENCES USERS(Email)
        );
    """)
    conn.commit()
    conn.close()
    cursor.close()


def CREATE_ONE_TIME_PASS(length=10):
    import random
    import string
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
    # print("Random string of length", length, "is:", result_str)

def GET_ONE_TIME_PASS(email):
    conn = connection.test_connection()
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
    conn = connection.test_connection()
    cursor = conn.cursor()
    
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

def CREATE_AND_SEND_ONE_TIME_PASS_EMAIL(email):
    conn = connection.test_connection()
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
    
    my_email.send_email(email, password)


def CONNECTION_INSERT(user_id1, user_id2):
    conn = connection.test_connection()

    # print("INSERTING CONNECTION SERVER SIDE", user_id1, "->", user_id2)
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"""
                INSERT INTO CONNECTIONS (User_Id1, User_Id2, creation_date)
                VALUES({user_id1}, {user_id2}, NOW())
            """)
        conn.commit()
        # print_green(f"CONNECTED {user_id1} -> {user_id2}")
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("ERROR:  [INSERT INTO CONNECTIONS] " + str(e))
        log_function("error", e) 
    
    cursor.close()
    conn.close()
    # print_green('CONNECTION INSERT COMPLETED')


def CONNECTION_REMOVE(user_id_first, user_id_second):
    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"""
        CALL CUSTOM_DELETION({user_id_first}, {user_id_second});
        """)
    conn.commit()
    
    cursor.close()
    conn.close()
    print_green('CONNECTION DELETION COMPLETED')


def CONNECTION_INSERT_MULTIPLE(size="small"):
    CONNECTION_INSERT( user_id1=1, user_id2=2)
    CONNECTION_INSERT( user_id1=1, user_id2=3)
    big_reset_file.GIANT_CONNECTION_INSERT(size)
    
    print_green("USER MULTI INSERT CONNECTIONS COMPLETED\n")


def LIKES_CREATE_TABLE():
    conn = connection.test_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"DROP TABLE IF EXISTS LIKES ;")
        cursor.execute(
                f"""
                CREATE TABLE LIKES(
                    Like_Id SERIAL PRIMARY KEY,
                    File_id INT,
                    Liker_Username varchar(50),
                    Date_Time timestamp, 

                    ---CONSTRAINTS
                    FOREIGN KEY (File_id) REFERENCES FILES(File_id),
                    UNIQUE (File_id, Liker_Username) --this should allow someone to only have one like per post
                );
                """)
        conn.commit()

        print_green("LIKES CREATE COMPLETED\n")
    except Exception as e:
        
        cursor.execute("ROLLBACK")
        print_error("\nHAD TO ROLLBACK LIKES TABLE CREATION" + str(e) )
        # exit()

    cursor.close()
    conn.close()

def LIKES_INSERT(liker_username, file_id):
    conn = connection.test_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"""
            INSERT INTO LIKES
            (File_id, Liker_Username, Date_Time)
            VALUES
            ({file_id}, '{liker_username}', CURRENT_TIMESTAMP);
            """)
        conn.commit()
        return True
    except Exception as e:
            # print(e)
            log_function("error", e)
            cursor.execute("ROLLBACK")
            # log_function(F"USER:{uploader} FILE INSEERT FAILED")      
            cursor.close()
            conn.close() 
            return False
            
             
def LIKES_REMOVE(liker_username, file_id):
    conn = connection.test_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"""
            DELETE FROM LIKES
            WHERE Liker_Username = '{liker_username}' AND File_id = {file_id}
            """)
        conn.commit()
    except Exception as e:
            # print(e)
            log_function("error", e)
            cursor.execute("ROLLBACK")
            # log_function(F"USER:{uploader} FILE INSEERT FAILED")      
            cursor.close()
            conn.close() 


def LIKE_LOGIC(liker_username, file_id):
    if LIKES_INSERT(liker_username, file_id): # RETURNS TRUE IF SMOOTH
        print("SUCCESSFUL LIKE INSERT")
        
    else:
        print("FAILED LIKE INSERT")
        LIKES_REMOVE(liker_username, file_id)

def DILIKES_CREATE_TABLE():
    conn = connection.test_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"DROP TABLE IF EXISTS DISLIKES;")
        cursor.execute(
                f"""
                CREATE TABLE DISLIKES(
                    Dislike_Id SERIAL PRIMARY KEY,
                    File_id INT,
                    Disliker_Username varchar(50),
                    Date_Time timestamp, 

                    ---CONSTRAINTS
                    FOREIGN KEY (File_id) REFERENCES FILES(File_id),
                    UNIQUE (File_id, Disliker_Username) --this should allow someone to only have one like per post
                );
                """)
        conn.commit()

        print_green("DISLIKES CREATE COMPLETED\n")
    except Exception as e:
        
        cursor.execute("ROLLBACK")
        print_error("\nHAD TO ROLLBACK DISLIKES TABLE CREATION" + str(e) )
        # exit()

    cursor.close()
    conn.close()

def DISLIKES_INSERT(disliker_username, file_id):
    conn = connection.test_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"""
            INSERT INTO DISLIKES
            (File_id, Disliker_Username, Date_Time)
            VALUES
            ({file_id}, '{disliker_username}', CURRENT_TIMESTAMP);
            """)
        conn.commit()
        return True
    except Exception as e:
            # print(e)
            log_function("error", e)
            cursor.execute("ROLLBACK")
            # log_function(F"USER:{uploader} FILE INSEERT FAILED")      
            cursor.close()
            conn.close() 
            return False

def DISLIKES_REMOVE(disliker_username, file_id):
    conn = connection.test_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"""
            DELETE FROM DISLIKES
            WHERE Disliker_username = '{disliker_username}' AND File_id = {file_id}
            """)
        conn.commit()
    except Exception as e:
            # print(e)
            log_function("error", e)
            cursor.execute("ROLLBACK")
            # log_function(F"USER:{uploader} FILE INSEERT FAILED")      
            cursor.close()
            conn.close() 

def DISLIKE_LOGIC(disliker_username, file_id):
    if DISLIKES_INSERT(disliker_username, file_id): # RETURNS TRUE IF SMOOTH
        print("SUCCESSFUL DISLIKE INSERT")
        
    else:
        print("FAILED DISLIKE INSERT")
        DISLIKES_REMOVE(disliker_username, file_id)

def GET_COUNT_LIKES_BY_ID(file_id):
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM LIKES
        WHERE File_Id = {file_id}
        """) 

    likes = cursor.fetchall()[0][0]
    print("NUM LIKES:",likes)
    return likes


def LIKES_DEMO_INSERT(size="small"):
    LIKES_INSERT("foreandr", 1)
    LIKES_INSERT("foreandr", 2)
    LIKES_INSERT("foreandr", 3)
    LIKES_INSERT("foreandr", 4)
    #LIKES_INSERT("foreandr", 1) # TEST SHOULD FAIL

def DISLIKES_DEMO_INSERT(size="small"):
    DISLIKES_INSERT("foreandr", 1)
    DISLIKES_INSERT("foreandr", 2)
    DISLIKES_INSERT("foreandr", 3)
    DISLIKES_INSERT("foreandr", 4)
    #DISLIKES_INSERT("foreandr", 1) # TEST SHOULD FAIL


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
        votes_left = 10 - num
        return votes_left
        
        # PREVIOUS CODE
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
        # print(F"{username} has {num_votes} votes left of type:{vote_type}")
        if num_votes == 0:
            print_error(F"[{username}] HAS ALREADY VOTED FOR TIMEFRAME [{vote_type}]. [{num_votes} VOTES]") 
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

    
def FILE_VOTE_INSERT_DEMO(size="small"):
    #FILE_VOTE_INSERT( 'foreandr', 1,  'Daily')
    FILE_VOTE_INSERT( 'foreandr', 1,  'Monthly')
    FILE_VOTE_INSERT( 'foreandr', 1,  'Monthly')
    FILE_VOTE_INSERT( 'foreandr', 2,  'Yearly')

    big_reset_file.GIANT_FILE_VOTE_INSERT(size)

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
        log_function("error", e)
    
        
        
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
        log_function("error", e)
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


def MANSURA_SUBSCRIBE_INSERT_MULTIPLE_DEMO(size="small"):
    conn = connection.test_connection()

    #TODO:THINK ABOUT DATA VALIDATNG THE USERNAME, PRBABLY WONT NEED
    # MANSURA_SUBSCRIBE( 'foreandr')
    MANSURA_SUBSCRIBE( 'andrfore')
    # MANSURA_SUBSCRIBE( 'bigfrog')
    MANSURA_SUBSCRIBE( 'cheatsie')
    
    big_reset_file.GIANT_SUBSCRIBE(size)



    print_green("SUBSCRIBED USERS\n")


def REMOVE_ALL_USER_DIRECTORIES():
    dirpath = 'static/#UserData/'
    # print(os.getcwd())
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
        try:
            shutil.rmtree(filepath)
        except OSError as e:
            # os.remove(filepath)
            log_function("error", e)
            # print(OSError)


def USER_FULL_RESET(size="small"):
    print_title("\nEXECUTING FULL RESET\n")
    
    # SET TIMEZONE
    # SET_TIME_ZONE(conn)
    
    # DROPPING ALL TABLES
    DROP_ALL_TABLES()
    REMOVE_ALL_USER_DIRECTORIES()

    # CREATE TABLES
    
    USER_CREATE_TABLE()
    CREATE_PAYOUTS_TABLE()
    FILE_CREATE_TABLE()  
    LIKES_CREATE_TABLE()
    DILIKES_CREATE_TABLE()
    CREATE_TABLE_KEYWORDS()
    CREATE_TABLE_FILE_KEYWORDS()
    FILE_VOTE_CREATE_TABLE() 
    CONNECTION_CREATE_TABLE()
    CREATE_MANSURA_TABLE() # SUBSCRIPTIONS
    SEARCH_ALGO_CREATE_TABLE()
    CREATE_TABLE_SEARCH_VOTES()
    CREATE_TABLE_SEARCH_FAVOURITES()
    CREATE_TABLE_POST_FAVOURITES()
    EQUITY_CREATE_TABLE()
    CREATE_TABLE_1_TIME_PASSWORDS()
    CREATE_TABLE_TRIBUNAL()

    FUNCTION_AND_PROCEDURES()

    USER_INSERT_MULTIPLE(size)
    CONNECTION_INSERT_MULTIPLE(size)
    MANSURA_SUBSCRIBE_INSERT_MULTIPLE_DEMO(size)
    USER_INSERT_MULTPLE_FILES(size)
    FILE_VOTE_INSERT_DEMO(size) # VOTES ON CSVS
    SEARCH_ALGO_INSERT_DEMO_MULTIPLE(size)
    LIKES_DEMO_INSERT(size)
    DISLIKES_DEMO_INSERT(size)
    DEMO_SEARCH_VOTE_INSERT(size)
    DEFAULT_EQUITY_INSERT(size)
    DEMO_FILE_INSERT_TIKTOKS(1)
    # EQUITY CAN GO LAST, DOESN'T INTERFERE WITH ANYTHING
    
    # TRANSFER_EQUITY(buyer="a", seller="foreandr", amount=2)

    # MODEL_MULTIPLE_INSERT(conn) # MODELS
    # MODEL_VOTE_INSERT_DEMO(conn) # VOTES ON MODELS \
    #TODO:EQUITY INSIRT
    
    print_title("USER FULL RESET COMPLETED")


def GET_ALL_KEY_words():
    conn = connection.test_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        f"""
        SELECT * FROM KEYWORDS
        """)
    #print("KEYWORDS:")
    for i in cursor.fetchall():
        print(i)


def ADD_POST_KEYWORDS_TO_DATABASE(list_of_keywords, file_id):
    conn = connection.test_connection()
    cursor = conn.cursor()
    # GET_ALL_KEY_words()

    new_list_of_keywords = STRIP_KEYWORDS_OF_SPECIAL_CHARS(list_of_keywords)

    for i in new_list_of_keywords:  
        cursor.execute(f"""
            INSERT INTO KEYWORDS(key_name) 
            VALUES (LOWER('{i}'))
            ON CONFLICT DO NOTHING
            """
            )
        conn.commit()

        cursor.execute(f"""
            INSERT INTO FILE_KEYWORDS(key_name, File_Id) 
            VALUES (LOWER('{i}'), {file_id})
            ON CONFLICT DO NOTHING
            """
            )
        conn.commit()

    #GET_ALL_KEY_words()
    #GET_ALL_FILE_KEY_words()


def STRIP_KEYWORDS_OF_SPECIAL_CHARS(list_of_keywords):
    # print("KEYWORDS",list_of_keywords)
    badwords_path = "/root/mansura/Python/bad_words_username.txt"
    f = open(badwords_path, 'r')
    bad_words = f.read().split(",")
    f.close()
    
    final_list = []
    for i in list_of_keywords:
        my_string = i #THIS WILL NEED TO BE INDEX IF USING THE NLP FROM BEFORE (i[0])
        # print(my_string)
        stringless = my_string.replace(" ", "") # stringless means spaceless lol sorry tired
        lower_bad_words = [x.lower() for x in bad_words]
        if (stringless.lower() in lower_bad_words):
            continue
        elif(bool(re.search('^[a-zA-Z0-9]*$',stringless))==False): # checking special chars
            continue
        else:
            final_list.append(my_string)
    
    #print("FINAL LIST OF KEYWORDS", final_list)
    return final_list


def GET_ALL_FILE_KEY_words():
    conn = connection.test_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        f"""
        SELECT * 
        FROM FILE_KEYWORDS
        """)
    print("FILE KEYWORDS:")
    for i in cursor.fetchall():
        print(i)


def CREATE_TABLE_KEYWORDS():
    conn = connection.test_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""DROP TABLE IF EXISTS KEYWORDS CASCADE""")
        cursor.execute(
            f"""
                CREATE TABLE KEYWORDS
                (
                Keyword_id SERIAL PRIMARY KEY,   
                key_name varchar UNIQUE
                );
            """)
        conn.commit()
        print_green("KEYWORDS CREATE COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        print_error("\nHAD TO ROLLBACK USER CREATION" + str(e) )
    
    cursor.close()
    conn.close()


def CREATE_TABLE_FILE_KEYWORDS():
    conn = connection.test_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""DROP TABLE IF EXISTS FILE_KEYWORDS CASCADE""")
        cursor.execute(
            f"""
                CREATE TABLE FILE_KEYWORDS
                (
                Key_Usage_Id SERIAL PRIMARY KEY,   
                key_name Varchar, 
                File_Id BIGINT,
                FOREIGN KEY (key_name) REFERENCES KEYWORDS(key_name),
                FOREIGN KEY (File_id) REFERENCES FILES(File_id)
                );
            """)
        conn.commit()
        print_green("FILE_KEYWORDS CREATE COMPLETED\n")
    except Exception as e:
        cursor.execute("ROLLBACK")
        print_error("\nHAD TO ROLLBACK USER CREATION" + str(e) )


def DROP_ALL_TABLES():
    conn = connection.test_connection()
    print_title("\nDROPPING TABELS..")
    cursor = conn.cursor()
    try:
        try:
            cursor.execute(f"DROP TABLE IF EXISTS POST_FAVOURITES CASCADE;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS POST_FAVOURITES;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            log_function("error", e)
        
        try:
            cursor.execute(f"DROP TABLE IF EXISTS SEARCH_FAVOURITES CASCADE;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS SEARCH_FAVOURITES;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            log_function("error", e)

        try:
            cursor.execute(f"DROP TABLE IF EXISTS SEARCH_VOTES CASCADE;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS SEARCH_VOTES ;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            log_function("error", e)

        try:
            cursor.execute(f"DROP TABLE IF EXISTS DISLIKES CASCADE;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS DISLIKES;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            log_function("error", e)

        try:
            cursor.execute(f"DROP TABLE IF EXISTS LIKES CASCADE;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS LIKES;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            log_function("error", e)
        
        try:
            cursor.execute(f"DROP TABLE IF EXISTS SEARCH_ALGORITHMS CASCADE;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS SEARCH_ALGORITHMS;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            log_function("error", e)

        try:
            cursor.execute(f"DROP TABLE IF EXISTS EQUITY CASCADE;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS EQUITY;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print_error("[EQUITY] " + str(e))

        try:
            cursor.execute(f"DROP TABLE IF EXISTS SUBSCRIPTIONS_MENSURA CASCADE;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS SUBSCRIPTIONS_MENSURA;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print_error("[SUBSCRIPTIONS_MENSURA] " + str(e))
               
        try:
            cursor.execute(f"DROP TABLE IF EXISTS MODEL_VOTES CASCADE;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS MODEL_VOTES;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print_error("[MODEL VOTES] " + str(e))
            
        try:
            cursor.execute(f"DROP TABLE IF EXISTS MODEL CASCADE;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS MODEL;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print_error("[MODEL] " + str(e))
                 
        try:
            cursor.execute(f"DROP TABLE IF EXISTS FILE_VOTES CASCADE;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS FILE_VOTES;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print_error("[FILE_VOTES] " + str(e) )

        try:
            cursor.execute(f"DROP TABLE IF EXISTS FILES CASCADE;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS FILES;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print_error("[FILES] " + str(e))

        try:
            cursor.execute(f"DROP TABLE IF EXISTS CONNECTIONS CASCADE;")
            conn.commit()
            print_green("DROPPED TABLE IF EXISTS CONNECTIONS;")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print_error("[CONNECTIONS]" + str(e))

        try:        
            cursor.execute(f"DROP TABLE IF EXISTS USERS CASCADE;")
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
                external_link="",
                distro_details=""):
    """
    REALLY COMPLICATED NIGHTMARE BUT IT WORKS
    
    """
    #1. CHECK THAT THE POST FOREIGN ID ACTUALLY EXISTS
    if post_foreign_id_source == "None" or post_foreign_id_source == "" or post_foreign_id_source == None:
        # print(F"EMPTY SOURCE IS [{post_foreign_id_source}]")
        post_foreign_id_source = ""
        # print(F"EMPTY SOURCE IS [{post_foreign_id_source}]")
            
    conn = connection.test_connection()
    cursor = conn.cursor()

    #CHECK EMPTY   
    if post_file == "":
        filename = ""
    else: 
        filename = post_file.filename

    # BEGINNING EXOCUTION
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
                print("ENTERING POSTIFLE:", post_file)
                target = rf'/root/mansura/static/#UserData/{uploader}/files/{new_path}/pic.jpg'#TODO: DIFFERENTIATE DIFFERENT EXTENSIONS
                post_file.stream.seek(0)
                post_file.save(target)
                
                # print("ENTERED INTO TARGET", target)
            except Exception as e:
                log_function(str(e) + "FILE ERROR ENTRY OF SOME KIND!!!!!")    

        # 5. INSERT INTO FILE SYSTEM           
        FILE_INSERT_STORAGE(
            username = uploader, 
            path_name=new_path, 
            text=post_text, 
            age_18=age_18,
            external_source=external_link,
            distro_details=distro_details

        )

        # INSERT INTO POSTKEYS
        # 6. 
        ADD_POST_KEYWORDS_TO_DATABASE(NLP_KEYWORD_EXTRACTOR(post_text), CURRENT_FILE_ID)
        # exit() 
        print_green(f"FILE INSERT COMPLETED {uploader}, {new_path}")
            
        # CLOSE CURSOR AND CONNECTION [MANDATORY]        
        cursor.close()
        conn.close()
        return CURRENT_FILE_ID

         # return new_path #TODO: not sure if this needs to return anything
    except Exception as e:
            print(e)
            log_function("error", e)
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
    jsonString = json.dumps(config_json, indent=4)
    jsonFile = open(f"static/#UserData/{username}/config.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

    search_counter_json = {
        "":""
    }
    search_jsonString = json.dumps(search_counter_json, indent=4)    
    search_jsonFile = open(f"static/#UserData/{username}/search_counter.json", "w")
    search_jsonFile.write(search_jsonString)
    search_jsonFile.close()


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
    try:
        USER_INSERT(username, password, email, paypal_email, balance)
        register_user_files(username)
        return True
    except Exception as e:
        log_function(e)
        return False
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
            log_function("error", e)


def CHANGE_PASSWORD(email, password):
    '''old unused code:

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
        log_function("error", e) 
    '''
    
    conn = connection.test_connection()
    cursor = conn.cursor()
    new_password = hashlib.sha256(f"{password}".encode('utf-8')).hexdigest()
    cursor.execute(f"""
        UPDATE USERS SET password = '{new_password}'
        WHERE email = '{email}';
    """)
    conn.commit()
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()
    print(f"CHANGED PASSWORD")
    print(f"OG {password}")
    print(f"HASHED {new_password}")


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
    
    # print('GET FOLLOWERS: ', username)
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
        log_function("error", e)  
        
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
        log_function("error", e)
    
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
        
        # print("created")
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
        log_function("error", e)
    
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
        log_function("error", e)
    
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
        log_function("error", e)
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
    try:
        conn = connection.test_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
                INSERT INTO EQUITY(username, percentage)
                VALUES ('foreandr', 100)
        """)
        conn.commit()
    except Exception as e:
        log_function(e)


def EQUITY_CREATE_TABLE():
    conn = connection.test_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DROP TABLE IF EXISTS EQUITY;")
        cursor.execute(f"""
        CREATE TABLE EQUITY 
        (
            username varchar(200) UNIQUE,
            percentage Decimal,
            FOREIGN KEY (username) REFERENCES USERS(username)
        );
        """)
        conn.commit()
        print_green("EQUITY_CREATE_TABLE SUCCESSFUL")
    except Exception as e:
        log_function(e)
    
    CLOSE_CURSOR_AND_CONN(cursor, conn)


def DEFAULT_EQUITY_INSERT(size='small'):
    conn = connection.test_connection()
    cursor = conn.cursor()
    try:

        cursor.execute(
            f"""
            INSERT INTO EQUITY (username, percentage)
            VALUES('foreandr', 100)
        """)
        conn.commit()

    except Exception as e:
        log_function(e)
    
    CLOSE_CURSOR_AND_CONN(cursor, conn)




def FILE_INSERT_STORAGE(username, path_name, text, age_18, external_source, distro_details):
    # print(f"username: {username}\npath_name: {path_name}\ntext: {text}\nmy_file: {my_file}\nage_18: {age_18}\nexternal_source: {external_source}")
    print("GETTING TO FILE STORAGE")
    external_source = CREATING_EMBED_STRUCTURE(external_source)
    
    my_dictionary = {
        "txt": f"{text}",
        "18+": f"{age_18}",
        "external_source": f"{external_source}",
        "distro_details": distro_details
    }
    # log_function("error", str(my_dictionary))
    # print(f"DICTIONARY:\n{type(my_dictionary)}\n{my_dictionary}")
    json_object = json.dumps(my_dictionary, indent=4)
    # Writing to sample.json
    with open(f"static/#UserData/{username}/files/{path_name}/post_config.json", "w") as outfile:
        outfile.write(json_object)
    '''
    try:
        target = rf'static/#UserData/{username}/files/{path_name}/post_text.txt' # WRITING TEXT PART   
        with open(target, 'w') as f:
            f.write(text)
    except Exception as e:
        log_function("error", e)
    
        
    try:
        target = rf'static/#UserData/{username}/files/{path_name}/age_18.txt' # WRITING TEXT PART   
        with open(target, 'w') as f:
            f.write(age_18)
    except Exception as e:
        log_function("error", e)
        
        
    try:
        target = rf'static/#UserData/{username}/files/{path_name}/external_source.txt' # WRITING TEXT PART   
        with open(target, 'w') as f:
            f.write(external_source)
    except Exception as e:
        log_function("error", e)
    '''

def CHECK_FILES_NOT_OVER_LIMIT(page_no):
    conn = connection.test_connection()
    print("CHECK_FILES_NOT_OVER_LIMIT", page_no)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT * 
        FROM FILES 
        OFFSET (({page_no} - 1) * 30)

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
        SELECT F.Uploader, F.File_PATH, F.UserId, F.Post_foreign_id_source, F.Date_Time, F.File_id,
        (   
            SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
            FROM FILE_VOTES file 
            WHERE file.File_id = F.File_id 
            AND Vote_Type = 'Daily'
        ), 
        (   
            SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
            FROM FILE_VOTES file 
            WHERE file.File_id = F.File_id 
            AND Vote_Type = 'Monthly'
        ),
        (  
            SELECT COUNT(*) -- TOTAL VOTES FOR DATASET
            FROM FILE_VOTES file 
            WHERE file.File_id = F.File_id 
            AND Vote_Type = 'Yearly'
        ),
        (
            SELECT COUNT(*)
            FROM LIKES likes
            WHERE likes.File_id = F.File_id 
        ),
        (
            SELECT COUNT(*)
            FROM DISLIKES dislikes
            WHERE dislikes.File_id = F.File_id 
        )


        FROM FILES F
        WHERE F.File_PATH = '{filename}'
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
                                                                                                     # daily        # month        # year        #likes         #dislikes
    return info_array[0], info_array[1], info_array[2], info_array[3], info_array[4], info_array[5], info_array[6], info_array[7], info_array[8],info_array[9], info_array[10],


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
        log_function("error", e)

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
    if File_id_ == "None" or File_id_ == "":
        return False
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

def CUSTOM_GET_HIGHEST_VALUE_IN_DICT_SLOW(my_dict):
    '''
    I ONLY WROTE THIS BECAUSE PYTHONS MAX FUNCTION HAS ALL KINDS OF ABSOLUTELY INSANE RULES

    SHOULD BE MUCH SLOWER TTHAN ITS NEEDS TO BE, COULD BE RE-WRITTEN IN LOWER LVL LANGUGAE
    '''
    
    # my_dict = {"": "", "a-1": 5, "andrfore-3": 3, "foreandr-2": 3}
    
    highest_key = None
    highest_num = 0
    for key, value in my_dict.items():
        
        if type(value) == int:
            # print(key, value, type(value))
            if value >= highest_num: # this should ensure the last search wins
                highest_num = value 
                highest_key = key
    
    # print(highest_key)
    return  highest_key

def TURN_CLAUSES_INTO_JSON(search, date_check, order_check, clauses_dict, searcher):
    #print("\nINSIDE TURNING INTO JSON\n")
    #print("ITEM SEARCH       :", search) # DONE
    #print("date_check        :", date_check) # DONE
    #print("order_check       :", order_check) # DONE
    # print("clauses_dict      :", clauses_dict)

    # QUERY STRING CHECK
    LIKE_QUERY = ""
    personal_where_clause = ""
    personal_order_by_clause=""
    if len(search) > 0:
        # print("search is a string with len", search)
        tag_query = f"""OR (0 < (SELECT COUNT(*) FROM FILE_KEYWORDS fkey WHERE fkey.File_Id = F.File_Id AND key_name = LOWER('{search}')))"""
        # print("tag_query:", tag_query)
        LIKE_QUERY = F"AND (LOWER(U.username) LIKE LOWER('%{search}%') {tag_query})"
        # print(LIKE_QUERY)
        # exit()

    # DATE CHECK 
    if date_check == "ALL":
        date_clause = ""
    elif date_check == "YEAR":
        date_clause = "AND F.Date_Time >= date_trunc('year', now())::date"
    elif date_check == "MONTH":
        date_clause = "AND F.Date_Time >= date_trunc('month', now())::date"
    elif date_check == "DAY":
        date_clause = "AND F.Date_Time >= date_trunc('day', now())::date"

    # ORDER CHECK
    if order_check == "TOP":
        order_clause = "ORDER BY (SELECT COUNT(*) FROM FILE_VOTES file WHERE file.File_id = F.File_id AND Vote_Type = 'Monthly') + (SELECT COUNT(*) FROM FILE_VOTES file WHERE file.File_id = F.File_id AND Vote_Type = 'Daily') + (SELECT COUNT(*) FROM FILE_VOTES file WHERE file.File_id = F.File_id AND Vote_Type = 'Yearly') DESC"
    elif order_check == "HOT":
        order_clause = "AND F.Date_Time >= date_trunc('month', now())::date" #TODO: CHANGE TO REFLECT ORDER BY FUNCTION
    elif order_check == "NEW":
        order_clause = "AND F.Date_Time >= date_trunc('day', now())::date" #TODO: CHANGE TO REFLECT ORDER BY FUNCTION
    else:
        #print("ORDER CHECK IS CUSTOM OR FAVOURITE", order_check)
        if order_check == "ONE OF THE DEFAULT ALGORITHM NAMES, THEN SEND THERE":#TODO: OBVIOUSLY THIS NEEDS TO CHANGE TO THE REAL ALGO NAMES
            pass
        else:
            # GO TO THAT USER, AND GRAB THAT ALGORITHM
            #print(order_check)

            #GET UPLOADER AND FILE_ID FROM ALGO NAME
            uploader, file_id, search_path = GET_UPLOADER_AND_FILE_ID_FROM_ALGO_NAME(order_check)
            username = uploader
            order_check = str(uploader) + "-" + str(file_id)
            # print("ALGO BY PERSON DETAILS:", uploader, file_id, order_check)
            f = open(f'/root/mansura/static/#UserData/{username}/search_algorithms/{search_path}.json')
            data_ = json.load(f)
            f.close()

            # COUNTING SEARCHES
            if searcher != "": # SEARCHER IS RELATED TO SESSION, VOTES ONLINE COUNT IF SIGNED IN
                # COULD ADD AN ADDITIONAL CRITERIA ABOUT SUBSCRIPTION
                if CHECK_DATE(searcher):
                    # JSON IN
                    with open(f'/root/mansura/static/#UserData/{searcher}/search_counter.json', 'r') as f:
                        data = json.load(f)
                        # print("data:\n",data)
                        data = dict(data)
                        # print("coming back from file:",data)

                        current_max= CUSTOM_GET_HIGHEST_VALUE_IN_DICT_SLOW(data)
                        #print("PRE DICT:",data )
                        if order_check in data:
                            # print("in")
                            data[order_check] += int(1)
                        else:
                            # print("not in")
                            data[order_check] = int(1)

                        #UPDATE MAJORITY SEARCH FOR THAT USER if new high
                        #print("POS DECT:",data )
                        new_max_algo_path = CUSTOM_GET_HIGHEST_VALUE_IN_DICT_SLOW(data)

                        #print("current_max:", current_max)
                        #print("new_max    :", new_max)
                        # print("SEARCH VOTE CHECKER?")
                        if new_max_algo_path != current_max:
                            print("searcher",searcher)
                            print("new_max_algo_path", new_max_algo_path)
                            UPDATE_TABLE_SEARCH_VOTES(voter_username=searcher, search_algo_path=new_max_algo_path)
                                          
                    # JSON OUT
                    with open(f'/root/mansura/static/#UserData/{searcher}/search_counter.json', 'w') as f:    
                        json_object = json.dumps(data) 
                        # print("NEW DICT", data)
                        # print("json_object", json_object)
                        f.write(json_object)
                else:
                    print(f"{searcher} NOT SUBSCRIBED")        
            order_clause = data_["ORDER_BY_CLAUSE"]
            personal_where_clause = data_["WHERE_CLAUSE"]





    #print("======================")
    #print(LIKE_QUERY)
    #print(date_clause)
    #print(order_clause)
    #print("======================")

    first = []
    second = []
    third = []
    fourth = []
    fifth = []
    sixth = []
    seventh = []
    eigth = []
    ninth = []
    tenth = []

    for i in clauses_dict:
        # print(i)
        # print(len(i), i)
        if len(i) > 0:
            first.append(i[0])
        if len(i) > 1:
            second.append(i[1])
        if len(i) > 2:
            third.append(i[2])
        if len(i) > 3:
            fourth.append(i[3])
        if len(i) > 4:
            fifth.append(i[4])
        if len(i) > 5:
            sixth.append(i[5])
        if len(i) > 6:
            seventh.append(i[6])
        if len(i) > 7:
            eigth.append(i[7])
        if len(i) > 8:
            first.append(i[8])
        if len(i) > 9:
            ninth.append(i[9])
        if len(i) > 10:
            tenths.append(i[10])

        
    #print("1:",first)
    #print("2:",second)
    #print("3:",third)
    #print("4:",fourth)
    #print("5:",fifth)
    #print("6:",sixth)
    #print("7:",seventh)
    #print("8:",eigth)
    #print("9:",ninth)
    #print("10:",tenth)
    #print("======================")
    clauses_reasembled = []

    clauses_reasembled.append(first)
    clauses_reasembled.append(second)
    clauses_reasembled.append(third)
    clauses_reasembled.append(fourth)
    clauses_reasembled.append(fifth)
    clauses_reasembled.append(sixth)
    clauses_reasembled.append(seventh)
    clauses_reasembled.append(eigth)
    clauses_reasembled.append(ninth)
    clauses_reasembled.append(tenth)
    
    #print("REASSEMBELLED")
    #for i in clauses_reasembled:
    #    print(i)
    #print("======================")
    
    list_of_assembled_queries = []
    
    for i in clauses_reasembled:
        temp_full_clause = TURN_WHERE_CLAUSE_TO_STRING(i)
        list_of_assembled_queries.append(temp_full_clause)

    #for i in list_of_assembled_queries:
    #    print(i)
    #print("======================")
    
    WHERE_CLAUSE = ""
    for i in list_of_assembled_queries:
        #print(i)
        WHERE_CLAUSE += i

    #print("WHERE CLAUSE:\n", WHERE_CLAUSE)
    WHERE_CLAUSE += LIKE_QUERY + " " + date_clause + " " + personal_where_clause
    #print("%LIKE%-WHERE CLAUSE:", WHERE_CLAUSE)
    #print("======================") 
    demo_json = {
        "ORDER_BY_CLAUSE": order_clause,
        "WHERE_CLAUSE": WHERE_CLAUSE
    }
    return demo_json

def UPDATE_TABLE_SEARCH_VOTES(voter_username, search_algo_path):
    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT COUNT(*)
    FROM SEARCH_VOTES
    WHERE Voter_Username = '{voter_username}'
    """)

    vote_exists = cursor.fetchall()[0][0]
    print("VOTE EXISTS", vote_exists)
    
    search_id = GET_SEARCH_ALGO_ID_BY_PATH(search_algo_path)
    
    print("search_id", search_id)
    print("search_algo_pathe", search_algo_path)
    if vote_exists == 0:
        print("INSERTING SEARCH VOTE")
        cursor.execute(f"""
            INSERT INTO SEARCH_VOTES(Search_id, Voter_Username)
            VALUES ({search_id}, '{voter_username}');
        """)
        conn.commit()
    else:
        print("UPDATING SEARCH VOTE")
        cursor.execute(f"""
            UPDATE SEARCH_VOTES
            SET Search_id = {search_id}
            WHERE Voter_Username = '{voter_username}'
        """)
        conn.commit()
    
    cursor.close()
    conn.close()

def GET_SEARCH_ALGO_ID_BY_PATH(algo_path):

    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT Search_id
        FROM SEARCH_ALGORITHMS
        WHERE Search_Path = '{algo_path}'
    """)

    search_id = ""
    for i in cursor.fetchall():
        search_id = i[0] 
    print("ENTERED ALGO NAME  :",algo_path, len(algo_path))
    print("RETURNED SEARCH ID:",search_id )
    return search_id



def GET_UPLOADER_AND_FILE_ID_FROM_ALGO_NAME(order_check):
    # print("GET_UPLOADER_AND_FILE_ID_FROM_ALGO_NAME")
    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT Username, Search_id, Search_Path
        FROM SEARCH_ALGORITHMS
        WHERE Algorithm_Name = '{order_check}'
    """)
    name = ""
    search_id = ""
    search_path = ""
    for i in cursor.fetchall():
        # print(i)
        name = i[0] 
        search_id = i[1]
        search_path = i[2]
    return name, search_id, search_path


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
        Search_TOTAL BIGINT,
        Date_Time timestamp,      
        FOREIGN KEY (Username) REFERENCES USERS(Username)
        );
        """)
    conn.commit()
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()


def CREATE_TABLE_POST_FAVOURITES():
    conn = connection.test_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DROP TABLE IF EXISTS POST_FAVOURITES;")
        cursor.execute(
                f"""
                CREATE TABLE POST_FAVOURITES(
                    Favourite_Id SERIAL PRIMARY KEY,
                    File_id INT,
                    Favouriter_Username varchar(50),
                    Date_Time timestamp, 

                    ---CONSTRAINTS
                    FOREIGN KEY (File_id) REFERENCES FILES(File_id),
                    UNIQUE (File_id, Favouriter_Username) --this should allow someone to only have one favourite per post
                );
                """)
        conn.commit()

        print_green("POST_FAVOURITES CREATE COMPLETED\n")
    except Exception as e:
        
        cursor.execute("ROLLBACK")
        print_error("\nHAD TO ROLLBACK POST_FAVOURITES TABLE CREATION" + str(e) )
        # exit()

    cursor.close()
    conn.close()

def GET_SEARCH_DETAILS_BY_ALGO_NAME(algo_name):
    print(algo_name)
    #GET UPLOADER AND FILE_ID FROM ALGO NAME
    uploader, file_id, search_path = GET_UPLOADER_AND_FILE_ID_FROM_ALGO_NAME(algo_name)
    username = uploader
    order_check = str(uploader) + "-" + str(file_id)
    # print("ALGO BY PERSON DETAILS:", uploader, file_id, order_check)
    f = open(f'/root/mansura/static/#UserData/{username}/search_algorithms/{search_path}.json')
    data_ = json.load(f)
    # print(data_)
    f.close()
    return data_


def GET_SEARCH_FAVOURITES_BY_USERNAME(username):
    conn = connection.test_connection()
    cursor = conn.cursor()
    query = f"""
        SELECT algos.Username,     
            (   
                SELECT COUNT(*) 
                FROM SEARCH_VOTES votes
                WHERE votes.Search_id = algos.Search_id
            ) as VOTE_COUNT,
            algos.Algorithm_Name, algos.Date_Time
        
        FROM SEARCH_ALGORITHMS algos

        INNER JOIN SEARCH_FAVOURITES favourites
        ON favourites.Search_id = algos.Search_id

        WHERE favourites.Favouriter_Username = '{username}'
        """
    cursor.execute(query)
    favourited_algos = []
    for i in cursor.fetchall():
        favourited_algos.append(i)
        # print(i)
    return favourited_algos

def CREATE_TABLE_SEARCH_FAVOURITES():
    conn = connection.test_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"DROP TABLE IF EXISTS SEARCH_FAVOURITES;")
        cursor.execute(
                f"""
                CREATE TABLE SEARCH_FAVOURITES(
                    Search_Favourite_Id SERIAL PRIMARY KEY,
                    Search_id INT,
                    Favouriter_Username varchar(50),
                    Date_Time timestamp, 

                    ---CONSTRAINTS
                    FOREIGN KEY (Search_id) REFERENCES SEARCH_ALGORITHMS(Search_id),
                    UNIQUE (Search_id, Favouriter_Username) --this should allow someone to only have one favourite per post
                );
                """)
        conn.commit()

        print_green("POST_FAVOURITES CREATE COMPLETED")    

    except Exception as e:       
        cursor.execute("ROLLBACK")
        print_error("HAD TO ROLLBACK  CREATE_TABLE_SEARCH_FAVOURITES TABLE CREATION" + str(e))   
        log_function(e)      

    cursor.close()
    conn.close()

def GET_SEARCH_ALGO_ID_BY_NAME(algo_name):
    #print("GET_SEARCH_ALGO_ID_BY_name")

    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT Search_id
        FROM SEARCH_ALGORITHMS
        WHERE Algorithm_Name = '{algo_name}'
    """)

    search_id = ""
    for i in cursor.fetchall():
        search_id = i[0] 
    #print("ENTERED ALGO NAME  :",algo_name, len(algo_name))
    #print("RETURNED SEARCH ID:",search_id )
    return search_id


def INSERT_INTO_SEARCH_FAVOURITES(user, search_id):
    # print("SEARCH FAVE INSERT:", user, search_id)
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO SEARCH_FAVOURITES(Search_id, Favouriter_Username)
        VALUES ({search_id}, '{user}')
        ON CONFLICT DO NOTHING
    """)
    conn.commit()
    conn.close()
    cursor.close()

def DEL_SEARCH_FAVOURITE(user, search_id):
    conn = connection.test_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            DELETE FROM SEARCH_FAVOURITES
            WHERE Search_id = {search_id} AND Favouriter_Username = '{user}';
        """)
        conn.commit()
    except Exception as e:
        # print("PROBABLY JUST DOESNT EXIST")
        pass
    conn.close()
    cursor.close()

def CREATE_TABLE_SEARCH_VOTES():
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS SEARCH_VOTES""")
    cursor.execute(
        f"""
            CREATE TABLE SEARCH_VOTES(
            Search_Vote_Id SERIAL PRIMARY KEY,
            Search_id INT,
            Voter_Username varchar,
            FOREIGN KEY (Search_id) REFERENCES SEARCH_ALGORITHMS(Search_id)
        )
        """)
    conn.commit()
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()

def DEMO_SEARCH_VOTE_INSERT(size="small"):
    UPDATE_TABLE_SEARCH_VOTES("foreandr", "a-1")
    UPDATE_TABLE_SEARCH_VOTES("Maire", "foreandr-2")
    UPDATE_TABLE_SEARCH_VOTES("a", "a-1")
    UPDATE_TABLE_SEARCH_VOTES("andefore", "andrfore-3")

def SEARCH_ALGO_INSERT(username, Algorithm_Name, order_by_clause, where_clause):
    
    conn = connection.test_connection()
    cursor = conn.cursor() 
    todays_saved_algos = COUNT_TODAYS_SEATRCH_ALGOS_FOR_USER(username)
    if todays_saved_algos != 0:
        print(f"{username} already saved an algo today")
        return False
    try:
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
            (Username, Search_Path, Algorithm_Name, Search_TOTAL, Date_Time)
        VALUES
            ('{username}', '{new_path}', '{Algorithm_Name}', 0, CURRENT_TIMESTAMP );
        """)        
        conn.commit()

        # 3. SAVE ORDER AND WHERE CLAUSE INTO FOLDER

        my_path = F"/root/mansura/static/#UserData/{username}/search_algorithms/{new_path}.json" 
        config_json = {
            'ORDER_BY_CLAUSE':f"{order_by_clause}",
            'WHERE_CLAUSE'   :f"{where_clause}"
        }
        jsonString = json.dumps(config_json, indent=4)
        jsonFile = open(f"{my_path}", "w")
        jsonFile.write(jsonString)
        jsonFile.close()

        # CLOSE CURSOR AND CONNECTION [MANDATORY]        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        log_function("error", e)
        return False


def SEARCH_ALGO_INSERT_DEMO_MULTIPLE(size="small"):
    # username, Algorithm_Name, order_by_clause, where_clause
    SEARCH_ALGO_INSERT(username='a', Algorithm_Name='a-demo', order_by_clause="", where_clause="")
    SEARCH_ALGO_INSERT('foreandr', 'foreandr-demo', "", "")
    SEARCH_ALGO_INSERT('foreandr', 'foreandr-demo2', "", "")
    SEARCH_ALGO_INSERT('andrfore', 'andrfore-demo', "", f"AND U.username LIKE 'foreandr%'")
    print_green("SEARCH_ALGO_INSERT_DEMO_MULTIPLE()")


def COMPOSE_ORDER_BY_CLAUSES(order_by_clause, custom_clauses_order_by):
    print("COMPOSE_ORDER_BY_CLAUSES====")
    print(order_by_clause)
    print(custom_clauses_order_by)

    demo_concat = order_by_clause + " " + custom_clauses_order_by
    #print("\ndemo_concat", demo_concat)

    demo_split_first = order_by_clause.split("ORDER BY")
    #print("\ndemo_split_first", demo_split_first)

    demo_split_second = custom_clauses_order_by.split("ORDER BY")
    #print("\ndemo_split_second", demo_split_second)

    print("===========================")
    return order_by_clause


def universal_dataset_function(search_type, page_no="1", search_user="None", file_id="None", profile_username="None", custom_clauses="None", tribunal=False):
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
    if tribunal: # -- THIS IS FOR THE TRIBUNAL -- ABSOLUTE FUCKING NIGHTMARE
        tribunal_query = """
        AND ((SELECT COUNT(*) FROM TRIBUNAL WHERE TRIBUNAL.File_Id = F.File_id) = 1 AND ((SELECT COUNT(*) FROM DISLIKES dislikes WHERE dislikes.File_id = F.File_id) / ((SELECT COUNT(*) FROM DISLIKES dislikes WHERE dislikes.File_id = F.File_id) + (SELECT COUNT(*) FROM LIKES likes WHERE likes.File_id = F.File_id))) > .75)
        """
    else:
        tribunal_query = """        
        
            AND CASE 
            WHEN (SELECT COUNT(*) FROM TRIBUNAL WHERE TRIBUNAL.File_Id = F.File_id) = 1 
                THEN                   
                    CASE 
                    WHEN (((SELECT COUNT(*) FROM DISLIKES dislikes WHERE dislikes.File_id = F.File_id) + (SELECT COUNT(*) FROM LIKES likes WHERE likes.File_id = F.File_id)) > 1 ) AND (SELECT COUNT(*) FROM DISLIKES dislikes WHERE dislikes.File_id = F.File_id) > 10 -- SWITCH TO TEN
                        THEN
                                ((SELECT COUNT(*) FROM DISLIKES dislikes WHERE dislikes.File_id = F.File_id) / ((SELECT COUNT(*) FROM DISLIKES dislikes WHERE dislikes.File_id = F.File_id) + (SELECT COUNT(*) FROM LIKES likes WHERE likes.File_id = F.File_id))) > .75                                                                                           
                        ELSE 1=1   
                    END                                                          
                ELSE 1 = 1 
            END
        
        """


    if search_type != "post":
        # payouts because small table, wasnt sure if size would effect query time
        POST_SEARCH_QUERIES = """ 
        (SELECT count(*) FROM PAYOUTS WHERE 1 = 0),
        (SELECT count(*) FROM PAYOUTS WHERE 1 = 0),
        (SELECT count(*) FROM PAYOUTS WHERE 1 = 0)
        """ # THIS IS JUST A NOTHING QUERY
        foreign_id_text_entry = F"" # a meaningless statement        
        if search_type == "prof":
            profile_search_clause = F"AND U.username = '{profile_username}'"      
        else:
            profile_search_clause = F""
    else:
        foreign_id_text_entry = F"AND F.Post_foreign_id_source = '{file_id}'"
        profile_search_clause = F""

    where_clause = custom_clauses["WHERE_CLAUSE"] 
    order_by_clause = custom_clauses["ORDER_BY_CLAUSE"]
    

    if len(order_by_clause) == 0:
        order_by_clause = "ORDER BY (SELECT COUNT(*) FROM FILE_VOTES file WHERE file.File_id = F.File_id AND Vote_Type = 'Monthly') + (SELECT COUNT(*) FROM FILE_VOTES file WHERE file.File_id = F.File_id AND Vote_Type = 'Daily') + (SELECT COUNT(*) FROM FILE_VOTES file WHERE file.File_id = F.File_id AND Vote_Type = 'Yearly') DESC"

    where_full_query = f"{foreign_id_text_entry} {profile_search_clause} {where_clause}" # THIS EXTRA PAREN SEEMS TO NEED TO BE HERE???
    #print("SEARCH CLAUSE", profile_search_clause)
    #print("ORDER  CLAUSE", order_by_clause)
    #print("WHERE  CLAUSE", where_clause)
    #print("FOREI  CLAUSE", foreign_id_text_entry)

    query = f"""
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
            {POST_SEARCH_QUERIES},
            (
                SELECT COUNT(*)
                FROM LIKES likes
                WHERE likes.File_id = F.File_id 
            ),
            (
                SELECT COUNT(*)
                FROM DISLIKES dislikes
                WHERE dislikes.File_id = F.File_id 
            ),
            (
                SELECT COUNT(*)
                FROM LIKES likes
                WHERE likes.File_id = F.File_id 
                AND '{search_user}' = likes.Liker_Username
            ),
            (
                SELECT COUNT(*)
                FROM DISLIKES dislikes
                WHERE dislikes.File_id = F.File_id 
                AND '{search_user}' = dislikes.Disliker_Username
            ),
            (
                SELECT COUNT(*)
                FROM FILES 
                WHERE Post_foreign_id_source = CAST (F.File_id AS  varchar) --bad mistake shouldnt have to cast but whatever
            ),
            (
                SELECT COUNT(*)
                FROM SUBSCRIPTIONS_MENSURA sub
                WHERE sub.username = U.username
            )

 
        FROM FILES F
        
        INNER JOIN USERS U
        on U.username = F.Uploader

        WHERE U.username = U.username -- DO THIS SO ALL OTHERC ALUSES CAN BE AND CLAUSES
        {where_full_query}
        {tribunal_query }                                                              
        {order_by_clause}
        
        OFFSET (({page_no} - 1) * 30)
        LIMIT 30; 
    """
    #print("MY QUERY ================================")
    #print(query)
    cursor.execute(query)
    # -- ORDER BY GET_FILE_VOTE_COUNT_TYPED(F.File_Id, '{sort_time_frame}') DESC
    search_arguments = {
        "search_type":search_type, 
        # "search_algo_path":search_algo_path, 
        "page_no":page_no, 
        "search_user":search_user, 
        "file_id":file_id, 
        "where_full_query":where_full_query, 
        "order_by_clause":order_by_clause
    }

    file_ids_list = []
    usernames_list = []
    paths_list = []
    dates_list = []
    post_sources_list = []
    day_votes = []
    month_votes = []
    year_votes = []
    total_votes = []
    likes = []
    dislikes = []
    searcher_has_liked = []
    searcher_has_disliked = []
    num_replies = []
    uploader_is_subbed = []


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
        likes.append(i[18])
        dislikes.append(i[19])
        searcher_has_liked.append(i[20])
        searcher_has_disliked.append(i[21])
        num_replies.append(i[22])
        uploader_is_subbed.append(i[23])
        
    # THIS SEEMED TO NOT WORK FOR PARTICULAR PROFILES #TODO: WORK INFESTIGATING WHY IT DIDN'T RUN
    if daily_left != "":
        if CHECK_DATE(search_user):
            daily_left = 10 - daily_left
            monthly_left= 10 - monthly_left
            yearly_left  = 10 - yearly_left 
        else:
            daily_left, monthly_left, yearly_left = 0, 0, 0

    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()
    ''' GETTING RID OF DUPES CAUSIGN WAY TOO MANY TROUBLWES RIGHT NOW
    #print("THESE ARE MY SERVER SIDE SEARCH ARGUMENTS")
    #print(search_arguments)
    print("TESTING!!!!", search_arguments["where_full_query"])
    where_clause_list_ = search_arguments['where_full_query'].split("AND")
    #print(where_clause_list_)
    search_arguments['where_full_query'] = list(dict.fromkeys(where_clause_list_))# getting rid of dupes
    search_arguments_with_and = ""
    for i in search_arguments['where_full_query']:
        if i != "":    
            j = "AND " + i
            search_arguments_with_and += j
    search_arguments['where_full_query'] = search_arguments_with_and

    print("SEARCH ARGS WITH DUPES", where_clause_list_)
    print("SEARCH ARGS WITH DUPES", search_arguments_with_and)

    #print(f"-----\n{search_arguments}\n-----")

    # search_arguments['where_full_query'] = list(dict.fromkeys(search_arguments['where_full_query']))
    '''
    # print("ORDER BY CLAUSE", search_arguments)
    return file_ids_list, usernames_list, paths_list, dates_list, post_sources_list, daily_left, monthly_left, yearly_left, day_votes, month_votes, year_votes, user_balance, dailypool, monthlypool, yearlypool, daily_votes_singular,  monthly_votes_singular, yearly_votes_singular, likes, dislikes,searcher_has_liked,searcher_has_disliked, num_replies, uploader_is_subbed, search_arguments

def GET_TOP_N_SEARCH_ALGORITHMS(N=100):
    conn = conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""


            SELECT search.Username,     
            (   
                SELECT COUNT(*) 
                FROM SEARCH_VOTES votes
                WHERE votes.Search_id = search.Search_id
            ) as VOTE_COUNT,
            search.Algorithm_Name, search.Date_Time
            
            FROM SEARCH_ALGORITHMS search
            
            order by VOTE_COUNT desc
            LIMIT {N}

    """)
    all_algos_without_counts = []
    for i in cursor.fetchall():
        # print(i)
        all_algos_without_counts.append([i[0],i[1],i[2],i[3]])
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()
    
    return all_algos_without_counts

    
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
    if search_algo_path == "":
        return ["", ""]
    
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
    
    if CHECK_DATE(username):
        daily_votes_left = 10 - daily_votes_left
        monthly_votes_left = 10 - monthly_votes_left
        yearly_votes_left = 10 - yearly_votes_left
    else:
        daily_votes_left = 0 
        monthly_votes_left = 0 
        yearly_votes_left = 0 
    return balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool

def GET_NOTIFICATIONS_BY_USER_ID(user_id):
    # TODO:GOING TO HAVE TO BE ABLE TO SPECIFY WHICH ONES YOU WANT TO SEE
    # TODO: SHOULD BE SIMPLIFED, ALSO DATE SORTING ISNT WORKING
    conn = connection.test_connection()

    # 1. GET INCOMING FOLLOWERS   
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT  creation_date,Friendship_Id, User_Id1, User_Id2
        FROM CONNECTIONS
        WHERE User_Id2 = {user_id} --USER_ID2 BECAUSE YOU'RE THE RECIEVER NOT THE SENDER
        ORDER BY creation_date       
    """)
    
    NOTIFS = []
    for i in cursor.fetchall():
        NOTIFS.append(["NEW FOLLOWER", [i[0],i[1],i[2],i[3]]])
    cursor.close()

    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT File_Id
        FROM FILES file
        WHERE file.UserId = {user_id}
    """)
    
    user_file_ids = []
    for i in cursor.fetchall():
        user_file_ids.append(i[0])
    cursor.close()
    #print(user_file_ids)

    # 2. GET POSTS
    REPLYING_TO_ID = []
    LIKES_TO_ID = []
    DISLIKES_TO_ID = []
    VOTES_TO_ID = []
    for i in user_file_ids:
        # REPLIES
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT  Date_Time, File_id, File_PATH,  Uploader, UserId, Post_foreign_id_source
            FROM FILES file
            WHERE file.Post_foreign_id_source = '{i}'
            ORDER BY Date_Time 
            LIMIT 100
        """)
        
        for j in cursor.fetchall():
            REPLYING_TO_ID.append([j[0],j[1],j[2],j[3],j[4],j[5]])
        cursor.close()

        # LIKES
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT Date_Time, Like_Id, File_id, Liker_Username
            FROM LIKES 
            WHERE File_id = '{i}'
            ORDER BY Date_Time
            LIMIT 100
            """)
        
        
        for k in cursor.fetchall():
            LIKES_TO_ID.append([k[0],k[1],k[2],k[3]])
        cursor.close()

        # DISLIKES
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT Date_Time, Dislike_Id, File_id, Disliker_Username, Date_Time
            FROM DISLIKES 
            WHERE File_id = '{i}'
            ORDER BY Date_Time
            LIMIT 100
            """)
        
        for y in cursor.fetchall():
            DISLIKES_TO_ID.append([y[0],y[1],y[2],y[3]])
        cursor.close()

        # VOTES
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT Date_Time, File_Vote_Id, File_id, Vote_Type, Voter_Username
            FROM FILE_VOTES 
            WHERE File_id = '{i}'
            ORDER BY Date_Time
            LIMIT 100
            """)
        
        for t in cursor.fetchall():
            VOTES_TO_ID.append([t[0],t[1],t[2],t[3],t[4],])
        cursor.close()

        # TAGS
        #TODO: IMPEMENT
        # FINANCIAL
        #TODO: IMPEMENT
            # - got money, withrdraw etc


        # MESSAGES

    for i in REPLYING_TO_ID:
        NOTIFS.append(["REPLY",i])
    for i in LIKES_TO_ID:
        NOTIFS.append(["LIKE",i])
    for i in DISLIKES_TO_ID:
        NOTIFS.append(["DISLIKE", i])
    for i in VOTES_TO_ID:
        NOTIFS.append(["VOTES", i])



    # 5. DAILY REWARD X
    # CREATE TABLE CASH_NOTIFICATIONS
    # PAYPAL MONEY ON ITS WAY
    # GOT YOUR FUNDS!
    # RECOVERY ETC
    # MESSAGES


    
    #for i in NOTIFS:
    #    print(i)
    
    return NOTIFS

def GET_PAYPAL_EMAIL_BY_USERNAME(username):
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT paypal_email 
    FROM USERS
    where username = '{username}'

    """)
    paypal_email = ''
    for i in cursor.fetchall():
        paypal_email = i[0]
        print("paypal_email:", paypal_email)
        # print(i)
    cursor.close()
    conn.close()
    return paypal_email

def GET_POST_URL_BY_ID(file_id):
    conn = connection.test_connection()
    cursor = conn.cursor()
    
    cursor.execute(f"""
        SELECT Uploader, File_PATH
        FROM FILES
        WHERE File_Id = '{file_id}'
    """)
    name = ''
    path = ''
    for i in cursor.fetchall():
        name = i[0]
        path = i[1]
        # print(i)
    # print(name, path)
    cursor.close()
    conn.close()
    return name, path


def GET_FILE_ALL_VOTES_BY_ID(file_id):
    conn = connection.test_connection()
    cursor = conn.cursor()
    DAILY = 0
    cursor.execute(f"""SELECT GET_FILE_VOTE_COUNT_TYPED({file_id}, 'Daily')""")
    for i in cursor.fetchall():
        DAILY = i[0]
    
    MONTHLY = 0
    cursor.execute(f"""SELECT GET_FILE_VOTE_COUNT_TYPED({file_id}, 'Monthly')""")
    for i in cursor.fetchall():
        MONTHLY = i[0]
    
    YEARLY = 0
    cursor.execute(f"""SELECT GET_FILE_VOTE_COUNT_TYPED({file_id}, 'Yearly')""")
    for i in cursor.fetchall():
        YEARLY = i[0]

    # print(DAILY, MONTHLY, YEARLY)
    cursor.close()
    conn.close()
    return DAILY, MONTHLY, YEARLY


def GET_SEARCH_LIKES_SINGLE_POST(searcher, file_id):
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        (
            SELECT COUNT(*)
            FROM LIKES likes
            WHERE likes.File_id = {file_id}
            AND '{searcher}' = likes.Liker_Username
        )
    """)
    likes = ""
    for i in cursor.fetchall():
        #print(i)
        likes = i[0]
    # FOR SOME STUPID REASON I CAN'T FIGURE OUT HOW TO GET BOTH OF THESE IN ONE QUERY, MAJOR EFFICIENCY BRAINFART
    
    cursor.execute(f"""
        (
            SELECT COUNT(*)
            FROM DISLIKES dislikes
            WHERE dislikes.File_id = {file_id}
            AND '{searcher}' = dislikes.Disliker_Username
        )
    """)
    dislikes = ""
    for i in cursor.fetchall():
        #print(i)
        dislikes = i[0]

    cursor.close()
    conn.close()
    # print(likes, dislikes)
    
    return likes, dislikes

def COUNT_TODAYS_SEATRCH_ALGOS_FOR_USER(user):
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM SEARCH_ALGORITHMS search_algo
        WHERE Username = '{user}'
        AND Date_Time >= date_trunc('day', now())::date
    """)
    count = 0
    for i in cursor.fetchall():
        print(i)
        count = i[0]
    
    cursor.close()
    conn.close()

    return count 

def GET_PATH_BY_FILE_ID(file_id):
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT File_Path
    FROM FILES 
    WHERE File_Id = '{file_id}'
    """)
    file_path = ""
    for i in cursor.fetchall():
        file_path = (i[0])
    
    cursor.close()
    conn.close()

    return file_path

def CREATE_TABLE_TRIBUNAL():
    conn = connection.test_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""DROP TABLE IF EXISTS TRIBUNAL CASCADE""")
        cursor.execute(
            f"""
                CREATE TABLE TRIBUNAL
                (
                Tribunal_id SERIAL PRIMARY KEY,   
                File_Id INT UNIQUE
                );
            """)
        conn.commit()
        print("TRIBUNAL CREATE COMPLETED")
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("\nHAD TO ROLLBACK TRIBUNAL CREATION" + str(e) )
    
    cursor.close()
    conn.close()

def INSERT_INTO_TRIBUNAL(file_id):
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO TRIBUNAL
        (File_Id)
        VALUES('{file_id}')
        ON CONFLICT DO NOTHING
    """)
    conn.commit()
    cursor.close()
    conn.close()

def CHECK_IF_FILE_IS_IN_TRIBUNAL(file_id):
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(F"""
    SELECT COUNT(*) 
    FROM TRIBUNAL WHERE
    File_Id = '{file_id}'
    """)
    count = 0
    for i in cursor.fetchall():
        count = i[0]
    if count > 1:
        print(True)
        return True
    else:
        print(False)
        return False

def DEMO_FILE_INSERT_TIKTOKS(num):
    path = "/root/mansura/Notes/TODO/PAGE LINKS/tiktok_links.txt"
    with open(path, 'r') as f:
        files = f.read()
        files_list = files.split("\n")
        #print(len(files_list))
        count = 0
        for i in files_list:
            value = CREATING_EMBED_STRUCTURE(i)
            if count > num:
                break
            # print("EXECUTING")
            FILE_INSERT("mazinosarchive", 12, size=100, post_foreign_id_source="None", 
                file_path="N-A", post_file="", 
                post_text="Mazinos Archive", age_18="", 
                external_link=value,
                distro_details=["EQUAL DISTRIBUTION", "None"])
            count += 1 
            
       
            