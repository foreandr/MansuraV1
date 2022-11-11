"""
PROCEDURES AND FUNCTIONS
AUTHOR:
PURPOSE:
DATE:
"""
#0
# NEED A VOTE RESET FUNCTION

import Python.db_connection as connection

def PROCEDURE_CUSTOM_MODEL_INSERT():
    conn = connection.test_connection()
    print("CREATING [PROCEDURE_CUSTOM_MODEL_INSERT] PROCEDURE..")
    try:
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE OR REPLACE PROCEDURE CUSTOM_MODEL_INSERT(
                model_path varchar(200), 
                model_description 	VARCHAR(400), 
                foreign_file_id INT,  
                personal_username varchar(200)
                )
                LANGUAGE SQL
                AS $$
                INSERT INTO MODEL(Local_File_PATH, Date_Time,Model_Description, Foreign_File_id, Uploader) -- can be png or jpg, or mp4
                VALUES (model_path, now() ,model_description, foreign_file_id, personal_username) 
            $$;
        """)
        conn.commit()
    except Exception as e:
        print(e)
        cursor.execute("ROLLBACK")
        print("ERROR: [PROCEDURE_CUSTOM_MODEL_INSERT] " + str(e))


def PROCEDURE_USER_MONTHLY_SUBSCRIPTION_FEE():
    conn = connection.test_connection()
    print("CREATING [PROCEDURE_USER_MONTHLY_SUBSCRIPTION_FEE] PROCEDURE...")
    print("BUG!!!!!!!!!!!!!!!!!!!! -- THIS NEEDS TO BE CHANGED TO MINUS ")
    try:
        cursor = conn.cursor()
        cursor.execute(f"""
        CREATE OR REPLACE PROCEDURE USER_MONTHLY_SUBSCRIPTION_FEE(my_username varchar)
            LANGUAGE SQL
            AS $$
                UPDATE USERS
                SET balance = balance - 5.00 
                WHERE username = my_username
                ;
            $$;
        """)
        conn.commit()
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("ERROR:  [PROCEDURE_USER_MONTHLY_SUBSCRIPTION_FEE] " + str(e))


def PROCEDURE_CUSTOM_DELETION():
    conn = connection.test_connection()
    print("CREATING [CUSTOM_DELETION] PROCEDURE..")
    cursor = conn.cursor()
    try:
        
        cursor.execute(f"""
        CREATE OR REPLACE PROCEDURE CUSTOM_DELETION(user_id_first INT, user_id_second INT)
            LANGUAGE SQL
            AS $$
                DELETE FROM CONNECTIONS AS conn
                WHERE conn.User_Id1 = user_id_first AND conn.User_Id2 = user_id_second
            $$;
        """)
        conn.commit()
    except Exception as e:
         cursor.execute("ROLLBACK")
         print("ERROR:  [CUSTOM_DELETION] " + str(e))


def PROCEDURE_ENTER_FILE_VOTE():
    conn = connection.test_connection()
    print("CREATING [ENTER_FILE_VOTE] PROCEDURE..")
    try:
        cursor = conn.cursor()
        cursor.execute(f"""
        CREATE OR REPLACE PROCEDURE ENTER_FILE_VOTE(file_id BIGINT, voter VARCHAR, vote_type VARCHAR)   
        LANGUAGE SQL
        AS $$
            INSERT INTO FILE_VOTES(File_id, Vote_Type, Voter_Username, Date_Time)
            VALUES(file_id, voter, vote_type, CURRENT_TIMESTAMP)
        $$;
        """)
        conn.commit()
    except Exception as e:
         cursor.execute("ROLLBACK")
         print("ERROR:  [ENTER_FILE_VOTE] " + str(e))


def PROCEDURE_ENTER_MODEL_VOTE():
    conn = connection.test_connection()
    print("CREATING [ENTER_MODEL_VOTE] PROCEDURE..")
    try:
        cursor = conn.cursor()
        cursor.execute(f"""
        CREATE OR REPLACE PROCEDURE ENTER_MODEL_VOTE(model_id BIGINT, voter VARCHAR)   
        LANGUAGE SQL
        AS $$
            INSERT INTO MODEL_VOTES(Model_id, Voter_Username)
            VALUES(model_id, voter)
        $$;
        """)
        conn.commit()
    except Exception as e:
         cursor.execute("ROLLBACK")
         print("ERROR:  [ENTER_MODEL_VOTE] " + str(e))


def PROCEDURE_CHANGE_PASSWORD():
    conn = connection.test_connection()
    print("CREATING [CHANGE_PASSWORD] PROCEDURE..")
    try:
        cursor = conn.cursor()
        cursor.execute(f"""
        CREATE OR REPLACE PROCEDURE CHANGE_PASSWORD_FOR_EMAIL(user_email varchar, new_password varchar)
            LANGUAGE SQL
            AS $$
                UPDATE USERS
                SET password = new_password
                WHERE USERS.email =  user_email;
            $$;
        """)
        conn.commit()
    except Exception as e:
         cursor.execute("ROLLBACK")
         print("ERROR:  [CHANGE_PASSWORD] " + str(e))


def FUNCTION_GET_ALL_DATASETS():
    conn = connection.test_connection()
    
    print("CREATING [GET_ALL_DATASETS] FUNCTION...")
    try:
        
        cursor = conn.cursor()
        
        cursor.execute(f"""drop function GET_ALL_DATASETS""")
        cursor.execute(f"""
        CREATE OR REPLACE FUNCTION GET_ALL_DATASETS(page_no INT, vote_type varchar, how_many INT)
            
        RETURNS TABLE(    
            username varchar,
            File_PATH varchar,
            Description varchar,
            Date_Time timestamp,
            File_size BIGINT,
            File_id INT
            )
            
        LANGUAGE plpgsql
        AS $function$

        DECLARE 
        BEGIN
            RETURN QUERY
                SELECT U.username, F.File_PATH "Path", F.Description "Desc", F.Date_Time, F.File_size "Size", F.File_id "ID"
                FROM USERS as U
                    
                INNER JOIN FILES as F
                ON F.UserId = U.User_Id

                ORDER BY GET_FILE_VOTE_COUNT_TYPED(F.File_Id, vote_type) DESC
                    
                OFFSET WHICH_PAGES(page_no, how_many)  ROWS 
                LIMIT how_many;             
        END
                    

        $function$
        ;
        """)
        conn.commit()
        # print("goodt things happened: [GET_ALL_DATASETS_BY_DATE]")
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("ERROR: [GET_ALL_DATASETS_BY_DATE] " + str(e))


def FUNCTION_GET_USER_ID():
    conn = connection.test_connection()
    print("CREATING [GET_USER_ID] FUNCTION..")
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
        CREATE OR REPLACE FUNCTION GET_USER_ID(my_username varchar)
            RETURNS TABLE(    
            User_Id INT,
            Username varchar)
            
        LANGUAGE plpgsql
        AS $function$
        BEGIN
        RETURN QUERY
                SELECT U.User_Id, U.username
                FROM USERS AS U
                WHERE U.username = my_username;
        END
        $function$
        ;
        """)
        conn.commit()
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("ERROR: [GET_USER_ID] " + str(e))


def FUNCTION_GET_FILE_VOTE_COUNT():
    conn = connection.test_connection()
    print("CREATING [GET_FILE_VOTE_COUNT] FUNCTION..")
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
        CREATE OR REPLACE FUNCTION GET_FILE_VOTE_COUNT(my_file_id INT)
            RETURNS TABLE(    
            num_files bigint
            )
            
        LANGUAGE plpgsql
        AS $function$
        BEGIN
            RETURN QUERY
                SELECT COUNT(*)
                FROM FILE_VOTES
                WHERE File_id = my_file_id;
        END
        $function$
        ;
        """)
        conn.commit()
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("ERROR: [GET_FILE_VOTE_COUNT] " + str(e))


def FUNCTION_GET_FOLLOWING():
    conn = connection.test_connection()
    print("CREATING [GET_GET_FOLLOWING] FUNCTION..")
    cursor = conn.cursor()
    try:
        # cursor.execute(f"""DROP FUNCTION GET_FOLLOWING""")
        cursor.execute(f"""
        CREATE OR REPLACE FUNCTION GET_FOLLOWING(my_username varchar)
            RETURNS TABLE(    
                User_Id INT,
                follower varchar,
                User_Id2 INT,
                followed varchar
            )
            
        LANGUAGE plpgsql
        AS $function$
        BEGIN
            RETURN QUERY
                SELECT U.User_Id, U.username, conn.User_Id2, users2.username 
                FROM USERS AS U
                
                INNER JOIN CONNECTIONS conn
                ON U.User_Id = conn.User_Id1
                
                INNER JOIN USERS users2
                ON conn.User_Id2 = users2.User_Id
                
                WHERE U.username = my_username;

        END
        $function$
        ;
        """)
        conn.commit()
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("ERROR: [GET_FOLLOWING] " + str(e))


def FUNCTION_GET_FOLLOWERS():
    conn = connection.test_connection()
    print("CREATING [GET_GET_FOLLOWERS] FUNCTION..")
    cursor = conn.cursor()
    try:
        # cursor.execute(f"""DROP FUNCTION IF EXISTS GET_FOLLOWERS""")
        cursor.execute(f"""
        CREATE OR REPLACE FUNCTION GET_FOLLOWERS(my_username varchar)
            RETURNS TABLE(    
                User_Id INT,
                follower varchar,
                User_Id2 INT,
                followed varchar
            )
            
        LANGUAGE plpgsql
        AS $function$
        BEGIN
            RETURN QUERY
                SELECT U.User_Id, U.username, conn.User_Id2, users2.username 
                FROM Users as U
                
                INNER JOIN CONNECTIONS conn
                ON U.User_Id = conn.User_Id2

                INNER JOIN USERS users2
                ON conn.User_Id1 = users2.User_Id
                
                WHERE U.Username = my_username;


        END
        $function$
        ;
        """)
        conn.commit()
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("ERROR: [GET_FOLLOWERS] " + str(e))


def FUNCTION_GET_FILES():
    conn = connection.test_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"""drop function if exists GET_FILES""")
        cursor.execute(f"""
        CREATE OR REPLACE FUNCTION GET_FILES(my_username varchar)
            RETURNS TABLE(
                File_id INT,
                File_PATH varchar,
                File_size BIGINT,
                Description varchar,
                UserId INT,
                Date_Time timestamp,
                username varchar
            )    
            LANGUAGE plpgsql
            AS $function$
            BEGIN
            RETURN QUERY
                SELECT files.*, users.username
                FROM FILES files

                INNER JOIN USERS users
                ON files.UserId = users.User_Id

                where users.username = my_username;
            END
            $function$
            ;
            """)
        conn.commit()
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("ERROR: [GET_FILES] " + str(e))   


def FUNCTION_GET_USER_BALANCE():
    conn = connection.test_connection()
    print("CREATING [GET_USER_BALANCE] FUNCTION..")
    cursor = conn.cursor()
    try:
        cursor.execute(f"""DROP FUNCTION GET_USER_BALANCE""")
        cursor.execute(f"""
        CREATE OR REPLACE FUNCTION GET_USER_BALANCE(my_username varchar)
            RETURNS TABLE(    
                User_Id INT,
                username varchar,
                balance decimal
            )
        LANGUAGE plpgsql
        AS $function$
        BEGIN
            RETURN QUERY
                SELECT U.User_Id, U.username, U.balance 
                FROM USERS U 
                WHERE U.username = my_username;
        END
        $function$ 
        """)

        conn.commit()
    
    
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("ERROR: [GET_USER_BALANCE] " + str(e))


def FUNCTION_GET_MODELS_BY_FILE_ID():
    conn = connection.test_connection()
    print("CREATING [GET_MODEL_BY_FILE_ID] FUNCTION..")
    cursor = conn.cursor()
    try:
        cursor.execute(f"""DROP FUNCTION GET_MODELS_BY_FILE_ID""")
        cursor.execute(f"""
        CREATE OR REPLACE FUNCTION GET_MODELS_BY_FILE_ID(my_file_id INT)
        RETURNS TABLE(    
                Model_id INT,
                Local_File_PATH varchar,
                Model_Description varchar,
                model_Date_Time timestamp,
                Foreign_File_id INT,
                Uploader varchar,
                User_Id INT,
                File_PATH varchar,
                File_size BIGINT,
                UserId INT,
                file_Date_Time timestamp
            )
        LANGUAGE plpgsql
        AS $function$
        BEGIN
        RETURN QUERY    
            SELECT 
                model.Model_id "MODEL_ID",
                model.Local_File_PATH "MODEL_ID",
                model.Model_Description "MODEL_ID",
                model.Date_Time "MODEL_ID",
                model.Foreign_File_id "MODEL_ID",
                model.Uploader "MODEL UPLOADER",
                users.User_Id "MODEL USER ID", 
                files.File_PATH "CSV FILE PATH", 
                files.File_size "CSV FILE PATH",  
                files.UserId "CSV USER ID" , 
                files.Date_Time "CSV UPLOAD DATE"
                
                FROM MODEL AS model
                
                INNER JOIN USERS as users
                ON model.Uploader = users.username
                
                INNER JOIN FILES as files
                ON model.Foreign_File_id = files.File_id
                
                WHERE files.File_id = my_file_id;
            END
            $function$
            ;
        """)
        conn.commit()
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("ERROR: [GET_MODEL_BY_FILE_ID] " + str(e))   


def FUNCTION_GET_FILE_ID():
    conn = connection.test_connection()

    print("CREATING [GET_FILE_ID] FUNCTION..")
    cursor = conn.cursor()
    try:
        cursor.execute(f"""DROP FUNCTION IF EXISTS GET_FILE_ID""")
        cursor.execute(f"""
        CREATE OR REPLACE FUNCTION GET_FILE_ID(my_username varchar, my_file_path varchar)
            RETURNS TABLE(    
                File_Id INT
            )
        LANGUAGE plpgsql
        AS $function$
        BEGIN
            RETURN QUERY
                
                SELECT F.File_Id
                FROM Files F

                INNER JOIN Users U
                ON U.username = my_username

                WHERE F.File_PATH LIKE '%' || my_file_path -- WEIRD AS FUCK BUT WORKS (SEE THAT || AS CONCATINATION?)
                AND U.username = my_username; 
                
                -- THIS MAY BE REDUNDANT BECAUSE THE PATH IS GOING TO BE UNIQUE, 
                --  BUT IN THE FUTURE THE FILENAME MAY NOT BE UNIQUE
        END
        $function$ 
        """)
        conn.commit()
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("ERROR: [GET_FILE_ID] " + str(e))


def FUNCTION_MODEL_GET_NUM_VOTES_BY_MODEL_ID():
    conn = connection.test_connection()

    print("CREATING [MODEL_GET_NUM_VOTES_BY_MODEL_ID] FUNCTION..")
    cursor = conn.cursor()
    try:
        cursor.execute(f"""DROP FUNCTION IF EXISTS MODEL_GET_NUM_VOTES_BY_MODEL_ID""")
        cursor.execute(f"""
        CREATE OR REPLACE FUNCTION MODEL_GET_NUM_VOTES_BY_MODEL_ID(my_model_id INT)
            RETURNS INT
            LANGUAGE plpgsql
        AS $function$

        declare num_votes int;

        BEGIN 
                SELECT COUNT(*)
                
                INTO num_votes

                FROM MODEL_VOTES

                WHERE Model_id = my_model_id;
                
                RETURN num_votes;

        END
        $function$ 
        """)
        conn.commit()
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("ERROR: [MODEL_GET_NUM_VOTES_BY_MODEL_ID] " + str(e))


def FUNCTION_GET_FILE_VOTE_COUNT_TYPED():
    conn = connection.test_connection()

    print("CREATING [GET_FILE_VOTE_COUNT_TYPED] FUNCTION..")
    cursor = conn.cursor()
    try:
        cursor.execute(f"""DROP FUNCTION IF EXISTS GET_FILE_VOTE_COUNT_TYPED""")
        cursor.execute(f"""
        CREATE OR REPLACE FUNCTION GET_FILE_VOTE_COUNT_TYPED(my_file_id INT, my_vote_type varchar)
            RETURNS TABLE(    
            num_files bigint
            )
            
        LANGUAGE plpgsql
        AS $function$
        BEGIN
            CASE
                WHEN (my_vote_type != 'TOTAL' ) THEN
                    RETURN QUERY
                            SELECT COUNT(*)
                            FROM FILE_VOTES AS csv
                            WHERE File_id = my_file_id 
                            AND csv.Vote_Type = my_vote_type;
                           
                ELSE
                    RETURN QUERY
                            SELECT COUNT(*)
                            FROM FILE_VOTES AS csv
                            WHERE File_id = my_file_id;
            END CASE;
        END
        $function$
        ;
        """)
        conn.commit()
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("ERROR: [GET_FILE_VOTE_COUNT_TYPED] " + str(e))


def FUNCTION_WHICH_PAGES():
    conn = connection.test_connection()

    #TODO:make proper syntax
    # ALSO EXPLAIN WHAT THE HELL IS GOING ON HERE
    cursor = conn.cursor()
    try:
        cursor.execute(f"""drop function IF EXISTS WHICH_PAGES""")    
        cursor.execute(f"""
            CREATE OR REPLACE FUNCTION WHICH_PAGES(page_no integer, how_many int)
                RETURNS integer
                LANGUAGE plpgsql AS
                $func$
                    BEGIN
                        RETURN (page_no - 1) * how_many;
                    END
                $func$;
    """)
        print("successfully created [WHICH_PAGES]")
    except Exception as e:
        cursor.execute("ROLLBACK")
        print(e)


def FUNCTION_GET_CALCULATED_UPLOAD_VOLUME_BY_MONTH():
    conn = connection.test_connection()
    print("CREATING [GET_CALCULATED_UPLOAD_VOLUME_BY_MONTH] FUNCTION..")
    cursor = conn.cursor()
    try:
        cursor.execute(f"""DROP FUNCTION IF EXISTS GET_CALCULATED_UPLOAD_VOLUME_BY_MONTH""")
        cursor.execute(f"""
            CREATE OR REPLACE FUNCTION GET_CALCULATED_UPLOAD_VOLUME_BY_MONTH(my_user_id INT)
                RETURNS INT
                
                LANGUAGE PLPGSQL
                AS $function$

                declare total_file_volume_this_month int;

                BEGIN
                    SELECT SUM(F.Post_total_size)

                    INTO total_file_volume_this_month

                    FROM FILES as F

                    WHERE F.UserId = my_user_id
                     
                    AND F.Date_Time > date_trunc('month', current_date); -- current date bigger than first of month

                    RETURN total_file_volume_this_month;

                END
                $function$ 
        """)
    
    except Exception as e:
        cursor.execute("ROLLBACK")
        print("ERROR: [GET_CALCULATED_UPLOAD_VOLUME_BY_MONTH] " + str(e))


# --

def TEST_SELECT_ALL_USERS():
    conn = connection.test_connection()
    # print("hi")
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * 
        FROM USERS
        -- WHERE username = 'foreandr'
        ORDER BY User_Id
    """)
    results = cursor.fetchall()
    for value in results:
        print(value)


def TEST_SELECT_ALL_MODELS():
    conn = connection.test_connection()
    # print("hi")
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT model.*, files.UserId
        FROM MODEL model

        INNER JOIN FILES files
        ON MODEL.Foreign_File_id = files.File_Id
    """)
    results = cursor.fetchall()
    for value in results:
        print(value)


def TEST_SELECT_ALL_FILE_VOTES():
    conn = connection.test_connection()
    # print("hi")
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * 
        FROM FILE_VOTES
        -- WHERE username = 'foreandr'
        ORDER BY User_Id
    """)
    results = cursor.fetchall()
    for value in results:
        print(value)


def TEST_SELECT_ALL_MANSURA_SUBSCRIPTIONS():
    conn = connection.test_connection()
    # print("hi")
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * FROM SUBSCRIPTIONS_MANSURA
    """)
    results = cursor.fetchall()
    print()
    for value in results:
        print(value)


def TEST_SELECT_ALL_FILES():
    conn = connection.test_connection()
    # print("hi")
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * FROM FILES
    """)
    results = cursor.fetchall()
    print()
    for value in results:
        print(value)


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
    return yearly 

