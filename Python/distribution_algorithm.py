'''NOTE==================================
WHEN DOING TESTS, YOU HAVE TO RUN WITH
import db_connection as connection

WHEN RUNNING IN PROD, YOU AHVE TO RUN WITH
import Python.db_connection as connection


ALL OF THIS CAN CERTAINLY BE OPTOMIZED, JUST GETTING THE THING WORKING FOR NOW
'''

import numpy as np
import csv
from datetime import datetime
import pytz
import json


try: #LIVE VERSION
    import Python.db_connection as connection
    from Python.helpers import print_green, print_title, log_function
    from Python.generating_excel import WRITE_HEADERS_TO_EXCEL
except: #TEST VERSION ---#DEFINITELY NOT A GOOD IDEA TO DO THIS
    from generating_excel import WRITE_HEADERS_TO_EXCEL
    import db_connection as connection
    from  helpers import print_green, print_title, log_function


def GET_REPLYING_TO(file_id):
    
    conn = connection.test_connection()
    cursor = conn.cursor()

    # EXECUTING QUERY TO GET THE ORIGINAL FILE ID
    cursor.execute(f"""
                SELECT file.Post_foreign_id_source
                FROM FILES file
                WHERE file.File_id = '{file_id}'            
        """)

    results = cursor.fetchall()
    replying_to_id = ""
    
    for value in results:
        replying_to_id = value[0]
        #print(replying_to_id)
    #print(F"ORIGINAL    :{file_id}")
    #print(F"REPLYING TO :{replying_to_id}")

    if (replying_to_id == "" or replying_to_id == "N-A" or replying_to_id == "None"):        
        #print("NO CONNECTION TO ANOTHER FILE:", replying_to_id)
        cursor.close()
        conn.close()
        return "None"
    else: # IF IT IS A REPLY, GRAB THE USERNAME
        #print("GETTING USERNAME:", replying_to_id)
        cursor.execute(f"""
                SELECT users.username
                FROM FILES file
            
                INNER JOIN USERS users
                ON file.UserId = Users.User_Id

                WHERE file.File_id = '{replying_to_id}'            
            """)
        
        results = cursor.fetchall()
        for value in results:
            #print(value)
            username = value[0]

        #print("HOST USER IS:", username)

        cursor.close()
        conn.close()

        return username


def FUNCTION_LOG_VOTER_DICT_WITH_FILE_ID_DICT(vote_type, testing=False):
    print(f"CURRENTLY TESTING? : {testing}")
    #print()
    #print("FUNCTION_LOG_VOTER_DICT_WITH_FILE_ID_DICT")
    
    conn = connection.test_connection()
    cursor = conn.cursor()
    my_dict = GET_FREQUENCY_DICT_TYPED(vote_type)
    #print(my_dict[4])
    
    non_equity_dict = {}
    for key, value in my_dict.items():        
        if key != "EQUITY" and key != "SEARCH":
            #print(f"\nFILE ID: {key}\t{value['AMOUNT']}")
            
            value = {
                "VALUE":value, 
                "ORDER":None,
                }
               
            uploader = GET_UPLOADER_OF_FILE_BY_ID(key)
            results_array = GET_ALL_VOTES_BY_FILE_ID_TYPED(key, vote_type)
            results_array.insert(0, uploader) # insert uploader to 0 so they get 50% by default
            value['ORDER'] = results_array
            
            #print("FIRST RESULT: ", results_array)
            #print("UPLOADER    :", uploader)
            #print("VALUE       :", value)
            
            # REPLYING LOGIC
            original_replying_to_user = GET_REPLYING_TO(key)
            if original_replying_to_user != "None":
                n_percent = float(BROKEN_ROUNDING(value["VALUE"]["AMOUNT"])) * 0.10
                #print(n_percent) 
                value["VALUE"]["AMOUNT"] = BROKEN_ROUNDING(float(value["VALUE"]["AMOUNT"]) - n_percent)
                value["REPLY"] = {
                    "REPLYING_TO": original_replying_to_user,
                    "AMOUNT": BROKEN_ROUNDING(n_percent)
                }

            # RATIO LOGIC
            #print(f"KEY IS {key}\n")
            ratio_file_id = CHECK_FOR_HIGHEST_RATIO(key, vote_type)
            if ratio_file_id !="None":
                n_percent = BROKEN_ROUNDING(value["VALUE"]["AMOUNT"]) * 0.10
                value["VALUE"]["AMOUNT"] = BROKEN_ROUNDING(float(value["VALUE"]["AMOUNT"]) - n_percent)
                #print(ratio_file_id)
                value["RATIO"] = {
                        F'{GET_USERNAME_BY_FILE_ID(ratio_file_id)}': BROKEN_ROUNDING(n_percent)
                }
                #print(value)
                #print()
                
                #print(value)
                #print(value["RATIO"], type(value["RATIO"]))
            # remove all votes of particular type from that file id
            if testing:
                pass
            else:
                ''' IMPORTANT DELETE CHECKPOINT 0'''
                cursor.execute(f"""
                    DELETE FROM FILE_VOTES
                    WHERE File_id = {key}
                    AND Vote_Type = '{vote_type}'
                    """)
                conn.commit()  
                

            non_equity_dict[key] = value
        else:
            non_equity_dict[key] = value


        #print("FILE ID=",key,":", value) 
    #print("\n")   

    #print("\nCHECKPOINT 1")
    #PROBABLY THE BEST THING TO PRINT TO KNOW WHAT'S GOING ON
    #NOTE, RATIO HAS ALREADY BEEN TAKEN OUT OF AMOUNT, IT ISN'T INCORRECT, CAN BE CHECKED WITH ALGOS
    
    for key, value in non_equity_dict.items():
        log_string = str(key) + ":" + str(value)
        log_function(msg_type="distro", log_string=log_string, vote_type=vote_type, distro_type="initial")
        #print(key, ":", value)
    # exit(0)
    #exit()  #THIS IS WHERE IM WORKIN CHECKPOINT 1
    UPDATE_BALANCES_TYPED(vote_type, non_equity_dict, testing)
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()
    print(F"DONE {vote_type} DISTRIBUTION")

    #print(new_dict)
    #exit()
    
    # TODO:RESET VOTE TYPE ON EACH DATASET WHO HAS ONE BACK TO ZERO


def GET_FREQUENCY_DICT_TYPED(my_vote_type):
    #print("GET_FREQUENCY_DICT_TYPED")
    conn = connection.test_connection()

    cursor = conn.cursor()
    dataset_array = GET_ALL_TYPED(my_vote_type)
    freq_array = []
    for i in dataset_array:
        #print(i)
        freq_array.append(i[0])
    
    freq = CountFrequency(freq_array)
    
    #print(F"KEY = FILE_ID | [0]  NUM_VOTES | [1] PERCENTAGE | [2] AMOUNT")
    new_dict = {}

    equity_percentage = 0
    if my_vote_type == "Daily":
        equity_percentage = 0.20
    elif my_vote_type == "Monthly":
        equity_percentage = 0.20
    elif my_vote_type == "Yearly":
        equity_percentage = 0.20
    search_equity_percentage = 0.20

    total_vote_count_typed = GET_TOTAL_VOTE_COUNT(my_vote_type)
    total_capital_typed = GET_TYPED_PAYOUT( my_vote_type)
      
    
    total_capital_for_search = total_capital_typed * search_equity_percentage
    total_capital_for_equity = total_capital_typed * equity_percentage
    #print("t1search", total_capital_for_search, search_equity_percentage)
    #print("t2global", total_capital_for_equity, equity_percentage)
      
    total_capital_typed = total_capital_typed - (total_capital_for_equity + total_capital_for_search)
    

    print(F"VOTE TYPE : {my_vote_type}")
    #print(F"VOTE COUNT: {total_vote_count_typed}")
    print(F"{my_vote_type} CAPITAL FOR TOTAL   : {GET_TYPED_PAYOUT( my_vote_type)}")
    print(F"{my_vote_type} CAPITAL FOR MANSURA : {BROKEN_ROUNDING(total_capital_for_equity)} [%{equity_percentage}]")
    print(F"{my_vote_type} CAPITAL FOR SEARCH  : {BROKEN_ROUNDING(total_capital_for_search)} [%{search_equity_percentage}]")
    print(F"{my_vote_type} CAPITAL FOR USERS   : {total_capital_typed}")
    
    for key, value in freq.items():        
        #print("FILE ID=", key, ":", "VOTES=",value)
        value = {"VOTES":value, 
                "PERCENT":"", 
                "AMOUNT": ""
                }
        
        value["PERCENT"] =  (value["VOTES"] / total_vote_count_typed)
        value["AMOUNT"] = BROKEN_ROUNDING(value["PERCENT"] * total_capital_typed) 
        value["PERCENT"] =  "".join(("%", str(value["PERCENT"])))

        new_dict[key] = value
    
        
    
    #print("\nTESTERS\n")
    new_dict["EQUITY"] = BROKEN_ROUNDING(total_capital_for_equity)
    new_dict["SEARCH"] = BROKEN_ROUNDING(total_capital_for_search)
    #for key, value in new_dict.items():        
    # #print(key, ":",value)
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()

    return new_dict


def GET_UPLOADER_OF_FILE_BY_ID(file_id):
    #print("GET_UPLOADER_OF_FILE_BY_ID")

    conn = connection.test_connection()
    cursor = conn.cursor()
    try:
        
        cursor.execute(f"""
            SELECT users.username
            
            FROM FILES file
        
            INNER JOIN USERS users
            ON file.UserId = Users.User_Id

            WHERE file.File_id = '{file_id}'
        
        """)
        conn.commit()
        results = cursor.fetchall()
        for value in results:           
            return value[0]
    
    except Exception as e:
        pass
    #print(e)
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()


def GET_ALL_VOTES_BY_FILE_ID_TYPED(file_id, vote_type):
    #print("GET_ALL_VOTES_BY_FILE_ID_TYPED")

    conn = connection.test_connection()
    
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT Voter_Username 
        FROM FILE_VOTES
        WHERE File_id = {file_id}
        AND Vote_type = '{vote_type}'
        ORDER BY Date_Time

    """)
    results = cursor.fetchall()
    
    list_of_names = []

    for i in results:
        i = i[0]
        list_of_names.append(i)

    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()

    return list_of_names


def GET_TYPED_PAYOUT(vote_type):
    #print("GET_TYPED_PAYOUT")
    conn = connection.test_connection()
        
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT {vote_type} 
        FROM PAYOUTS;
    """)
    conn.commit()
    results = cursor.fetchall()
    for value in results:
        return value[0]
    
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()


def GET_TOTAL_VOTE_COUNT(type):
    #print("GET_TOTAL_VOTE_COUNT")
      
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
            #print(F"TOTAL {type} VOTES: ", value[0])
            num_votes = value[0]
            break
        
        # CLOSE CURSOR AND CONNECTION [MANDATORY]        
        cursor.close()
        conn.close()
        return num_votes
    except Exception as e:
        cursor.execute("ROLLBACK")
        #print("ERROR:  [GET_TOTAL_VOTE_COUNT] " + str(e))

        # CLOSE CURSOR AND CONNECTION [MANDATORY]        
        cursor.close()
        conn.close()


def CountFrequency(my_list):
 
    # Creating an empty dictionary
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1    
    
    return freq


def UPDATE_BALANCE_FROM_FINAL_DICT(final_dict, vote_type, testing=False):
#print("3")
    #print(F"\nUPDATING {vote_type} \n| {final_dict}")
    conn = connection.test_connection()  
    cursor = conn.cursor()
    #print("\n\nUPDATING BALANCE FROM LIST")
    #for key, value in final_dict.items():
    ##print(key, ":", value)

    # 1 UPDATE EACH USER + THEIR WINNINGS
    try:
        for key, value in final_dict.items():        
            if key != "EQUITY" and key != "SEARCH":
                #print("FINAL POST/VOTE UPDATES:")
                #print("i")
                #UPDATE ALL THE PLAYERS IN THE GAME 
                
                #print(key, ":", value)       
                cursor.execute(f"""
                    UPDATE USERS 
                    SET balance = ROUND((balance + {value}), 2)
                    WHERE username = '{key}';
                """)
                conn.commit()
     
            elif key == "EQUITY": # UPDATING ALL THE PEOPLE WHO HOLD EQUITY
                #print("FINAL EQUITY UPDATES:")
                #print(key, value)
                #print("j")
                equity_holders_dict = GET_ALL_EQUITY_HOLDERS()
                #print()
                #print(equity_holders_dict)
                for key_, value_ in equity_holders_dict.items():
                    #print(key_, ":", float(value_))
                    name = key_
                    percent = float(value_)
                    amount = value["AMOUNT"] * (percent / 100)
                    #print(f"name:{name}")
                    #print(f"percent:%{percent}")
                    #print(f"amount:{amount}")
                    #print()
                    cursor.execute(f"""
                    UPDATE USERS 
                    SET balance = ROUND(balance + {amount}, 2)
                    WHERE username = '{name}';
                    """)
                    conn.commit()
            elif key == "SEARCH":
                #print("FINAL SEARCH UPDATES:")
                #print(key, value)
                for key__, value__ in value.items():
                    #print(f"{key__}: {value__}")
                    
                    cursor.execute(f"""
                        UPDATE USERS 
                        SET balance = ROUND(balance + {value__}, 2)
                        WHERE username = '{key__}';
                        """)
                    conn.commit()
                    
        # 2 CHANGE TYPE BACK TO 0 IF LIVE
        if not testing:
            cursor.execute(f"""
                UPDATE PAYOUTS
                SET {vote_type} = 0
                """)
            conn.commit()

        # 3 IF TYPE ==  MONTHLY, DELETE ALL SUBSCRIPTIONS
        if not testing:
            if vote_type == "Monthly":
                cursor.execute(f"""DELETE FROM SUBSCRIPTIONS_MENSURA;""" )
          
    except Exception as e:
        cursor.execute("ROLLBACK")
        log_function(e)
    conn.commit()

    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()


def GET_ALL_TYPED(my_vote_type):
    #print("GET_ALL_TYPED")
    
    conn = connection.test_connection()
        
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
                SELECT F.File_Id, F.file_path, votes.Voter_Username, votes.Date_Time
                FROM FILES as F
        
                INNER JOIN FILE_VOTES votes
                ON F.File_Id = votes.File_id

                WHERE Vote_Type = '{ my_vote_type }'

            """)
        conn.commit()

        results = cursor.fetchall()
        all_typed_datasets = []
        for value in results:
            #print(value)   
            all_typed_datasets.append(value)
        
        # BUILD FREQUENCY TABLE FOR FILE ID'S
        
        #for i in all_typed_datasets:
        # #print(i)
        
        # CLOSE CURSOR AND CONNECTION [MANDATORY]        
        cursor.close()
        conn.close()
        return all_typed_datasets
    except Exception as e:
        cursor.execute("ROLLBACK")
    #print("ERROR:  [USER_SUBSCRIBE_FULL] " + str(e))
    # CLOSE CURSOR AND CONNECTION [MANDATORY]        
    cursor.close()
    conn.close()


def UPDATE_BALANCES_TYPED(vote_type, update_dict, testing=False):
#print("2")
    #rint("\n\nupdate_dict")
    #for key_, value_ in update_dict.items():
    ##print(f"{key_}: {value_}")  
    #print(f'[UPDATE_BALANCES_TYPED]: {vote_type}')
    
    all_temp_dicts = {}
    
    FINAL_DICT = {} 
    for key, value in update_dict.items():
        #print("LKASJHGDKASHGJKAHDGKJHAGFSD", key, value)
        if key != "EQUITY" and key != "SEARCH":
            name_array = value['ORDER']            
            dataset_id_total_capital = (value['VALUE']['AMOUNT'])    
        
            # temp dict is a dictionary that goes into [NAME ARRAY] in order, and has distributed the capital
            #print(dataset_id_total_capital, name_array)
            ALGO = GET_DISTRO_ALGO_BY_FILE_ID(key)
            #print("ALGO", ALGO)
            #print(key, ALGO)
            if ALGO[0] == "EQUAL DISTRIBUTION":
                temp_dict = EQUAL_DISTRIBUTION(float(dataset_id_total_capital), name_array)
                if testing:
                    pass
                #print("EQUAL DISTRIBUTION")
                #print("error","EQUAL")
                #print("error", ( "CHECK DATA: " + str(name_array) + str(dataset_id_total_capital)))
                #print("EQU DISTRO",dataset_id_total_capital, temp_dict)
            elif ALGO[0] == "LOG DISTRIBUTION": 
                temp_dict = PURE_LOG_DISTRIBUTION(float(dataset_id_total_capital), name_array) 
                if testing:
                    pass
                    #print("PURE_LOG_DISTRIBUTION")
                #print("error","LOG")
                #print("LOG DISTRO", dataset_id_total_capital, temp_dict)
                #exit()
            elif ALGO[0] == "LOG EQUAL DISTRIBUTION":
                if testing:
                    pass
                    #print("LOG EQUAL DISTRIBUTION")
                #print("error","LOG EQUAL")
                temp_dict = SECTIONED_EQUAL_DISTRIBUTION(float(dataset_id_total_capital), name_array, float(ALGO[1]))
            else:
                 #print("error","DEFAULT")
                #print("error", name_array, dataset_id_total_capital)
                temp_dict = EQUAL_DISTRIBUTION(float(dataset_id_total_capital), name_array)
            
            all_temp_dicts[key] = {
                "ORDER":temp_dict,
                "VALUE":value,
            }
            # exit() # GENERATIONG EXCEL CHECKPOINT
            #print("error", str("TEMPT DICT: " + str(temp_dict)))
            for key_, value_ in temp_dict.items(): # THIS MAKES EVERYTHING SO MUCH SLOWER
                if key_ not in FINAL_DICT:
                    try:
                        FINAL_DICT[key_] = BROKEN_ROUNDING(float(value_))
                    except Exception as e:
                        print(e)
                        log_function("error", (str(e) + " " + str(key_) + " " + str(value_) + " " + str(temp_dict) + " " + str(ALGO[0]) + "insert"))
                else:
                    try:
                        FINAL_DICT[key_] += BROKEN_ROUNDING(float(value_))
                    except Exception as e:
                        print(e)
                        log_function("error", (str(e) + " " + str(key_) + " " + str(value_) + " " + str(temp_dict) + " " + str(ALGO[0])+ "added"))

                    #print(f"DUPE KEY={key} | ORIG={org} + {value} = NEW={FINAL_DICT[key]}")
                #print("NORMAL POST", FINAL_DICT[key_],value)
            # GRABBING THE REPLY DETAILS            
            if "REPLY" in value:
                # continue
                #print(value["REPLY"])
                name = value["REPLY"]['REPLYING_TO']
                #print("error", str("REPLY NAME: " +  str(name)))
                #print("error", str("REPLY REPLY: " +  str(value["REPLY"])))
                #print("error", str("WHOLE VALUE: " +  str(value)))
            
                if value["REPLY"]['REPLYING_TO'] not in FINAL_DICT:
                    FINAL_DICT[value["REPLY"]['REPLYING_TO']] = BROKEN_ROUNDING(float(value["REPLY"]['AMOUNT']))
                else:
                    #org = FINAL_DICT[value['REPLY']['REPLYING_TO']]                  
                    FINAL_DICT[value['REPLY']['REPLYING_TO']] += BROKEN_ROUNDING(float(value['REPLY']['AMOUNT']))
                    #print(f"DUPE KEY={value['REPLY']['REPLYING_TO']} | ORIG={org} + {value['REPLY']['AMOUNT']} = NEW={FINAL_DICT[value['REPLY']['REPLYING_TO']]}") 
                    #print(FINAL_DICT[value])
            # RATIO DETIALS
            if "RATIO" in value:
                username = str((list(value["RATIO"].keys())[0]))
            
                my_value = value["RATIO"][username]
                #print("USERNAME CHECK", username)
                #print("VALUE", my_value)
                #print(F"(RATIO) THIS SHOULD BE A POSITIVE NUMBER", my_value, type(my_value))
                if username not in FINAL_DICT:
                    FINAL_DICT[username] = BROKEN_ROUNDING(my_value)  
                    #print("CREATE", FINAL_DICT[username])
                else:
                    #print("BEFORE", FINAL_DICT[username])
                    FINAL_DICT[username] += BROKEN_ROUNDING(my_value)  
                    #print("ADD", FINAL_DICT[username])
                #print("PRINT RATIO CHANGES", FINAL_DICT[username], value)

        elif key == "EQUITY":
            # prEint("DOING ANY OF THIS?")
            equity_dict = GET_ALL_EQUITY_HOLDERS()
            FINAL_DICT[key] = {
                "AMOUNT": value,
                "EQUITY":equity_dict 
            }
            #print(F"\n\n\n\nEQUITY DICT {key}, {value}")
            #print(equity_dict)
        elif key == "SEARCH":
            #print("GOT TO EARCH FUNCTIONALITY")
            search_dict = CREATE_SEARCH_VOTE_FREQUNCY_DICT()
            total_search_equity = value
            
            dict_of_search_details = {}
            for key__, value__ in search_dict.items():
                #print("SEARCH", key__, value__)
                dollar_amount = total_search_equity * value__['PERCENTAGE']
                amount_for_creator = BROKEN_ROUNDING(dollar_amount / 2) #creator half
                dollar_amount -= amount_for_creator
                #print(dollar_amount)
                #print(amount_for_creator)
                #print(key__, value__, dollar_amount)
                # dict_of_search_details[key__] = BROKEN_ROUNDING(dollar_amount / len(value__['SEARCHERS_LIST']))
                creator = value__["SEARCH_CREATOR"]
                for i in value__["SEARCHERS_LIST"]:
                    #print("EQUATION IS: ", dollar_amount, "/", len(value__["SEARCHERS_LIST"]))
                    dict_of_search_details[i] = BROKEN_ROUNDING(dollar_amount / len(value__["SEARCHERS_LIST"]))
                    #print(i, dict_of_search_details[i])
                dict_of_search_details[creator] = amount_for_creator
                #print(amount_for_creator)
                #print("SEARCH AMOUNT FOR CREATOR", amount_for_creator)

            FINAL_DICT[key] = dict_of_search_details
            #print(dict_of_search_details)
    #print("\nFINAL DICT INFO")
    #print("GOT TO WRITING TO DIST EXCEL")
    count = 0
    #for key, value in FINAL_DICT.items():
    ##print("COUNT", count, "-", key, value, )
    #    count +=1 
    #exit(0)
    for key, value in FINAL_DICT.items():
        if key == "EQUITY":
            log_string = str("MANSURA") + ":" + str((value))
        elif key =="SEARCH":
            log_string = str("SEARCH-TEMP") + ":" + str((value))
        else:
            log_string = str(key) + ":" + str(BROKEN_ROUNDING(value))
            log_function(msg_type="distro", log_string=log_string, vote_type=vote_type, distro_type="final")
        
        if type(value) is not dict:
            num = BROKEN_ROUNDING(value)
            temp_array_ = [key, num]
            #print(temp_array_)
            my_time = pytz.timezone('US/Eastern') 
            current_datetime = datetime.now(my_time).replace(microsecond=0).replace(tzinfo=None)
            current_date = current_datetime.strftime('%Y-%m-%d')

            with open(f'/root/mansura/Python/HISTORY/{vote_type}/{current_date}-dist.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow(temp_array_)

            #print(value)
            # IMPORTANT PRINT
            #print(f'{key}                :{num }'.rjust(38))
    #print(FINAL_DICT)
    
    equity_dict_current = GET_ALL_EQUITY_HOLDERS()
    WRITE_HEADERS_TO_EXCEL(
        equity_dict=equity_dict_current, 
        vote_type=vote_type, 
        equity_total=update_dict["EQUITY"],
        search_dict=update_dict["SEARCH"],
        all_temp_dicts=all_temp_dicts,
        testing=testing
    )
    # exit()

    UPDATE_BALANCE_FROM_FINAL_DICT(FINAL_DICT, vote_type, testing)


def read_date_from_csv():
    import csv
    with open('Python/current_date.csv') as csvfile:
        reader = csv.reader(csvfile)
        
        date = []
        for row in reader:
            date = row
            #print(row)
            if len(row) > 0:
                return row[0] # ALWAYS FIRST ROW OF CSV
            else: return []


def write_date_to_csv(date):
    import csv
    with open('Python/current_date.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(date)


def append_log_to_csv(string):
    import csv
    with open('Python/all_dates.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(string)


def TESTING_TIMING():    
    # START AT THE TOP OF THE HOUR, I COULD PROBABLY WRITE CODE TO GET IT PERFECT
#print_title("\nCREATING THREAD FOR TIME TESTING")
    
    from apscheduler.schedulers.background import BackgroundScheduler

    scheduler = BackgroundScheduler()
    scheduler.add_job(CHECK_TIME_EQUIVALENCE_AND_EXECUTE, 'interval', seconds=120)
    scheduler.start()


def CHECK_TIME_EQUIVALENCE_AND_EXECUTE():   
    #print("CHECK_TIME_EQUIVALENCE_AND_EXECUTE")
    conn = connection.test_connection()
    my_time = pytz.timezone('US/Eastern') 
    
    current_datetime = datetime.now(my_time).replace(microsecond=0).replace(tzinfo=None)
    #print(current_datetime)
    # exit(0)

    previous_datetime = read_date_from_csv()
    if previous_datetime == []:
        pass
    #print("First Iter empty")
    else:
        previous_datetime = datetime.strptime(previous_datetime, '%Y-%m-%d %H:%M:%S') # equivalent to a cast
        
        # current_data = my_datetime.strftime("%d/%m/%Y %H:%M:%S")
        
        #print("CURRENT :",current_datetime)
        #print("PREVIOUS:",previous_datetime)
        # CHECK DAY
        if current_datetime.strftime("%d") != previous_datetime.strftime("%d"):
            append_log_to_csv(["DAY CHANGED"])
            FUNCTION_LOG_VOTER_DICT_WITH_FILE_ID_DICT("Daily")
        # CHECK MONTH
        if current_datetime.strftime("%m") != previous_datetime.strftime("%m"):
            append_log_to_csv(["MONTH CHANGED"])
            FUNCTION_LOG_VOTER_DICT_WITH_FILE_ID_DICT("Monthly")
        # CHECK YEAR
        if current_datetime.strftime("%Y") != previous_datetime.strftime("%Y"):
            append_log_to_csv(["YEAR CHANGED"])
            FUNCTION_LOG_VOTER_DICT_WITH_FILE_ID_DICT("Yearly")
        

        # TESTS
        #if current_datetime.strftime("%M") != previous_datetime.strftime("%M"):
        ##print("MINUTE CHANGED")
        #if current_datetime.strftime("%H") != previous_datetime.strftime("%H"):
        ##print("HOUR CHANGED: ", current_datetime.strftime('%Y-%m-%d %H:%M:%S'))
        
        append_log_to_csv([current_datetime.strftime("CURRENT  : %Y-%m-%d %H:%M:%S")])
        append_log_to_csv([previous_datetime.strftime("PREVIOUS : %Y-%m-%d %H:%M:%S")])

    write_date_to_csv([current_datetime])


    
    # IF DATA.DAY > READ(CSV.DAY)
    # IF DATA.MONTH > READ(CSV.MONTH)
    # IF DATA.YEAR > READ*CSV.YEAR)


    #print(data)


def DISTRIBUTION_GET_NUM_FILE_VOTES_FOR_TYPE_TOTAL(file_id, my_vote_type):
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


def CHECK_FOR_HIGHEST_RATIO(file_id_key, vote_type):
    #print("GOT TO RATIO FUNCTION")
    conn = connection.test_connection()
    cursor = conn.cursor()
    # GET ALL POSTS WITH THIS AS A POTENTIAL REPLY
    cursor.execute(f"""
        SELECT File_id 
        FROM FILES files
        WHERE files.Post_foreign_id_source = '{file_id_key}'
    """)
    posts_replying_to_original = []
    for i in cursor.fetchall():
        posts_replying_to_original.append([i][0][0]) #TI FEEL LIKE THIS IS GOING TO CAUSE PROBLEMS
        #print("POST_ID", i[0])

    post_array_vote_count = {}

    # #TODO:GET ALL VOTES FOR EACH FILE ID
    for i in posts_replying_to_original:
        #print(i)
        post_array_vote_count[f"{i}"] = (DISTRIBUTION_GET_NUM_FILE_VOTES_FOR_TYPE_TOTAL(i, vote_type))
    
    #print(F"REFERENCING FILE [{file_id_key}]")
    MAIN_vote_count = DISTRIBUTION_GET_NUM_FILE_VOTES_FOR_TYPE_TOTAL(file_id_key, vote_type)
    ratio_dict = {}
    for key, value in post_array_vote_count.items():
        #print(f"{key}: {value}")
        if int(value) > MAIN_vote_count:
            #print(f"{value} > {MAIN_vote_count}, poster got RATIO'D BOZO")
            ratio_dict[key] = value
        else:
            pass
        
    cursor.close()
    conn.close()

    if not ratio_dict:# CHECK IF THERE IS A RATIO AT ALL
        #print("Dict is Empty")
        return "None"
    else:
        max_value = max(ratio_dict, key=ratio_dict.get)
        #print(f"HIGHEST RATIO FILE ID IS: ",max_value)
        return max_value
    

    ## GET ALL FILES RESPONDING
    #except Exception as e:       
    ##print(e)
    

def GET_ALL_EQUITY_HOLDERS():
    #print("EXECUTED THIS FUNCTION")
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT username, percentage
        FROM EQUITY
    """)
    equity_dict = {}
    for i in cursor.fetchall():
        equity_dict[i[0]] = i[1]
        #print(i)
    
    #for key,value  in equity_dict.items():
    ##print("GET_ALL_EQUITY_HOLDERS()" ,key, ":", value)

    return equity_dict


def RUN_WITH_TIME_TEST():
    #TODO: RUN THE FUNCTION AND ACTUALLY FINISH THE UPDATE EXECUTION
    #TODO: ANALYTICS ON WHAT PERCENT OF PEOPLE CAME OUT WITH LOWER THAN X DOLLARS AND SO ON
    #TODO: SHOW IT IN TERMS OF A GUASSIAN DISTRIBUTION
    #TODO: CHECK IF SORT IS POSSIBLE sorted(d.items(), key=lambda x: x[1])
    import time

    # get the start time
    st = time.time()

    FUNCTION_LOG_VOTER_DICT_WITH_FILE_ID_DICT("Daily", testing=False)
    #FUNCTION_LOG_VOTER_DICT_WITH_FILE_ID_DICT("Monthly")
    
    # FUNCTION_LOG_VOTER_DICT_WITH_FILE_ID_DICT("Yearly", testing=True)
        
    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
#print('Execution time:', elapsed_time, 'seconds')


def RESULT_ANALYSIS():
    #TODO: CUSTOM DATE
    total = 0
    rows = 0 
    greater_than_1 = 0
    greater_than_2 = 0
    greater_than_3 = 0
    greater_than_4 = 0
    greater_than_5 = 0
    greater_than_6 = 0
    greater_than_7 = 0
    greater_than_8 = 0
    greater_than_9 = 0
    greater_than_10 = 0
    with open('/root/mansura/Python/HISTORY/Monthly/2022-11-06-dist.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',',)
        for row in reader:
            total += float(row[1])
            rows +=1
        #print(float(row[1]))
            
            if float(row[1]) >= 1:
                greater_than_1 +=1
            if float(row[1]) >= 2:
                greater_than_2 +=1
            if float(row[1]) >= 3:
                greater_than_3 +=1
            if float(row[1]) >= 4:
                greater_than_4 +=1    
            if float(row[1]) >= 5:
                greater_than_5 +=1
            if float(row[1]) >= 6:
                greater_than_6 +=1
            if float(row[1]) >= 7:
                greater_than_7 +=1
            if float(row[1]) >= 8:
                greater_than_8 +=1
            if float(row[1]) >= 9:
                greater_than_9 +=1
            if float(row[1]) >= 10:
                greater_than_10 +=1    

#print("TOTAL      :",total)
#print("VOTERS     :",rows)
#print("GREATER 1  : %", (greater_than_1) / rows)
#print("GREATER 2  : %", (greater_than_2) / rows)
#print("GREATER 3  : %", (greater_than_3) / rows)
#print("GREATER 4  : %", (greater_than_4) / rows)
#print("GREATER 5  : %", (greater_than_5) / rows)
#print("GREATER 6  : %", (greater_than_6) / rows)
#print("GREATER 7  : %", (greater_than_7) / rows)
#print("GREATER 8  : %", (greater_than_8) / rows)
#print("GREATER 9  : %", (greater_than_9) / rows)
#print("GREATER 10 : %", (greater_than_10) / rows)


def GET_USERNAME_BY_FILE_ID(file_id):
        
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT u.username
        FROM USERS u

        INNER JOIN FILES f
        ON f.uploader = u.username

        WHERE f.File_Id = {file_id}
    """)

    for i in cursor.fetchall():
        #print(i[0])
        return i[0]
        cursor.close()
        conn.close()
    else:
    #print("no user with file :", file_id)
        cursor.close()
        conn.close()
        return "None"


def PURE_LOG_DISTRIBUTION(TOTAL, my_array):
    
    new_dict = {}
    num_members = len(my_array)

    if len(my_array) == 1: #SINGLE ELEMENT
        new_dict[TOTAL] = my_array[0]
        #print("[PURE_LOG_DISTRIBUTION] SINGLE ITEM :", new_dict)
        return new_dict

    for i in range(num_members):      
        temp_holder = TOTAL / (2 ** (i+1))
        if temp_holder < 0.01:
            break # PROBABLY NOT WORTH HAVING THE ZEROES, PROBABLY WILLC REATE BUGS
            # new_dict[my_array[i]] = 0.0

            # break #this breaks the whole loop and stops giving out money, I could just have the rest be zeroes instead
        else:
            if my_array[i] not in new_dict: # IF NEW KEY
                new_dict[my_array[i]] = temp_holder  
            else:
                new_dict[my_array[i]] += temp_holder # add dupe value to value already inside
    
    current_total = 0
    for key, value in new_dict.items():
        current_total += value

    extra_amount = BROKEN_ROUNDING(TOTAL - current_total)
    
    j = 0 
    for key, value in new_dict.items():
        extra_dist = extra_amount / num_members
        #print(j, key, value, extra_dist)
        new_dict[key] = BROKEN_ROUNDING(new_dict[key] + extra_dist)
        j+=1    

    current_total_after_redo = 0
    for key, value in new_dict.items():
        current_total_after_redo += value

    # FOR TESTING PURPOSES
    #print("PURE_LOG_DISTRIBUTION\nENTERED TOTAL:", TOTAL)
    #print("EXTRA   TOTAL:", current_total)
    #print("UPDATED TOTAL:", "{:.2f}\n".format(current_total_after_redo))
    #print("MINE :", new_dict)
    return new_dict


def BROKEN_ROUNDING(my_float):
    #USE EXTREMELY CAUTIOUSLY
    
    string_float = str(my_float) # THE FLOAT CONVERSION IS TO MAKE SURE THEY ALL HAVE DECIMAL POINTS
    before_dec = string_float.split(".")[0]
    after_dec = string_float.split(".")[1]
    after_dec = after_dec[:2]
    return float(before_dec + "." + after_dec)


def EQUAL_DISTRIBUTION(TOTAL, my_array):
    array_length = len(my_array)
    each = BROKEN_ROUNDING(TOTAL / array_length)
    new_dict = {}
    for i in range(len(my_array)):
        #print(my_array[i])
        new_dict[my_array[i]] = BROKEN_ROUNDING(each)
    
    new_sum = 0
    for key, value in new_dict.items():
        #print(key, value)
        new_sum  += value
    TOTAL = BROKEN_ROUNDING(TOTAL) #TODO:THERE ARE PLACES WHERE PYTHONS DEFAULT ROUNDING WILL GO TERRIBLY WRONG
    new_sum = BROKEN_ROUNDING(new_sum)
    #print("TOTAL", TOTAL)
    #print("new_sum", new_sum)
    EXTRA_CAPITAL = TOTAL - new_sum
    #print(EXTRA_CAPITAL)
    #exit(0)
    each_second = BROKEN_ROUNDING(EXTRA_CAPITAL / array_length)
    for i in range(len(my_array)):
        #print(my_array[i])
        new_dict[my_array[i]] += BROKEN_ROUNDING(each_second)
    
    # CHECK AT THE END
    new_sum = 0
    for key, value in new_dict.items():
        #print("OG", key, value)
        new_dict[key] = BROKEN_ROUNDING(value)
        #print("CH", new_dict[key], BROKEN_ROUNDING(value))
        new_sum  += value

    #print(F"TOTAL : {TOTAL}")
    #print(F"EACH  : {each}")
    #print(F"RE-SUM: {round(new_sum, 2)}")
    #for key, value in new_dict.items():
    #print(key, value)
    return new_dict


def SECTIONED_EQUAL_DISTRIBUTION(TOTAL, my_array, sections=2):
    """
    NOTES: 1. i do not know why this is the case, but BUT SECTIONS HAVE TO  BE BELOW 195, or I got weired bugs with the totals
           2. I know there will be anomalies here so I wrapped it in a try catch, and just run the easier equal distribution anyway then log the error
    """

    try:
        if sections == 1:
            return EQUAL_DISTRIBUTION(TOTAL, my_array)
        
        my_arrays = np.array_split(my_array, sections)

        array_of_initial_amounts = 0
        ordered_temp_array = []
        for i in range(sections):
            temp_holder = TOTAL / (2 ** (i+1))
            if temp_holder < 0.01:
                break

            array_of_initial_amounts += temp_holder
            ordered_temp_array.append(temp_holder)
        
        amount_left = TOTAL - array_of_initial_amounts
        amount_left = BROKEN_ROUNDING(amount_left) 
        dict_of_nums_arrays = {}
        for i in range(len(ordered_temp_array)):
            dict_of_nums_arrays[ordered_temp_array[i]] = my_arrays[i]

        each_second = BROKEN_ROUNDING(amount_left / len(my_arrays))

        keys_list = list(dict_of_nums_arrays.keys())
        for i in range(len(keys_list)):
            keys_list[i] = BROKEN_ROUNDING(keys_list[i] + each_second)

        
        dict_for_equal = {}
        counter = 0
        for key,value in dict_of_nums_arrays.items():
            dict_for_equal[keys_list[counter]] = value
            counter += 1
        
        second_counter_check = 0
        FINAL_DICT = {}
        for key, value in dict_for_equal.items():
            #print(f"{key}: {value}")
            second_counter_check += key
            single_for_each = key / len(value)
            for i in value:
                #print(i)
                if i in FINAL_DICT:
                    FINAL_DICT[i] += BROKEN_ROUNDING(single_for_each)
                else:
                    FINAL_DICT[i] = BROKEN_ROUNDING(single_for_each)
        #for key,value in FINAL_DICT.items():
        ##print(key, value)
                
        return FINAL_DICT
    except Exception as e:
        print("DISTRO ERROR, DOING EQUALITY", e)
        # THERE WAS SOME KIND OF ERROR SO JUST DO EQUALITY
    #print("error", e)
        return EQUAL_DISTRIBUTION(TOTAL, my_array)
    # return new_dict


def GET_FILE_PATH_BY_ID(file_id):
    conn = connection.test_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT File_PATH
        FROM FILES 
        WHERE File_id = '{file_id}'
    """)
    path = ""
    for i in cursor.fetchall():
        path = i[0]

    cursor.close()
    conn.close()
    return path


def GET_DISTRO_ALGO_BY_FILE_ID(file_id):
    
    #print(F"FILE ID: {file_id}")
    path = GET_FILE_PATH_BY_ID(file_id)
    username = path.split("-")[0]
    #"/root/mansura/static"
    full_path = f"/root/mansura/static/#UserData/{username}/files/{path}/post_config.json"
    
    #full_path = f"../static/#UserData/{username}/files/{path}/post_config.json"
    full_path = f"/root/mansura/static/#UserData/{username}/files/{path}/post_config.json"
    f = open(f'{full_path}')
    data = json.load(f)
    distro_details = data["distro_details"]
    #print(path)
    #print(username)
    #print(distro_details)
    return distro_details



    #f = open(f'{my_path}/post_config.json')
    #data = json.load(f)
    #distro_details = data["distro_details"]
    #print("DISTRO DETAILS:", distro_details)
    #return ""


#============================search related
def CREATE_SEARCH_VOTE_FREQUNCY_DICT():
    array_of_searches = GET_ALL_SEARCH_VOTES()
    search_vote_freq_dict = {}
    for i in array_of_searches:
        #print(i)
        if i[1] in search_vote_freq_dict:
            # WHAT I NEED TO DO NEXT IS ATTACH ALL THE PEOPLE WHO VOTED FOR THIS DATASET IN AN ARRAY
            search_vote_freq_dict[i[1]]['AMOUNT'] +=1
            search_vote_freq_dict[i[1]]['SEARCHERS_LIST'].append(i[2])
        else:
            search_creator = GET_CREATOR_OF_SEARCH_ALGO_BY_SEARCH_ID(i[1])
            search_vote_freq_dict[i[1]] = {"AMOUNT": 1, 'SEARCHERS_LIST': [i[2]], 'SEARCH_CREATOR': search_creator}
    
    TOTAL_NUM_SEARCH_VOTES = GET_NUM_SEARCH_VOTES()
    for key, value in search_vote_freq_dict.items():
        percentage = BROKEN_ROUNDING(value['AMOUNT'] / TOTAL_NUM_SEARCH_VOTES)
        value['PERCENTAGE'] = percentage

    #for key, value in search_vote_freq_dict.items():
    ##print(key, value)
    
    return search_vote_freq_dict


def GET_ALL_SEARCH_VOTES():
    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT Search_Vote_Id, Search_id, Voter_Username
    FROM SEARCH_VOTES
    
    """
    )
    vote_list = []
    for i in cursor.fetchall():
        #print(i)
        vote_id = i[0]
        search_algo_id = i[1]
        voter_name = i[2]   
        vote_list.append([vote_id,search_algo_id,voter_name])     
    return vote_list


def GET_CREATOR_OF_SEARCH_ALGO_BY_SEARCH_ID(search_id):
    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT Username
        FROM SEARCH_ALGORITHMS
        WHERE Search_id = {search_id}
    """
    )
    
    username = ""
    for i in cursor.fetchall():
        username = i[0]
    return username


def GET_NUM_SEARCH_VOTES():
    conn = connection.test_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT COUNT(*) 
    FROM SEARCH_VOTES
    """
    )
    count = 0 
    for i in cursor.fetchall():
        count = i[0]
    #print("TOTAL NUM VOTES", count)
    return count
#============================search related

# GET_DISTRO_ALGO_BY_FILE_ID(1)
# PURE_LOG_DISTRIBUTION(100.00, test_ordered_array)
# EQUAL_DISTRIBUTION(100.00, test_ordered_array)
# SECTIONED_EQUAL_DISTRIBUTION(19.91, test_ordered_array, sections=2)RUN_WITH_TIME_TEST()
#print(EQUAL_DISTRIBUTION(2.59, ['Valen', 'Rayne', 'Philippa', 'Lindsee', 'Tel', 'Phuoc', 'Kameka']))
# RUN_WITH_TIME_TEST()