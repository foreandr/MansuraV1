# TODO:
#  NEED A DEBUG VERSION
#  NEED A TESTNET/PBE VERSION

# LIBRARIES 
from waitress import serve
import flask
import os


from flask import Flask, render_template, request, session, redirect, url_for, g, send_from_directory, Response
from psycopg2 import connect
import requests
import Python.database as database
import Python.db_connection as connector
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.datastructures import FileStorage
import os
from PIL import Image
from threading import Thread
import logging
import sys
import urllib.parse
import requests
import datetime
from datetime import datetime
from csv import writer

# CUSTOM CODE
import Python.helpers as helpers
from Python import my_email
import Python.distribution_algorithm as distribution_algorithm

TEMPLATE_DIR = os.path.abspath('./Templates')
STATIC_DIR = os.path.abspath('./static')
# import sql_functions

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = 'demokey'
# user = sql_functions.check_users() #list of user in DB

app.config["FILE UPLOADS"] = "static/#UserData"

@app.route('/', methods=['GET', 'POST'])  # homepage
def home():
    print('EXECUTING INDEX FUNCTION')
    if "user" in session.keys():
        session_username = session["user"]
    else:
        session_username = ""
    
    #print(request.url) # TO SEE WHATS GOIN ON
    #print(request.body)
    #print(request.headers)

    print("SESSION USERNAME IS:", session_username)
    
    # PAGE NUMBER CHECK FOR GETTING NEW INFO
    if request.method == 'POST':
        page_no = request.form.get("page_number")
        if page_no == "None" or page_no == None:
            page_no = 1
        more_left = database.CHECK_FILES_NOT_OVER_LIMIT(int(page_no)+1) ##CHECK IF THE NEXT ONE WOULD BREAK THINGS
        # print("THERE IS STILL ROOM TO SCROLL", more_left)
        if more_left:
            page_no = int(page_no) + 1
        else:
            page_no = page_no

        print(page_no)
    else:
        page_no = 1
   
    file_ids_list, usernames_list, paths_list, dates_list, post_sources_list, daily_left, monthly_left, yearly_left, day_votes, month_votes, year_votes, user_balance, dailypool, monthlypool, yearlypool, daily_votes_singular,  monthly_votes_singular, yearly_votes_singular = database.universal_dataset_function(search_type="home", search_algo_path="foreandr-1", page_no=page_no, search_user=session_username)
    # GRAB STUFF IT'S IT'S EMPTY EITHE RWAY
    if len(file_ids_list) == 0:
        balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session_username)
    
    username_len = len(usernames_list)
    # print("USERNAMES LEN", username_len, usernames_list)

    text_list = []
    age_18_list = []
    source_list = []
    image_path_list = []
    for i in range(len(usernames_list)):
        # print(usernames_list[i], paths_list[i])
        my_path = f"static/#UserData/{usernames_list[i]}/files/{paths_list[i]}"
        post_text, post_age_18, post_sources, post_image_path = helpers.get_postinfo_from_path(my_path)
        age_18_list.insert(i, post_age_18)
        source_list.insert(i, post_sources)
        text_list.insert(i, post_text)
        image_path_list.insert(i, post_image_path)

                #age_18 = f.read()
                #print(f)
        #print("")
    
    #print(len(text_list), " - ", text_list)
    #print(len(age_18_list), " - ", age_18_list)
    #print(len(source_list), " - ", source_list)
    #print(len(image_path_list), " - ", image_path_list)
    # print("FILENAMES: ", filenames)
    lengths_of_text_files = []
    for i in text_list:
        lengths_of_text_files.append(len(i))

    return render_template('index.html',
                           message="index.html page",
                           usernames_list=usernames_list,
                           file_ids_list=file_ids_list,
                           session_username=session_username,
                           username_len=username_len,
                           
                           paths_list=paths_list,
                           dates_list=dates_list,
                           post_sources_list=post_sources_list,
                           
                           day_votes=day_votes,
                           month_votes=month_votes,
                           year_votes=year_votes,
                           
                           dailypool = dailypool,
                           monthlypool = monthlypool,
                           yearlypool = yearlypool,
                           
                           daily_left = daily_left,
                           monthly_left = monthly_left,
                           yearly_left = yearly_left,
                           user_balance = user_balance,
                           
                           text_list=text_list,
                           lengths_of_text_files=lengths_of_text_files,
                           age_18_list=age_18_list,
                           source_list=source_list,
                           image_path_list=image_path_list,
                           page_no=page_no

                           )


@app.route('/register', methods=['GET', 'POST'])
def register():
    print('EXECUTING REGISTER FUNCTION')
    if "email" in session:
        return redirect(url_for("user_profile"))
    if request.method == 'GET':
        sign_up_message = 'Please sign up'
        return render_template('register.html', message=sign_up_message)

    if request.method == 'POST':
        my_dict = request.form.to_dict(flat=False)
        try:  # DO NOT EXECUTE UNTIL SUBMIT IS CLICKED
            registering_username = my_dict['username']
            password = my_dict['password']
            email = my_dict['email']
            paypal_email =my_dict['paypal_email']

            # CHECK WHETHER VALUES ARE IN RESTRICTED LIST
            
            has_bad_words = helpers.USERNAME_PROFANITY_CHECK(registering_username[0])

            if not has_bad_words:

                print(registering_username, "is registering their account!")
                # print(password)

                # database.create_user(conn=connection, username="hello", password="password", email="bce@hotmail.com")
                database.full_register(username=registering_username[0], password=password[0],email=email[0], paypal_email=paypal_email[0] , balance=0)

                # GO TO THEIR PROFILE
                return redirect(url_for('login'))

            else:
                return render_template('register.html', 
                return_message="YOU HAD SOME BAD WORDS YOU SHOULDNT HAVE IN YOUR USERNAMER"
                )

        except Exception as e:
            print("Error on HTML POST Register", e)
        return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    print('EXECUTING LOGIN FUNCTION')
    if "email" in session:
        email = session["email"]  # getting user info from session variable
        return redirect(url_for("user_profile"))
    if request.method == 'GET':
        login_message = 'Please LOGIN'
        if "email" in session:
            return redirect(url_for("user_profile"))
        return render_template('login.html', message=login_message)
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        signed_in = database.validate_user_from_session(email, password)

        if signed_in[0]:
            session["id"] = signed_in[1]
            session["user"] = signed_in[2]
            session["email"] = email
            #session["password"] = password
            print('SESSION INFO: ', session)
            return redirect(url_for("user_profile"))
        else:
            return render_template('login.html', message="wrong email or password, try again")


@app.route('/logout', methods=['GET'])
def logout():
    session.pop("email", None)  # remove data from session
    session.pop("user", None)  # remove data from session
    session.pop("password", None)  # remove data from session
    return redirect(url_for("login"))


@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    print('USING USER PROFILE')
    # print(request)
    if "email" not in session:
        return redirect(url_for('login'))
    elif request.method == "GET":
        print('USING USER PROFILE - GET')
        print(session)
        # return redirect(url_for("user_profile"))
        return redirect(url_for('user_profile_name', username=session['user']))

        # return render_template(f"user_profiles/{session['user']}.html", friends=my_friends,account_name=session['user'])

    elif request.method == "POST":

        #password = session["password"]  # DON'T NEED?
        #email = session["email"]  # DON'T NEED?
        user = session["user"]
        id = session["id"]

        # print("ID:", id)
        # print("USERNAME:", user)
        # print("PASSWORD:", password)
        # print("EMAIL   :", email)
        # print("-------")
        if request.files:
            file = request.files['file']  # because name in HTML FORM is file
            my_description = ""  # only here because needs to be global
            my_file_size = 0
            # print(request.headers)

            # print(file)
            # print(app.config["FILE UPLOADS"])
            # print(file.filename)
            my_path_with_file = ""
            # print("FILE", file.content_type, type(file.content_type))
            if file.content_type == "text/csv":  # if it's a csv file, store it at the user location
                my_path_with_file = f"{app.config['FILE UPLOADS']}/{user}/csv_files/{file.filename}"
                file.save(my_path_with_file)

                my_description = request.form["description"]
                my_file_size = request.form["hidden_file_size"]

            elif file.content_type == "image/jpeg" or file.content_type == "image/png":
                my_path_with_file = f"{app.config['FILE UPLOADS']}/{user}/profile/profile_pic.jpg"  # overriding file type
                file.save(my_path_with_file)

            # print("MY PATH:", my_path)
            print("MY PATH W/F:", my_path_with_file)
            '''
            database.FILE_INSERT(
                connection,
                file_path=my_path_with_file,
                description=my_description,
                user_id=id,
                file_size=my_file_size
            )
            '''
            print("OUT OF CHECKING FILETYPE-------")
            print("Saved and completed")
        # return redirect(url_for("user_profile", message="hi")) # THIS APPEARS IN THE ADDRESS BAR AS A QUERY
        return redirect(url_for("user_profile"))
    

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if "email" not in session:
        return redirect(url_for('login'))

    if request.method == "POST": # UPLOADING SOMETHING
        print("GOT TO WHETHER SOMETHING IS BEING POISTED OR NOT ==================================")
        post_text = request.form.get("textbox")
        post_file = request.files['file']
        plus_18 =  request.form.get("older_18")
        forign_id_source = request.form.get("external_source")
        external_link = request.form.get("external_source_link")
        
        print("UPLOAD DETAILS ==============================")
        print("UPLOADER: " + str(session['user']))
        print("POST TEXT: " + str(post_text))        
        print("POST FILE: " + str(post_file))
        print("POST LINK: " + str(external_link))
        print("POST FOID: " + str(forign_id_source))
        print("POST 18+ : " + str(plus_18))
        # print("POST SIZE: " + str(file_length))
        print("=============================================")
        
        print(len(post_file.filename), post_file.filename)
        if ( (len(post_text) == 0) and (len(post_file.filename) == 0)): 
            print("EMPTY HERE")
            #print("post text:", post_text, type(post_text), len(post_text))
            #print("filename:", post_file.filename, type(post_file.filename), len(post_file.filename))
            return redirect(url_for("home"))
            
        database.FILE_INSERT( uploader=session["user"], uploaderId=database.GET_USER_ID(session["user"]), size="10", post_foreign_id_source=forign_id_source, 
                file_path="N-A", post_file=post_file, 
                post_text=post_text, age_18=plus_18, 
                external_link=external_link
                )
        #TODO: THIS SHOULD REDIRECT TO THE PAGE OF THE POST 
        return redirect(url_for("home"))
    else:
        #TODO: THIS SHOULD REDIRECT TO INDEX.HTML        
        return redirect(url_for("home"))


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if "email" not in session:
        return redirect(url_for('login'))
    #TODO: THIS WORKS BUT IT'S ALL KIND OF BUGGY
    print("inside of subscribe!!!!") 
    #TODO:COULD BE MADE INTO ONE FUNCTION TO SIMPLIFY
 
    if "email" not in session: #TODO:PROBABLY CAN ERASE THIS SINCE THERE IS A CHECK AT THE TOP
        return redirect(url_for('login'))
    else:
        print("REQUEST", request)
        print("THERE WAS AN ERROR, MAYBE A GET REQUESt?")
        return render_template(f"subscribe.html", 
                                       session_user = session["user"],
                                       daily_votes_left=daily_votes_left,
                                       monthly_votes_left=monthly_votes_left,
                                       yearly_votes_left=yearly_votes_left,
                                       balance = balance

                                       )


@app.route('/<username>', methods=['GET', 'POST'])
def user_profile_name(username):
    print('EXECUTING WITH ARGUMENT: ', username)
    if "email" not in session:
        return redirect(url_for('login'))
    if username == "favicon.ico": # check weird username issue
        print("FAVICON ISSUE")
        return redirect(url_for('home'))
    """
    if request.method == "POST":
        print("USERNAME POSTING")
    """
    # CHECK USER INFO
    if username == session['user']: # Check some user info
        is_session_user = True  
        is_following = False
    else:
        is_session_user = False
        is_following = database.CHECK_IF_ALREADY_FOLLOWING(session['user'], username)

    #   CHECK WHICH ONE OF THE OTHERS IT UIS
    #=======================================================
    if username.endswith('-post_page'): # CHECK IF GOING TO A PARTICULAR POST
        if "email" in session:
            balance = database.GET_USER_BALANCE_SIMPLE( session["user"])
        else:
            balance = 0

        # print("\nTHIS SHOWS ITS GETTING TO INDIVIDUAL FILE========================")
        
        list_from_username = username.split("_")

        new_username = list_from_username[0]
        filename = list_from_username[1].split("_page") # something going on weird here that is making me do the split twice
        new_filename = filename[0].split("-post")
        final_filename = new_filename[0]
        file_id = final_filename.split("-")[1]
        num_replies = database.GET_NUM_REPLIES(file_id)
        reply_array = database.GET_ALL_REPLIES(file_id)
        post_username, post_file_path, post_user_id, post_foreign_id_source, post_date, file_id_ = database.GET_SINGLE_DATASET_INFO(final_filename)
            
        file_ids_list, usernames_list, paths_list, dates_list, post_sources_list, daily_left, monthly_left, yearly_left, day_votes, month_votes, year_votes, user_balance, dailypool, monthlypool, yearlypool, daily_votes_singular,  monthly_votes_singular, yearly_votes_singular = database.universal_dataset_function(search_type="post", search_algo_path="foreandr-1", page_no="1", search_user=session['user'], file_id=file_id)
        #MIGHT BE WRTH CONSOLIDATIING INTO ONE FUNCTION
        if len(file_ids_list) == 0:
            user_balance, daily_left, monthly_left, yearly_left, dailypool, monthlypool, yearlypool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session['user']) # THIS ASSUMES ALREADY IN SESSION, SHOULD BE

        text_list = []
        age_18_list = []
        source_list = []
        image_path_list = []
        usernames_list = []
        paths_list = []

        for i in range(len(reply_array)):
            #print(i)
            #print(i[1])
            usernames_list.append(reply_array[i][0])
            paths_list.append(reply_array[i][1])
            my_path = f"static/#UserData/{reply_array[i][0]}/files/{reply_array[i][1]}"
            # print("PATH    :", my_path)
            
            post_text, post_age_18, post_sources, post_image_path = helpers.get_postinfo_from_path(my_path)
            age_18_list.insert(i, post_age_18)
            source_list.insert(i, post_sources)
            text_list.insert(i, post_text)
            image_path_list.insert(i, post_image_path)
        
        my_og_path = f"static/#UserData/{new_username}/files/{post_file_path}"
        og_post_text, og_post_18, og_post_src, og_post_img   = helpers.get_postinfo_from_path(my_og_path)

        # GET LENGTHS OF TEXT
        lengths_of_text_files = []
        for i in text_list:
            lengths_of_text_files.append(len(i))
            # print(i, len(i))
        '''
        print("=====================DETAILS=======================")
        print("DATES LIST:", dates_list)
        print("RAW NAME :", username)
        print("USERNAME :", new_username)
        print("FILENAME :", final_filename)
        print("FILE  ID :", file_id)
        print("NUM REPL :", num_replies)
        # print("ARR REPL:", reply_array)        
        print("POST USER:", post_username)
        print("POST PATH:",post_file_path)
        print("POST U ID:",post_user_id)
        print("POST F ID:",post_foreign_id_source)
        print("POST DATE:",post_date)
        
        print("POST DATE:",og_post_text)
        print("IMG PATH :",og_post_img)
        print("POST SORC:",og_post_src)
        print("POST OV18:",og_post_18)
        '''
        return render_template('post_details.html',
                            # POST DETAILS

                            len_text=len(og_post_text),
                            og_post_text=og_post_text,
                            og_post_img=og_post_img ,
                            og_post_src=og_post_src,
                            og_post_18=og_post_18,

                            test_message="post_details.html page",
                            lengths_of_text_files=lengths_of_text_files,
                            text_list=text_list,
                            age_18_list=age_18_list,
                            source_list=source_list,
                            image_path_list=image_path_list,
                            username_len=len(usernames_list),
                            username=new_username,
                            final_filename=final_filename,
                            file_id=file_id,
                            num_replies=num_replies,
                            post_user_id=post_user_id,
                            post_foreign_id_source=post_foreign_id_source,
                            post_date=post_date,
                            reply_array=reply_array,

                            file_ids_list=file_ids_list,
                            usernames_list=usernames_list,
                            paths_list=paths_list,
                            dates_list=dates_list,
                            post_sources_list=post_sources_list,

                            daily_left=daily_left,
                            monthly_left=monthly_left,
                            yearly_left=yearly_left,
                            
                            day_votes=day_votes,
                            month_votes=month_votes,
                            year_votes=year_votes,

                            daily_pool=dailypool,
                            monthly_pool=monthlypool,
                            yearly_pool=yearlypool,
                            user_balance=user_balance,

                            daily_dataset_votes=daily_votes_singular,
                            monthly_dataset_votes=monthly_votes_singular,
                            yearly_dataset_votes=yearly_votes_singular
                        )        
    else:
        # print(username, "does not end with -post_page")
        pass
    if database.CHECK_IF_NAME_EXISTS(username) == False:
        print("NAME DOESNT EXIST")
        return redirect(url_for('home'))             
    if username == 'upload':
        print("THIS SHOWS ITS GETTING TO UPLOAD")
        return redirect(url_for('upload'))
    if username == 'subscribe':
        print("THIS SHOWS ITS GETTING TO SUBSCRIBE")
        return redirect(url_for('subscribe'))
    if username == "add_funds":
        print("THIS SHOWS ITS GETTING TO ADD FUNDS")
        return redirect(url_for('add_funds'))
    if username == "paypalsuccess":
        print("THIS SHOWS ITS GETTING TO paypalsuccess")
        return redirect(url_for('paypalsuccess'))
    if username == "paypalfailure":
        print("THIS SHOWS ITS GETTING TO paypalfailure")
        return redirect(url_for('paypalfailure'))
    if username == "withdraw_funds":
        print("THIS SHOWS ITS GETTING TO withdraw funds")
        return redirect(url_for('withdraw_funds'))    
    if username == "settings":
        print("\nTHIS SHOWS ITS GETTING TO settings funds")
        return redirect(url_for('settings'))  
    #=======================================================


    print(F"GOING TO A USER PROFILE: ", username)
    # ASSUME IT'S JUST SOMEBODIES NAME THEN?
    name_exists = database.CHECK_IF_NAME_EXISTS(username=username) #TODO:IMPLEMENT FUNCTION
    my_friends, friend_count = database.GET_FOLLOWING(username)
    my_followers, follow_count = database.GET_FOLLOWERS(username=username)
    # #TODO:might be worth doing a check befroe before the big query someday
    file_ids_list, usernames_list, paths_list, dates_list, post_sources_list, daily_left, monthly_left, yearly_left, day_votes, month_votes, year_votes, user_balance, dailypool, monthlypool, yearlypool, daily_votes_singular,  monthly_votes_singular, yearly_votes_singular = database.universal_dataset_function(search_type="prof", search_algo_path="foreandr-1", page_no="1", search_user=session['user'], profile_username=username)
    
    if len(file_ids_list) == 0:
        print("THERE IS NOTHING HERE", session['user'])
        user_balance, daily_left, monthly_left, yearly_left, dailypool, monthlypool, yearlypool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session['user']) # THIS ASSUMES ALREADY IN SESSION, SHOULD BE
        
    text_list = []
    age_18_list = []
    source_list = []
    image_path_list = []
    
    profile_bio = helpers.GET_USER_BIO(username)
    #print("USER BIO LEN  :", len(profile_bio))
    #print("USER BIOL     :", profile_bio)

    for i in range(len(usernames_list)):
        # print(usernames_list[i], paths_list[i])
        my_path = f"static/#UserData/{usernames_list[i]}/files/{paths_list[i]}"
        post_text, post_age_18, post_sources, post_image_path = helpers.get_postinfo_from_path(my_path)
        age_18_list.insert(i, post_age_18)
        source_list.insert(i, post_sources)
        text_list.insert(i, post_text)
        image_path_list.insert(i, post_image_path)

    # print("FILENAMES: ", filenames)
    lengths_of_text_files = []
    for i in text_list:
        lengths_of_text_files.append(len(i))

    if name_exists:
        
        return render_template(f"user_profile.html",
                #SPECIFIC TO USER PROFILE
                followers=my_followers,
                friends=my_friends,
                profile_bio=profile_bio,
                friend_count=friend_count,
                follow_count=follow_count,

                # NORMAL FOR ALL
                usernames_list=usernames_list,
                username_len=len(usernames_list),
                paths_list=paths_list,
                post_sources_list=post_sources_list,
                file_ids_list=file_ids_list,
                account_name=username,
                dates_list=dates_list,
                host_account=[username, session['user'], is_session_user, is_following],
                
                day_votes=day_votes,
                month_votes=month_votes,
                year_votes=year_votes,

                dailypool=dailypool,
                monthlypool=monthlypool,
                yearlypool=yearlypool,
                daily_votes_left=daily_left,
                monthly_votes_left=monthly_left,
                yearly_votes_left=yearly_left,
                user_balance = user_balance,

                text_list=text_list,
                lengths_of_text_files=lengths_of_text_files,
                age_18_list=age_18_list,
                source_list=source_list,
                image_path_list=image_path_list              
            )
    else:                             
        return redirect(url_for('home'))


@app.route("/add_funds", methods=['GET', 'POST'])
def add_funds():
    if "email" not in session:
        return redirect(url_for('login'))
    print("GOT TO ADD FUNDS HERE")

    

    if request.method == 'POST':
        print("DOING POST METHOD")
        if request.form['subscribe_button'] == 'SUBSCRIBE':
            is_already_subbed_this_month = database.CHECK_DATE( session["user"])   
            if is_already_subbed_this_month:
                return redirect(url_for('home'))#TODO:COULD REDIRECT TO SUB PAGE AND SAY ALREADY SUBBED

            subscribed = database.MANSURA_SUBSCRIBE( session["user"])
            print("REQUEST", request)
            print("SUBBED", subscribed)
            if subscribed: # IF SUBSCRIBE SUCCESSFULL
                print("WAS ABLE TO SUBSCRIBE")
                return redirect(url_for('home'))
            else:
                print("COULD NOT SUBSCRIBE")
                balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session["user"])
                return render_template(f"add_funds.html", 
                               session_user = session["user"],
                               sub_status = "YOU ARE ALREADY SUBSCRIBED OR DON'T HAVE A BALANCE OF OVER $5",
                               daily_votes_left=daily_votes_left,
                               monthly_votes_left=monthly_votes_left,
                               yearly_votes_left=yearly_votes_left,
                               balance = balance,
                               daily_pool=daily_pool, 
                               monthly_pool=monthly_pool, 
                               yearly_pool=yearly_pool
                               )
    session_username = session["user"]

    balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session_username)
    return render_template('add_funds.html', 
                            session_username=session_username,
                            daily_votes_left=daily_votes_left,
                            monthly_votes_left=monthly_votes_left,
                            yearly_votes_left=yearly_votes_left,
                            balance = balance,
                            daily_pool=daily_pool, 
                            monthly_pool=monthly_pool, 
                            yearly_pool=yearly_pool
                           )


@app.route("/withdraw_funds", methods=['GET', 'POST'])
def withdraw_funds():
    if "email" not in session:
        return redirect(url_for('login'))
    session_username = session["user"]

    print("GOT TO WITHDRAWFUNDS HERE")
    
    if request.method == "POST":
        print(F"\n {session_username} WANTS TO DO A WITHDRAWL")
        print(request)
        withdrawl_amount = 2
        # withdrawl_amount = request.form["withdrawl_amount"]
        print("WITHDRAWL AMOUNT", withdrawl_amount)
       
        #TODO: CHECK WITHDRAWL AMOUNT IS SMALLER THAN BALANCER
        balance = database.GET_USER_BALANCE_SIMPLE( session["user"])
        if balance >= withdrawl_amount:
            
            # THEN ADD IT TO THE END OF A WITHDRAW CSV
            with open('Python/withdrawl.csv', 'a') as f: # CAN MAKE THIS AN EXTERNAL FUNCTION #TODO:
                my_writer = writer(f)
            
                # Pass the list as an argument into
                # the writerow()
                my_writer.writerow([session_username, withdrawl_amount])
            
                # Close the file object
                f.close()
            print("FINISHED WRITING TO FILE")

            # THEN REMOVE THAT AMOUNT FROM USER BALANCE
            database.WITHDRAWL_FUNCTION(session_username, withdrawl_amount)
            print("UPDATED USER BALANCE")
            #return redirect(url_for("index.html"))
            return redirect(url_for('user_profile_name', username=session['user']))
        else:
            print("DIDNT HAVE ENOUGH")
    balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session_username)
    print(request)
    return render_template('withdraw_funds.html', 
                            session_username=session_username,
                            daily_votes_left=daily_votes_left,
                            monthly_votes_left=monthly_votes_left,
                            yearly_votes_left=yearly_votes_left,
                            balance = balance,
                            daily_pool=daily_pool, 
                            monthly_pool=monthly_pool, 
                            yearly_pool=yearly_pool
                           )
                           

@app.route("/get_csv/<account_name>/<folder>/<filename>", methods=['GET', 'POST'])
def get_csv(account_name, folder, filename):
    print('Filename:', account_name, folder, filename)
    full_file = "static/" + "#UserData/" + account_name + "/" + folder + "/" + filename
    print(full_file)
    with open(full_file) as fp:
        csv = fp.read()

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                     "attachment; filename=myplot.csv"})


@app.route("/add_user/<username>", methods=['POST'])
def add_user(username):
    if "email" not in session:
        return redirect(url_for('login'))
    # print('do something')
    user_id_first = database.GET_USER_ID( username=session['user'])
    user_id_second = database.GET_USER_ID( username=username)
    # print("USERNAME 1: ", session['user'], " | ID 1: ", user_id_first)
    # print("USERNAME 2: ", username, " | ID 2: ", user_id_second)
    if user_id_first == user_id_second:
        print("NOT ADDING YOURSELF")
        return redirect(url_for('user_profile_name', username=session['user']))
    else:
        print("inserting connection betrween: FOLLOWER=", user_id_first,"->FOLLOWING=", user_id_second)
        database.CONNECTION_INSERT( user_id_first, user_id_second)
        return redirect(url_for('user_profile_name', username=session['user']))


@app.route("/remove_user/<username>", methods=['POST'])
def remove_user(username):
    if "email" not in session:
        return redirect(url_for('login'))
    user_id_first = database.GET_USER_ID( username=session['user'])
    user_id_second = database.GET_USER_ID( username=username)
    if user_id_first == user_id_second:
        print("NOT REMOVING YOURSELF")
        return redirect(url_for('user_profile_name', username=session['user']))
    else:
        database.CONNECTION_REMOVE( user_id_first, user_id_second)
        return redirect(url_for('user_profile_name', username=session['user']))


@app.route("/password_recovery", methods=['GET', 'POST'])
def password_recovery():
    print("LOADING PASSWORD RECOVERY")

    if request.method == "POST":
        recovery_email = request.form["email"]
        print(recovery_email)
        my_email.send_email(recovery_email)
    return render_template(f"password_recovery.html")


@app.route("/password_reset", methods=['GET', 'POST'])
def password_reset():
    print("got here 1")
    if request.method == "POST":
        print("got here 2")
        email = request.form["email"]
        password = request.form["password"]
        recov_test_password = request.form["repeat_password"]
        print(email)
        print(password)
        print(recov_test_password)
        if password == recov_test_password:

            database.CHANGE_PASSWORD( email, password)
            print(email, " Password changed")
            return redirect(url_for("login"))
        else:
            print("got here 3")
            return render_template(f"password_reset.html", message="Passwords are not the same!")
    else:
        print("got here 4")
        return render_template(f"password_reset.html")


@app.route("/vote/<file_id>/<vote_type>", methods=['GET', 'POST'])
def file_vote(file_id, vote_type):
    if "email" not in session:
        return redirect(url_for('login'))
    print("voting", file_id, vote_type)
    is_already_subbed_this_month = database.CHECK_DATE( session["user"])
    if is_already_subbed_this_month:
        #print(is_already_subbed_this_month)
        database.FILE_VOTE_INSERT( session["user"], file_id, vote_type)
        return redirect(url_for("home"))
    else:
        return redirect(url_for("subscribe"))


@app.route("/paypalsuccess", methods=['GET', 'POST'])
def paypalsuccess():
    print((type(request)),":", request)
    #if request.method == "POST":
    #    print(request)
    #    for key,value in request.items():
    #        print(key, value)
    return render_template(f"paypalsuccess.html")


@app.route("/paypalfailure", methods=['GET'])
def paypalfailure():
    return render_template(f"paypalfailure.html")


@app.route("/PayPal_IPN", methods=['GET','POST'])
def PayPal_IPN():
    print("REQUESt:    ", request)
    
    '''This module processes PayPal Instant Payment Notification messages (IPNs).'''

    # Switch as appropriate
    VERIFY_URL_PROD = 'https://ipnpb.paypal.com/cgi-bin/webscr'
    VERIFY_URL = VERIFY_URL_PROD

    # Read and parse query string
    params = request.form.to_dict()

    # Add '_notify-validate' parameter
    params['cmd'] = '_notify-validate'
    
    #print(session)
    #print("PARAMS")
    #print(params, type(params))
    #for key, value in params.items():
    #    print(key, value)

    
    # print("PARAMS:", params)
    
    # Post back to PayPal for validation

    headers = {'content-type': 'application/x-www-form-urlencoded',
               'user-agent': 'Python-IPN-Verification-Script'}
    r = requests.post(VERIFY_URL, params=params, headers=headers, verify=True)
    r.raise_for_status()

    # Check return message and take action as needed
    if r.text == 'VERIFIED':
        print("SUCCESSFULL")
        item = params["item_name"]
        payer_email = params["payer_email"]
        #print("ITEM       :", item)
        print("PAYER EMAIL:", payer_email)
        database.SUBSCRIBE_FROM_PAYAPL_BUY(payer_email)
        return render_template(f"paypalsuccess.html",
            user=database.GET_USERNAME_BY_EMAIL(payer_email),
        )
        #TODO:SUBSCRIBE THE USER 
    elif r.text == 'INVALID':
        print("FAILURE")
        return render_template(f"paypalfailure.html",
            user=database.GET_USERNAME_BY_EMAIL(payer_email),
        )
    else:
        print("NOTHING HAPPENED?")
    

@app.route("/history", methods=['GET'])
def history():
    if "email" not in session:
        return redirect(url_for('login'))

    session_username = session["user"]
    print("HISTORY IS BEING SELECTED")
    print(os.getcwd())
    list_of_history_day = os.listdir( ( os.getcwd() + "/Python/HISTORY/Daily") )
    list_of_history_month = os.listdir( ( os.getcwd() + "/Python/HISTORY/Monthly") ) 
    list_of_history_year = os.listdir( ( os.getcwd() + "/Python/HISTORY/Yearly") )  
    
    balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session["user"])

    return render_template(f"history.html",
        all_daily=list_of_history_day,
        daily_len=len(list_of_history_day),
        
        all_monthly=list_of_history_month,
        monthly_len=len(list_of_history_month),
        
        all_yearly=list_of_history_year,
        yearly_len=len(list_of_history_month),

        daily_votes_left=daily_votes_left,
        monthly_votes_left=monthly_votes_left,
        yearly_votes_left=yearly_votes_left,
        balance=balance,
        daily_pool=daily_pool, 
        monthly_pool=monthly_pool, 
        yearly_pool=yearly_pool
    )


@app.route("/settings", methods=['GET', 'POST'])
def settings():
    print("SETTINGS IS BEING SELECTED")

    return render_template(f"settings.html",
    )


if __name__ == '__main__':
    #SUBTITLE Network Societey and it's Future
    
    #my_port = 443
    host = "0.0.0.0" #could be local host
    # logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG) #ISN'T    WORKING THE WAY I WANT
    # database.USER_FULL_RESET()

    
    thread = Thread(target = distribution_algorithm.TESTING_TIMING, args = ())
    thread.start()

    #app.run(host=host, port="8080", debug=True, use_reloader=False)  # host is to get off localhost
    serve(app, host=host)    

    # If the debugger is on, I can change my files in real time after saving
