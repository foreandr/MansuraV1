from itertools import pairwise
import psycopg2
import random
import os
import csv
import json


def GET_CURRENT_DATE():
    conn = test_connection()

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


def CHECK_DATE(my_username):
    conn = test_connection()

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

conn = test_connection()
cursor = conn.cursor()

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
    print("SEARCH PATH:", search_algo_path)
    username = search_algo_path.split("-")[0]
    f = open(f'/home/app/DOCKERIZED/static/#UserData/{username}/search_algorithms/{search_algo_path}.json')
    data = json.load(f)
    f.close()


    ORDER_BY_CLAUSE = data["ORDER_BY_CLAUSE"]
    WHERE_CLAUSE = data["WHERE_CLAUSE"]
    return [ORDER_BY_CLAUSE, WHERE_CLAUSE]


def universal_dataset_function(search_type, search_algo_path="foreandr-1", page_no="1", search_user="None", file_id="None", profile_username="None"):
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


    conn = test_connection()
    cursor = conn.cursor()

    order_by_clause, where_clause = GRAB_SEARCH_ALGO(search_algo_path)
    print("CUSTOM QUERY            :", where_clause, order_by_clause)
    print("PROFILE SEARCH CLAUSE   :",profile_search_clause)
    print("FOREIGN ID              :", foreign_id_text_entry)
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

        OFFSET WHICH_PAGES({page_no}, 100)  ROWS 
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
    

    print("1 : file_ids_list              :", file_ids_list)
    print("2 : USERNAMES                  :", usernames_list)
    print("3 : paths_list                 :", paths_list)
    #print("4 :dates_list           :", dates_list)
    print("5 : post_sources_list          :", post_sources_list)

    print("6: daily_left                 :", daily_left)
    print("7: monthly_left               :", monthly_left)
    print("8: yearly_left                :", yearly_left)

    print("9 : day_votes                  :", day_votes)
    print("10 : month_votes                :", month_votes)
    print("11 : year_votes                 :", year_votes)
    print("12 : user_balance               :", user_balance)

    print("13: dailypool                  :", dailypool)
    print("14: monthlypool                :", monthlypool)
    print("15: yearlypool                 :", yearlypool )
    
    print("16:POST_PAGE MAIN_DAILY       :", daily_votes_singular)
    print("17:POST_PAGE MAIN_MONTHLY     :", monthly_votes_singular)
    print("18:POST_PAGE MAIN_YEARLY      :", yearly_votes_singular)
   
           
    return file_ids_list, usernames_list, paths_list, dates_list, post_sources_list, daily_left, monthly_left, yearly_left, day_votes, month_votes, year_votes, user_balance, dailypool, monthlypool, yearlypool, daily_votes_singular,  monthly_votes_singular, yearly_votes_singular
    

def SEARCH_ALGO_CREATE_TABLE():
    conn = test_connection()
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
    conn = test_connection()
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

    my_path = F"/home/app/DOCKERIZED/static/#UserData/{username}/search_algorithms/{new_path}.json" 
    config_json = {
        'ORDER_BY_CLAUSE':f"{order_by_clause}",
        'WHERE_CLAUSE'   :f"{where_clause}"
    }
    jsonString = json.dumps(config_json)
    jsonFile = open(f"{my_path}", "w")
    jsonFile.write(jsonString)
    jsonFile.close()
    #TODO: EVENTUALLY I SHOULD RUN THESE AGAINST A TESTNET OR SOMETHING AUTOMATICALLY AND JUST SEE IF THEY PRODUCE A RESULT
    #TODO: FOR NOW I WILL JUST CHECK THEM MANUALLY
    




#SEARCH_ALGO_CREATE_TABLE()
#SEARCH_ALGO_INSERT('foreandr', 'foreandr-basic-top-month', "ORDER BY U.username DESC", "")
#SEARCH_ALGO_INSERT('andrfore', 'andrfore-basic-top-month', "ORDER BY U.username ASC", f"AND U.username LIKE 'foreandr%'")
#SEARCH_ALGO_INSERT('foreandr', 'foreandr-basic-top-month2')
#SEARCH_ALGO_INSERT('foreandr', 'foreandr-basic-top-month3')
#SEARCH_ALGO_INSERT('foreandr', 'foreandr-basic-top-month4')

#universal_dataset_function(search_type="home", search_algo_path="foreandr-1", page_no="1", search_user="foreandr", file_id="None", profile_username="None")

#DATASET CHECKS
#universal_dataset_function(search_type="post", search_algo_path="foreandr-1", page_no="1", search_user="foreandr", file_id="4")
#universal_dataset_function(search_type="post", search_algo_path="andrfore-2", page_no="1", search_user="foreandr", file_id="4")
#HOME CHECKS
#universal_dataset_function(search_type="home", search_algo_path="foreandr-1", page_no="1", search_user="foreandr")
#universal_dataset_function(search_type="home", search_algo_path="andrfore-2", page_no="1", search_user="foreandr")
# PROFILE CHECKS
#universal_dataset_function(search_type="prof", search_algo_path="foreandr-1", page_no="1", search_user="foreandr", profile_username="oguser")
#universal_dataset_function(search_type="prof", search_algo_path="andrfore-2", page_no="1", search_user="foreandr", profile_username="oguser")


# 

            
GET_VOTES_AND_BALANCE_AND_PAYOUTS("foreandr")

'''
cursor.execute(f"""
    SELECT *
    FROM USERS
""")

for i in cursor.fetchall():
    print(i)
'''