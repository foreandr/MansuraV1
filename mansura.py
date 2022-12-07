# TODO:
#  NEED A DEBUG VERSION
#  NEED A TESTNET/PBE VERSION

# LIBRARIES 

from waitress import serve
import flask
import os
from os import path

from flask import Flask, render_template, request, session, redirect, url_for, g, send_from_directory, Response, send_file, make_response
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
from datetime import datetime, date
from csv import writer

import hashlib
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
    #print("RENDERING TEMPLATE")
    #if helpers.CHECK_IF_MOBILE(request):
    #    return redirect(url_for('cover_page'))
    if "email" not in session: # testasdkjhfaks
        return redirect(url_for('cover_page'))
    
    
    if "user" in session.keys():
        session_username = session["user"]
    else:
        session_username = ""
    helpers.log_function("request", request, session_user=session['user'])
    '''
    print("REQUEST TYP:",request.method)
    print("REQUEST URL:",request.url)
    '''

    search_json = {}
    json_search_clauses = "None"
    search = "None"

    if request.method == 'POST':
        search = request.form.get("search")   
        reset = request.form.get("reset")
        save_algo = request.form.get("save_algo")
        
        if save_algo != "None" and save_algo != None:
            returned_search_arguments = request.form.get("search_arguments")
            print("CURRENT ARGS TO BE SAVED", returned_search_arguments)
            database.SAVE_CURRENT_ALGO(returned_search_arguments)
            
        if reset != "None" and save_algo != None:
            print("CLICKED RESET")
            return redirect(url_for("home"))
        

        date_check = request.form.get("date_check")  
        order_check = request.form.get("order_check")  
        and_or_clauses, where_clauses, hi_eq_low, num_search_text = helpers.GET_ALL_QUERY_INFO_FROM_REQUEST_FORM(request)
        clauses_dict = [
            and_or_clauses, 
            where_clauses, 
            hi_eq_low, 
            num_search_text
        ]
        json_search_clauses = database.TURN_CLAUSES_INTO_JSON(search, date_check, order_check, clauses_dict, session_username)
    
    # GRAB THE ARGS FROM QUERY BEFORE THE CURRENT PAGE [GET OR POST]
    returned_search_arguments = request.form.get("search_arguments")
    # print(returned_search_arguments)

    new_json_search_clauses = helpers.COMPOSE_SEARCHARGS_AND_JSONCLAUSE(returned_search_arguments, json_search_clauses)
    '''
    print("COMPOSE_SEARCHARGS_AND_JSONCLAUSE")
    print(new_json_search_clauses)
    print("===================================")
    '''
    page_no = request.form.get("page_number")
    #print("CURRENT PAGE NUMBER:", type(page_no), page_no)
    # print("===================================")

    if page_no == None or str(page_no) == "None":
        page_no = 1

    #TODO: what I may have to do is do a similar query to the one below, but just returning a path list, grab all the paths that meet the criteria, then stick is back into
    # a function that returns the correct info with the search value in there as welll

    file_ids_list, usernames_list, paths_list, dates_list, post_sources_list, daily_left, monthly_left, yearly_left, day_votes, month_votes, year_votes, user_balance, dailypool, monthlypool, yearlypool, daily_votes_singular,  monthly_votes_singular, yearly_votes_singular, likes, dislikes,searcher_has_liked,searcher_has_disliked, num_replies, uploader_is_subbed, search_arguments = database.universal_dataset_function(search_type="home", page_no=page_no, search_user=session_username, custom_clauses=new_json_search_clauses)
    # print("hello??", num_replies)
    #print(searcher_has_liked)
    #print(searcher_has_disliked)
    
    #FOR DIABLING OR ACTIVATING SCROLL LOGIC
    numposts = len(file_ids_list)
    if numposts < 29: # this 100 number needs to be better coded, hard coding is going to cause issues
        can_scroll = False
    else:
        can_scroll = True


    # GRAB STUFF IT'S IT'S EMPTY EITHE RWAY
    if len(file_ids_list) == 0:
        print("IS EMPTY")
        user_balance, daily_left, monthly_left, yearly_left, dailypool, monthlypool, yearlypool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session_username)
    
    username_len = len(usernames_list)
    # print("USERNAMES LEN", username_len, usernames_list)

    text_list = []
    age_18_list = []
    source_list = []
    image_path_list = []
    distro_details_list = []
    for i in range(len(usernames_list)): # GETTING POST INFO FROM PATH
        my_path = f"static/#UserData/{usernames_list[i]}/files/{paths_list[i]}"
        post_text, post_age_18, post_sources, post_image_path, distro_details = helpers.get_postinfo_from_path(my_path)
        age_18_list.insert(i, post_age_18)
        source_list.insert(i, post_sources)
        text_list.insert(i, post_text)
        image_path_list.insert(i, post_image_path)
        distro_details_list.insert(i,distro_details)
    
    lengths_of_text_files = []
    for i in text_list:
        lengths_of_text_files.append(len(i))

    # GET SEARCH FAVOURITES
    search_favourites = database.GET_SEARCH_FAVOURITES_BY_USERNAME(session["user"])
    favourites_len = len(search_favourites)
    if favourites_len > 20:
        favourites_len = 20

    return render_template('index.html',
                            message="index.html page",
                           
                            usernames_list=usernames_list,
                            file_ids_list=file_ids_list,
                            session_username=session_username,
                            username_len=username_len,
                           
                            paths_list=paths_list,
                            dates_list=dates_list,
                            post_sources_list=post_sources_list,
                            likes=likes,
							dislikes=dislikes,
							searcher_has_liked=searcher_has_liked, 
							searcher_has_disliked=searcher_has_disliked,
                            num_replies=num_replies,
                            
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
                            distro_details_list=distro_details_list,
                            
                            search_arguments=search_arguments,
                            page_no=page_no,
                            can_scroll=can_scroll,
                            
                            search_favourites=search_favourites,
                            favourites_len=favourites_len,
                            uploader_is_subbed=uploader_is_subbed
                           )


@app.route('/register', methods=['GET', 'POST'])
def register():
    #print("RENDERING TEMPLATE")
    # print('EXECUTING REGISTER FUNCTION')
    helpers.log_function("request", request)
    if "email" in session:
        return redirect(url_for("user_profile"))
    if request.method == 'GET':
        sign_up_message = 'Please sign up'
        return render_template('register.html', message=sign_up_message)

    if request.method == 'POST':
        my_dict = request.form.to_dict(flat=False)
        #print(my_dict)
        try:  # DO NOT EXECUTE UNTIL SUBMIT IS CLICKED
            #print("INSIDE REGISTER POST")
            registering_username = my_dict['username'][0]
            password = my_dict['password'][0]
            email = my_dict['email'][0]
            paypal_email =my_dict['paypal_email'][0]

            #print("\nREGISTRATION DETAILS")
            #print("registering_username   :", registering_username)
            #print("password               :", password)
            password = password.encode('utf-8')
            hashedPassword = hashlib.sha256(password).hexdigest()
            #print("hashedPassword         :",hashedPassword)
            #print("email                  :", email)
            #print("paypal_email           :",paypal_email)

            # CHECK WHETHER VALUES ARE IN RESTRICTED LIST
            
            has_bad_words = helpers.USERNAME_PROFANITY_CHECK(registering_username)
            # print("has_bad_words", has_bad_words)
            if not has_bad_words:

                # print(registering_username, "is registering their account!")
                # print(password)

                # database.create_user(conn=connection, username="hello", password="password", email="bce@hotmail.com")
                if database.full_register(username=registering_username, password=hashedPassword, email=email, paypal_email=paypal_email, balance=0):
                    return redirect(url_for('login'))
                # GO TO THEIR PROFILE
                else:
                    return render_template('register.html', 
                    return_message="Name already exists"
                )
                

            else:
                return render_template('register.html', 
                    return_message="Mansura thinks you either have a bad word, or something that could be used for an SQL attack of some kind."
                )

        except Exception as e:
            helpers.log_function("error", e)
        return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # print('EXECUTING LOGIN FUNCTION')
    helpers.log_function("request", request)
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

        # print("password               :", password)
        password = password.encode('utf-8')
        hashedPassword = hashlib.sha256(password).hexdigest()

        signed_in = database.validate_user_from_session(email, hashedPassword)

        if signed_in[0]:
            session["id"] = signed_in[1]
            session["user"] = signed_in[2]
            session["email"] = email
            #session["password"] = password
            # print('SESSION INFO: ', session)
            return redirect(url_for("user_profile"))
        else:
            return render_template('login.html', message="wrong email or password, try again")


@app.route('/logout', methods=['GET'])
def logout():
    helpers.log_function("request", request)
    session.pop("email", None)  # remove data from session
    session.pop("user", None)  # remove data from session
    session.pop("password", None)  # remove data from session
    return redirect(url_for("login"))


@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    #print("RENDERING TEMPLATE")
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    #print('USING USER PROFILE')

    # print(request)
    if "email" not in session:
        return redirect(url_for('login'))
    helpers.log_function("request", request, session_user=session['user'])

    if request.method == "GET":
        return redirect(url_for('user_profile_name', username=session['user']))
    
    #THIS IS WHERE PROFILE PICTRUE IS CHANGED
    elif request.method == "POST":
        user = session["user"]
        id = session["id"]

        if request.files:
            file = request.files['file']
            my_path_with_file = f"{app.config['FILE UPLOADS']}/{user}/profile/profile_pic.jpg"  
            if file.content_type == "image/jpeg" or file.content_type == "image/png":
                if helpers.POST_IMG_CHECK(file):
                    print("should be saving the file")
                    file.stream.seek(0)
                    file.save(my_path_with_file)
                else:
                    return redirect(url_for("terms_and_conditions"))

        return redirect(url_for("user_profile"))
    

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    
    if "email" not in session:
        return redirect(url_for('login'))

    helpers.log_function("request", request, session_user=session['user'])
    if request.method == "POST": # UPLOADING SOMETHING
        save_algo = request.form.get("save_algo")
        if save_algo != "None" and save_algo != None:
            hidden_search_arguments = request.form.get("hidden_search_arguments")
            hidden_search_arguments = helpers.TURN_STRING_TO_DICT(hidden_search_arguments)
            
            where_clause = hidden_search_arguments['where_full_query']
            order_by_clause = hidden_search_arguments['order_by_clause']
            user_name = session["user"]
            search_algo_name = session["user"] + "-" + request.form.get("Algorithm Name")
            check_success = database.SEARCH_ALGO_INSERT(username=session["user"], Algorithm_Name=search_algo_name, order_by_clause=order_by_clause, where_clause=where_clause)
            if check_success:
                return redirect(url_for("search_algorithms_page"))
            else:
                print("FAILED CUZ OF DUPE")# todo: gotta find a way to show the user
                return redirect(url_for("search_algorithms_page"))
        
        #print("GOT TO WHETHER SOMETHING IS BEING POISTED OR NOT ==================================")
        post_text = request.form.get("textbox")
        post_file = request.files['file']
        # plus_18 =  request.form.get("older_18")
        plus_18 = "older_18"# make it that by default
        forign_id_source = str(request.form.get("external_source"))
        external_link = request.form.get("external_source_link")
        distribution_algorithm_ = str(request.form.get("distro_algo"))
        how_many_sections = str(request.form.get("how_many_sections_"))
        
        ''''''
        print("UPLOAD DETAILS ==============================")
        print("UPLOADER   :" + str(session['user']))
        print("POST TEXT  :" + str(post_text))        
        print("POST FILE  :" + str(post_file))
        print("POST LINK  :" + str(external_link))
        print("POST FOID  :" + str(forign_id_source))
        print("POST 18+   :" + str(plus_18))
        print("DISTRO ALGO:" + distribution_algorithm_, type(distribution_algorithm_))
        print("DISTRO SECT:" + str(how_many_sections))
        distro_details = [distribution_algorithm_, how_many_sections]
        print(distro_details)
        print("=============================================")

        post_text = helpers.POST_TEXT_CHECK(post_text)

        # helpers.ADD_POST_KEYWORDS_TO_DATABASE(post_text) #TODO:IMPLEMENT THIS

        if len(post_file.filename) != 0: #THERE IS A FILE
            if helpers.POST_IMG_CHECK(post_file):
                pass
            else:
                #print("IMG HAD BAD SHIT")
                return redirect(url_for("terms_and_conditions"))
                

        #print(len(post_file.filename), post_file.filename)
        if ( (len(post_text) == 0) and (len(post_file.filename) == 0)): 
            #print("EMPTY HERE")
            #print("post text:", post_text, type(post_text), len(post_text))
            #print("filename:", post_file.filename, type(post_file.filename), len(post_file.filename))
            return redirect(url_for("home"))
            
        file_id, forign_id_source = database.FILE_INSERT( 
                uploader=session["user"], 
                uploaderId=database.GET_USER_ID(session["user"]), 
                size="10", 
                post_foreign_id_source=forign_id_source, 
                file_path="N-A", post_file=post_file, 
                post_text=post_text, age_18=plus_18, 
                external_link=external_link,
                distro_details=distro_details
                )

        if forign_id_source != "None" and forign_id_source != "":
            name, path = database.GET_POST_URL_BY_ID(forign_id_source)
            return_path = name + "_" + path + "-post_page"
            # return redirect(url_for("user_profile_name")) 
            return redirect(url_for('user_profile_name', username=return_path))
        else:
            try:
                name, path = database.GET_POST_URL_BY_ID(file_id)
                return_path = name + "_" + path + "-post_page"        
                return redirect(url_for('user_profile_name', username=return_path))
            except Exception as e:
                helpers.log_function("error", e + "[MY GUESS IS IT'S TOO BIG FOREIGN]")
    else:
        return redirect(url_for("home"))


@app.route('/<username>', methods=['GET', 'POST'])
def user_profile_name(username):
    # print("I AM IN USERNAME")
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    #print('EXECUTING WITH ARGUMENT: ', username)
    helpers.log_function("request", request)
    if "email" not in session:
        return redirect(url_for('login'))
    if username == "favicon.ico": # check weird username issue

        return redirect(url_for('home'))
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
        # print("GOING TO A PARTICULAR POST")
        if "email" in session:
            balance = database.GET_USER_BALANCE_SIMPLE( session["user"])
        else:
            balance = 0

        # print("\nTHIS SHOWS ITS GETTING TO INDIVIDUAL FILE========================")
        # print(username)
        list_from_username = username.split("_")

        new_username = list_from_username[0]
        filename = list_from_username[1].split("_page") # something going on weird here that is making me do the split twice
        new_filename = filename[0].split("-post")
        final_filename = new_filename[0]
        file_id = final_filename.split("-")[1]
        single_num_replies = database.GET_NUM_REPLIES(file_id)
        
        reply_array = database.GET_ALL_REPLIES(file_id)
        post_username, post_file_path, post_user_id, post_foreign_id_source, post_date, file_id_, single_day_votes, single_month_votes, single_year_votes, single_likes, single_dislikes = database.GET_SINGLE_DATASET_INFO(final_filename)

        search_json = {}
        json_search_clauses = "None"
        if request.method == 'POST':
            search = request.form.get("search")   
            date_check = request.form.get("date_check")  
            order_check = request.form.get("order_check")  
            
            and_or_clauses, where_clauses, hi_eq_low, num_search_text = helpers.GET_ALL_QUERY_INFO_FROM_REQUEST_FORM(request)
            
            clauses_dict = [
                and_or_clauses, 
                where_clauses, 
                hi_eq_low, 
                num_search_text
            ]
            json_search_clauses = database.TURN_CLAUSES_INTO_JSON(search, date_check, order_check, clauses_dict, session['user'])

        returned_search_arguments = request.form.get("search_arguments")
        page_no = request.form.get("page_number")
        
        new_json_search_clauses = helpers.COMPOSE_SEARCHARGS_AND_JSONCLAUSE(returned_search_arguments, json_search_clauses)
        if page_no == None or str(page_no) == "None":
                page_no = 1
                
        
        file_ids_list, usernames_list, paths_list, dates_list, post_sources_list, daily_left, monthly_left, yearly_left, day_votes, month_votes, year_votes, user_balance, dailypool, monthlypool, yearlypool, daily_votes_singular,  monthly_votes_singular, yearly_votes_singular, likes, dislikes,searcher_has_liked,searcher_has_disliked, num_replies, uploader_is_subbed, search_arguments = database.universal_dataset_function(search_type="post", page_no=page_no, search_user=session['user'], custom_clauses=new_json_search_clauses, file_id=file_id_)
        # print(num_replies)


        sername_len = len(usernames_list)
        if len(file_ids_list) == 0:
            # print("THERE IS NOTHING NO FILES ON HOMEPAGE HERE", session['user'])
            user_balance, daily_left, monthly_left, yearly_left, dailypool, monthlypool, yearlypool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session['user']) # THIS ASSUMES ALREADY IN SESSION, SHOULD BE

        if len(file_ids_list) < 29: # this 100 number needs to be better coded, hard coding is going to cause issues
            can_scroll = False
        else:
            can_scroll = True


        text_list = []
        age_18_list = []
        source_list = []
        image_path_list = []
        distro_details_list = []
        #print(usernames_list)
        #print(len(usernames_list))
        # print(file_id)
        for i in range(len(usernames_list)): # GETTING POST INFO FROM PATH
            # exit(0)
            my_path = f"static/#UserData/{usernames_list[i]}/files/{paths_list[i]}"
            # print(my_path)
            post_text, post_age_18, post_sources, post_image_path, distro_details = helpers.get_postinfo_from_path(my_path)
            age_18_list.insert(i, post_age_18)
            source_list.insert(i, post_sources)
            text_list.insert(i, post_text)
            image_path_list.insert(i, post_image_path)
            distro_details_list.insert(i,distro_details)

        if len(text_list) == 0: # IF NOTHING RETURNED GET VOTE DETAILS
            #print("getting values", session['user'])
            _1, daily_left, monthly_left, yearly_left, _1, _2, _3 = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session['user']) # THIS ASSUMES ALREADY IN SESSION, SHOULD BE
            #print(daily_left, monthly_left, yearly_left)
            single_day_votes, single_month_votes, single_year_votes =  database.GET_FILE_ALL_VOTES_BY_ID(file_id)

        searcher_like_single, searcher_dislike_single = database.GET_SEARCH_LIKES_SINGLE_POST(session['user'], file_id)

        og_post_text = ""
        og_post_18 = ""
        og_post_src = ""
        og_post_img = ""
        og_post_distro_details = ""
        # print(text_list)
        lengths_of_text_files = []
        my_og_path = f"static/#UserData/{post_username}/files/{post_file_path}"
        for i in text_list:
            lengths_of_text_files.append(len(i))
        
        og_post_text, og_post_18, og_post_src, og_post_img, og_post_distro_details = helpers.get_postinfo_from_path(my_og_path)
        lengths_of_text_files = []
        for i in text_list:
            lengths_of_text_files.append(len(i))
            # DOUBLE CHECK IMG PATH BECAUSE ABOVE MIGHT BE EMPTY
        
        pic_path = os.path.join(my_og_path + "/pic.jpg").strip()
        if not path.exists(pic_path):
            og_post_img = ""
        else:
            og_post_img = pic_path[7:]

        search_favourites = database.GET_SEARCH_FAVOURITES_BY_USERNAME(session["user"])
        favourites_len = len(search_favourites)
        if favourites_len > 20:
            favourites_len = 20
        
        try: # MOVE THIS TO IT'S OWN FUNCTION
            replying_to_path = database.GET_PATH_BY_FILE_ID(post_foreign_id_source)
            name_and_id = replying_to_path.split("-")
            name = name_and_id[0]
            their_id =  name_and_id[1]
            full_replying_to_path = name + "_" + name + "-" + their_id + "-post_page"
            #print(full_replying_to_path)
        except Exception as e:
            #print(e)
            full_replying_to_path =""
        # print(full_replying_to_path)

        return render_template('post_details.html',
                                # POST DETAILS

                                len_text=len(og_post_text),
                                og_post_text=og_post_text,
                                og_post_img=og_post_img ,
                                og_post_src=og_post_src,
                                og_post_18=og_post_18,
                                og_post_distro_details=og_post_distro_details,
                                test_message="post_details.html page",
                                lengths_of_text_files=lengths_of_text_files,
                                username_len=len(usernames_list),
                                username=post_username,
                                final_filename=final_filename,
                                file_id=file_id,
                                single_num_replies=single_num_replies,
                                post_user_id=post_user_id,
                                post_foreign_id_source=post_foreign_id_source,
                                post_date=post_date,
                                reply_array=reply_array,

                                search_favourites=search_favourites,
                                favourites_len=favourites_len,

                                daily_dataset_votes=single_day_votes, 
                                monthly_dataset_votes=single_month_votes,
                                yearly_dataset_votes=single_year_votes, 
                                single_likes=single_likes, 
                                single_dislikes=single_dislikes,

                                searcher_like_single=searcher_like_single, 
                                searcher_dislike_single=searcher_dislike_single,
								
								searcher_has_liked=searcher_has_liked, 
								searcher_has_disliked=searcher_has_disliked,

                                usernames_list=usernames_list,
                                file_ids_list=file_ids_list,
                                session_username=session["user"],
                                paths_list=paths_list,
                                dates_list=dates_list,
                                post_sources_list=post_sources_list,
                                likes=likes,
                                dislikes=dislikes,
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
                                age_18_list=age_18_list,
                                source_list=source_list,
                                image_path_list=image_path_list,
                                distro_details_list=distro_details_list,
                                num_replies=num_replies,          
                                uploader_is_subbed=uploader_is_subbed,                  
                                
                                search_arguments=search_arguments,
                                page_no=page_no,
                                can_scroll=can_scroll,
                                full_replying_to_path=full_replying_to_path
                            )        
    else:
        # print(username, "does not end with -post_page")
        pass
    if database.CHECK_IF_NAME_EXISTS(username) == False:
        #print("NAME DOESNT EXIST")
        return redirect(url_for('home'))             
    if username == 'upload':
        print("THIS SHOWS ITS GETTING TO UPLOAD")
        return redirect(url_for('upload'))
    if username == 'subscribe':
        #print("THIS SHOWS ITS GETTING TO SUBSCRIBE")
        return redirect(url_for('subscribe'))
    if username == "add_funds":
        #print("THIS SHOWS ITS GETTING TO ADD FUNDS")
        return redirect(url_for('add_funds'))
    if username == "paypalsuccess":
        #print("THIS SHOWS ITS GETTING TO paypalsuccess")
        return redirect(url_for('paypalsuccess'))
    if username == "paypalfailure":
        #print("THIS SHOWS ITS GETTING TO paypalfailure")
        return redirect(url_for('paypalfailure'))
    if username == "withdraw_funds":
        #print("THIS SHOWS ITS GETTING TO withdraw funds")
        return redirect(url_for('withdraw_funds'))    
    if username == "settings":
        #print("\nTHIS SHOWS ITS GETTING TO settings funds")
        return redirect(url_for('settings'))  
    #=======================================================

    #print(F"GOING TO A USER PROFILE: ", username)
    # ASSUME IT'S JUST SOMEBODIES NAME THEN?
    name_exists = database.CHECK_IF_NAME_EXISTS(username=username) 
    my_friends, friend_count = database.GET_FOLLOWING(username)
    my_followers, follow_count = database.GET_FOLLOWERS(username=username)

    if session["user"] == username: # BOOLEAN HAS TO BE THIS DUMB WAY FOR JAVASCRIPT iLL ADVISED
        is_host = "true"
        can_follow = "false"
    else:
        is_host = "false"
        if session["user"] in my_followers:
            can_follow = "false"
        else:
            can_follow = "true"

    search_json = {}
    json_search_clauses = "None"
    if request.method == 'POST':
        search = request.form.get("search")   
        date_check = request.form.get("date_check")  
        order_check = request.form.get("order_check")  
        and_or_clauses, where_clauses, hi_eq_low, num_search_text = helpers.GET_ALL_QUERY_INFO_FROM_REQUEST_FORM(request)
        clauses_dict = [
            and_or_clauses, 
            where_clauses, 
            hi_eq_low, 
            num_search_text
        ]
        json_search_clauses = database.TURN_CLAUSES_INTO_JSON(search, date_check, order_check, clauses_dict, session["user"])

    returned_search_arguments = request.form.get("search_arguments")
    page_no = request.form.get("page_number")
    
    new_json_search_clauses = helpers.COMPOSE_SEARCHARGS_AND_JSONCLAUSE(returned_search_arguments, json_search_clauses)
    if page_no == None or str(page_no) == "None":
            page_no = 1
            

    file_ids_list, usernames_list, paths_list, dates_list, post_sources_list, daily_left, monthly_left, yearly_left, day_votes, month_votes, year_votes, user_balance, dailypool, monthlypool, yearlypool, daily_votes_singular,  monthly_votes_singular, yearly_votes_singular, likes, dislikes,searcher_has_liked,searcher_has_disliked, num_replies, uploader_is_subbed, search_arguments = database.universal_dataset_function(search_type="prof", page_no=page_no, search_user=session['user'], profile_username=username, custom_clauses=new_json_search_clauses)
    # print(num_replies)
    # print("UNIVERSAL PROFILE GOT", file_ids_list)
    username_len = len(usernames_list)
    if len(file_ids_list) == 0:
        # print("THERE IS NOTHING NO FILES ON HOMEPAGE HERE", session['user'])
        user_balance, daily_left, monthly_left, yearly_left, dailypool, monthlypool, yearlypool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session['user']) # THIS ASSUMES ALREADY IN SESSION, SHOULD BE

    if len(file_ids_list) < 29: # this 100 number needs to be better coded, hard coding is going to cause issues
        can_scroll = False
    else:
        can_scroll = True

    profile_bio = helpers.GET_USER_BIO(username)

    text_list = []
    age_18_list = []
    source_list = []
    image_path_list = []
    distro_details_list = []
    for i in range(len(usernames_list)): # GETTING POST INFO FROM PATH
        my_path = f"static/#UserData/{usernames_list[i]}/files/{paths_list[i]}"
        post_text, post_age_18, post_sources, post_image_path, distro_details = helpers.get_postinfo_from_path(my_path)
        age_18_list.insert(i, post_age_18)
        source_list.insert(i, post_sources)
        text_list.insert(i, post_text)
        image_path_list.insert(i, post_image_path)
        distro_details_list.insert(i,distro_details)

    lengths_of_text_files = []
    for i in text_list:
        lengths_of_text_files.append(len(i))
    
    search_favourites = database.GET_SEARCH_FAVOURITES_BY_USERNAME(session["user"])
    favourites_len = len(search_favourites)
    if favourites_len > 20:
        favourites_len = 20

    if name_exists:
        return render_template('user_profile.html',
                                message="user_profile.html page",
                                host_user=username,
                                followers=my_followers,
                                friends=my_friends,
                                friend_count=friend_count,
                                follow_count=follow_count,
                                profile_bio=profile_bio,
                                
                                favourites_len=favourites_len,
                                search_favourites=search_favourites,


                                usernames_list=usernames_list,
                                file_ids_list=file_ids_list,
                                session_username=session['user'],
                                username_len=username_len,
                                paths_list=paths_list,
                                dates_list=dates_list,
                                post_sources_list=post_sources_list,
                                likes=likes,
                                dislikes=dislikes,
                                num_replies=num_replies,

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
	
								searcher_has_liked=searcher_has_liked, 
								searcher_has_disliked=searcher_has_disliked,
                                text_list=text_list,
                                lengths_of_text_files=lengths_of_text_files,
                                age_18_list=age_18_list,
                                source_list=source_list,
                                image_path_list=image_path_list,
                                distro_details_list=distro_details_list,
                                uploader_is_subbed=uploader_is_subbed,
                                
                                search_arguments=search_arguments,
                                page_no=page_no,
                                can_scroll=can_scroll, 
                                is_host=is_host,
                                can_follow=can_follow

                            )
    else:                             
        return redirect(url_for('home'))


@app.route("/add_funds", methods=['GET', 'POST'])
def add_funds():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    
    if "email" not in session:
        return redirect(url_for('login'))
    
    helpers.log_function("request", request, session_user=session['user'])
    if request.method == 'POST':
        #print("DOING POST METHOD")
        if request.form['subscribe_button'] == 'SUBSCRIBE':
            is_already_subbed_this_month = database.CHECK_DATE( session["user"])   
            if is_already_subbed_this_month:
                return redirect(url_for('home'))#TODO:COULD REDIRECT TO SUB PAGE AND SAY ALREADY SUBBED

            subscribed = database.MANSURA_SUBSCRIBE(session["user"])
            #print("REQUEST", request)
            #print("SUBBED", subscribed)
            if subscribed: # IF SUBSCRIBE SUCCESSFULL
                #print("WAS ABLE TO SUBSCRIBE")
                return redirect(url_for('home'))
            else:
                #print("COULD NOT SUBSCRIBE")
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
                               yearly_pool=yearly_pool,
                               is_already_subbed_this_month=is_already_subbed_this_month
                               )
    session_username = session["user"]
    is_already_subbed_this_month = database.CHECK_DATE( session["user"])   
    balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session_username)
    return render_template('add_funds.html', 
                            session_username=session_username,
                            daily_votes_left=daily_votes_left,
                            monthly_votes_left=monthly_votes_left,
                            yearly_votes_left=yearly_votes_left,
                            balance = balance,
                            daily_pool=daily_pool, 
                            monthly_pool=monthly_pool, 
                            yearly_pool=yearly_pool,
                            is_already_subbed_this_month=is_already_subbed_this_month
                           )


@app.route("/withdraw_funds", methods=['GET', 'POST'])
def withdraw_funds():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    
    if "email" not in session:
        return redirect(url_for('login'))
    session_username = session["user"]
    helpers.log_function("request", request, session_user=session['user'])
    #print("GOT TO WITHDRAWFUNDS HERE")
    
    if request.method == "POST":
        print(F"\n {session_username} WANTS TO DO A WITHDRAWL")
        #print(request)
        withdrawl_amount = float(request.form.get("withdraw_amount"))
        print("WITHDRAWL AMOUNT", withdrawl_amount)

        balance = float(database.GET_USER_BALANCE_SIMPLE( session["user"]))
        if balance >= withdrawl_amount:
            # THEN ADD IT TO THE END OF A WITHDRAW CSV
            with open('Python/withdrawl.csv', 'a') as f: # CAN MAKE THIS AN EXTERNAL FUNCTION #TODO:
                my_writer = writer(f)
            
                # Pass the list as an argument into
                # the writerow()
                my_writer.writerow([session_username, withdrawl_amount, date.today(), database.GET_PAYPAL_EMAIL_BY_USERNAME(session_username)])
            
                # Close the file object
                f.close()
            #print("FINISHED WRITING TO FILE")

            # THEN REMOVE THAT AMOUNT FROM USER BALANCE
            database.WITHDRAWL_FUNCTION(session_username, withdrawl_amount)
            #print("UPDATED USER BALANCE")
            #return redirect(url_for("index.html"))
            return redirect(url_for('user_profile_name', username=session['user']))
        else:
            # print("DIDNT HAVE ENOUGH")
            pass
    balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session_username)
    # print(request)
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
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    helpers.log_function("request", request)
    #print('Filename:', account_name, folder, filename)
    full_file = "static/" + "#UserData/" + account_name + "/" + folder + "/" + filename
    #print(full_file)
    with open(full_file) as fp:
        csv = fp.read()

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                     "attachment; filename=myplot.csv"})


@app.route("/add_user/<username>", methods=['POST'])
def add_user(username):
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
   
    if "email" not in session:
        return redirect(url_for('login'))
    helpers.log_function("request", request, session_user=session['user'])
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
        return redirect(url_for('user_profile_name', username=username))


@app.route("/remove_user/<username>", methods=['POST'])
def remove_user(username):
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    
    if "email" not in session:
        return redirect(url_for('login'))
    helpers.log_function("request", request, session_user=session['user'])
    
    user_id_first = database.GET_USER_ID( username=session['user'])
    user_id_second = database.GET_USER_ID( username=username)
    if user_id_first == user_id_second:
        print("NOT REMOVING YOURSELF")
        return redirect(url_for('user_profile_name', username=session['user']))
    else:
        database.CONNECTION_REMOVE( user_id_first, user_id_second)
        return redirect(url_for('user_profile_name', username=session['user']))

@app.route("/report/<file_id>", methods=['GET','POST'])
def report(file_id):
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    
    if "email" not in session:
        return redirect(url_for('login'))
    
    helpers.log_function("request", request, session_user=session['user'])
    # INSERT INTO TRIBUNAL
    print("REPORTING", file_id)
    database.INSERT_INTO_TRIBUNAL(file_id)
    return redirect(url_for('home'))


@app.route("/password_recovery", methods=['GET', 'POST'])
def password_recovery():
    helpers.log_function("request", request)
    #print("LOADING PASSWORD RECOVERY")

    if request.method == "POST":
        recovery_email = request.form["email"]
        # print(recovery_email)
        database.CREATE_AND_SEND_ONE_TIME_PASS_EMAIL(recovery_email)
        # my_email.send_email(recovery_email)
        return redirect(url_for('password_reset'))
    return render_template(f"password_recovery.html")


@app.route("/password_reset", methods=['GET', 'POST'])
def password_reset():#TODO: GET THIS WORKING, CHECK IF OEN TIME PASS IS THE SMAE
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    helpers.log_function("request", request)

    if request.method == "POST":
        print("TEST 1 ")
        
        email = request.form["email"]
        password = request.form["password"]
        repeat_pass = request.form["check_password"]
        one_time_pass = request.form["One Time Password"]
        current_one_time_pass = database.GET_ONE_TIME_PASS(email)
        
        print("email                :",email)
        print("password             :",password)
        print("repeat_pass          :",repeat_pass)
        print("one_time_pass        :",one_time_pass)
        print("current_one_time_pass:",current_one_time_pass)
        

        if (password == repeat_pass) and (one_time_pass == current_one_time_pass):
            database.CHANGE_PASSWORD( email, password)
            return redirect(url_for("login"))
        else:
            return render_template(f"password_reset.html", message="Passwords are not the same! \nOr One Time Password is Incorrect!")
    else:
        return render_template(f"password_reset.html")


@app.route("/user_download_excel/<vote_timeframe>/<vote_date>", methods=['GET', 'POST'])
def user_download_excel(vote_timeframe, vote_date):
	if helpers.CHECK_IF_MOBILE(request):
		return redirect(url_for('cover_page'))
	try:
		custom_path = f"/root/mansura/Python/logs/distro/{vote_timeframe}/{vote_date}/FULL_SET.txt" # SHOULD ADD DISTRO
		# print(custom_path)
		filename = "Mansura-"+ vote_date + ".txt"
		return send_file(custom_path, download_name=filename)
	except Exception as e:
		helpers.log_function("error", e)


@app.route("/vote/<file_id>/<vote_type>", methods=['GET', 'POST'])
def file_vote(file_id, vote_type):
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    
    if "email" not in session:
        return redirect(url_for('login'))
    
    helpers.log_function("request", request, session_user=session['user'])
    # print("voting", file_id, vote_type)
    name, path = database.GET_POST_URL_BY_ID(file_id)
    return_path = name + "_" + path + "-post_page"

    if vote_type == "like":
        #print("DOING LIKE LOGIC")
        database.LIKE_LOGIC(session["user"], file_id)
        return redirect(url_for('user_profile_name', username=return_path))
    
    if vote_type == "dislike":
        #print("DOING DISLIKE LOGIC")
        database.DISLIKE_LOGIC(session["user"], file_id)
        return redirect(url_for('user_profile_name', username=return_path))
    
    is_already_subbed_this_month = database.CHECK_DATE( session["user"])
    if is_already_subbed_this_month:
        #print(is_already_subbed_this_month)
        database.FILE_VOTE_INSERT( session["user"], file_id, vote_type)
        return redirect(url_for('user_profile_name', username=return_path))
    else:
        return redirect(url_for("subscribe"))


@app.route("/paypalsuccess", methods=['GET', 'POST'])
def paypalsuccess():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    helpers.log_function("request", request)
    print((type(request)),":", request)
    #if request.method == "POST":
    #    print(request)
    #    for key,value in request.items():
    #        print(key, value)
    return render_template(f"paypalsuccess.html")


@app.route("/paypalfailure", methods=['GET'])
def paypalfailure():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    helpers.log_function("request", request)
    return render_template(f"paypalfailure.html")


@app.route("/PayPal_IPN", methods=['GET','POST'])
def PayPal_IPN():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    helpers.log_function("request", request)
    # print("REQUESt:    ", request)
    
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
        #print("SUCCESSFULL")
        item = params["item_name"]
        payer_email = params["payer_email"]
        #print("ITEM       :", item)
        # print("PAYER EMAIL:", payer_email)
        database.SUBSCRIBE_FROM_PAYAPL_BUY(payer_email)

        helpers.log_function(msg_type="payment", log_string=F"{payer_email} subscribed!")
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
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    
    if "email" not in session:
        return redirect(url_for('login'))
    
    helpers.log_function("request", request, session_user=session['user'])
    
    session_username = session["user"]
    #print("HISTORY IS BEING SELECTED")
    print(os.getcwd())
    list_of_history_day = os.listdir("/root/mansura/Python/logs/distro/Daily") 
    list_of_history_month = os.listdir("/root/mansura/Python/logs/distro/Monthly") 
    list_of_history_year = os.listdir("/root/mansura/Python/logs/distro/Yearly") 
    
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
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    helpers.log_function("request", request)
    
    # print("SETTINGS IS BEING SELECTED")
    balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session["user"])
    return render_template(f"settings.html",
        daily_votes_left=daily_votes_left,
        monthly_votes_left=monthly_votes_left,
        yearly_votes_left=yearly_votes_left,
        balance=balance,
        daily_pool=daily_pool, 
        monthly_pool=monthly_pool, 
        yearly_pool=yearly_pool
    )


@app.route("/terms_and_conditions", methods=['GET'])
def terms_and_conditions():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    helpers.log_function("request", request)
    return render_template(f"terms_and_conditions.html",
    )


@app.route("/search_algorithms_page", methods=['GET', 'POST'])
def search_algorithms_page():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    
    if "email" not in session:
        return redirect(url_for('login'))
    helpers.log_function("request", request, session_user=session['user'])
    
    algos = ""
    if request.method == "POST":
        save_algo = request.form.get("save_algo")
        del_algo = request.form.get("del_algo")
        show_all = request.form.get("show_all")
        show_favourites = request.form.get("show_favourites")
        #print("save_algo", save_algo)
        #print("show_all", show_all)
        #print("save_algo", show_favourites)

        if save_algo != None:
            search_id = database.GET_SEARCH_ALGO_ID_BY_NAME(save_algo)
            database.INSERT_INTO_SEARCH_FAVOURITES(session["user"], search_id)
            pass
        if show_all != None:
            # DO ORDINARY THING
            pass
        if show_favourites != None:
            # GET SEARCH ALGORITHMS INNER JOIN FAVORUITES ON THIS USERS FAVOURITES
            algos = database.GET_SEARCH_FAVOURITES_BY_USERNAME(session["user"])

        if del_algo != None:
            search_id = database.GET_SEARCH_ALGO_ID_BY_NAME(del_algo)
            database.DEL_SEARCH_FAVOURITE(session["user"], search_id)
    
    #print(len(algos), algos)
    if len(algos) == 0:
        algos = database.GET_TOP_N_SEARCH_ALGORITHMS()
    
    search_query_details = []
    count = 0
    for i in algos:
        algoname = i[2] 
        print(count, algoname)
        search_query_details.append(database.GET_SEARCH_DETAILS_BY_ALGO_NAME(algoname))
        count += 1

    len_algos = len(algos)
    balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session["user"])

    return render_template(f"search_algorithms_page.html",
        algos=algos,
        len_algos=len_algos,
        search_query_details=search_query_details,
        
        daily_votes_left=daily_votes_left,
        monthly_votes_left=monthly_votes_left,
        yearly_votes_left=yearly_votes_left,
        balance=balance,
        daily_pool=daily_pool, 
        monthly_pool=monthly_pool, 
        yearly_pool=yearly_pool
    )


@app.route("/contact", methods=['GET'])
def contact():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    if "email" not in session:
        return redirect(url_for('login'))
    helpers.log_function("request", request, session_user=session['user'])
    balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session["user"])
    return render_template(f"contact.html",
        daily_votes_left=daily_votes_left,
        monthly_votes_left=monthly_votes_left,
        yearly_votes_left=yearly_votes_left,
        balance=balance,
        daily_pool=daily_pool, 
        monthly_pool=monthly_pool, 
        yearly_pool=yearly_pool
    )


@app.route("/FAQ", methods=['GET'])
def FAQ():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    if "email" not in session:
        return redirect(url_for('login'))
    helpers.log_function("request", request, session_user=session['user'])
    balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session["user"])
    return render_template(f"FAQ.html",
        daily_votes_left=daily_votes_left,
        monthly_votes_left=monthly_votes_left,
        yearly_votes_left=yearly_votes_left,
        balance=balance,
        daily_pool=daily_pool, 
        monthly_pool=monthly_pool, 
        yearly_pool=yearly_pool
    )


@app.route("/instructions", methods=['GET'])
def instructions():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    helpers.log_function("request", request)
    balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session["user"])
    return render_template(f"instructions.html",
        daily_votes_left=daily_votes_left,
        monthly_votes_left=monthly_votes_left,
        yearly_votes_left=yearly_votes_left,
        balance=balance,
        daily_pool=daily_pool, 
        monthly_pool=monthly_pool, 
        yearly_pool=yearly_pool

    )


@app.route("/leaderboards", methods=['GET'])
def leaderboards():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    helpers.log_function("request", request)
    balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session["user"])
    return render_template(f"leaderboards.html",
        daily_votes_left=daily_votes_left,
        monthly_votes_left=monthly_votes_left,
        yearly_votes_left=yearly_votes_left,
        balance=balance,
        daily_pool=daily_pool, 
        monthly_pool=monthly_pool, 
        yearly_pool=yearly_pool
    )


@app.route("/messages", methods=['GET'])
def messages():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    helpers.log_function("request", request)
    balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session["user"])
    return render_template(f"messages.html",
        daily_votes_left=daily_votes_left,
        monthly_votes_left=monthly_votes_left,
        yearly_votes_left=yearly_votes_left,
        balance=balance,
        daily_pool=daily_pool, 
        monthly_pool=monthly_pool, 
        yearly_pool=yearly_pool
    )


@app.route("/notifications", methods=['GET'])
def notifications():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    
    if "email" not in session:
        return redirect(url_for('login'))
    helpers.log_function("request", request, session_user=session['user'])
    
    user_id = database.GET_USER_ID(session["user"])
    notifications = database.GET_NOTIFICATIONS_BY_USER_ID(user_id)

    LIKES = []
    DISLIKES = []
    REPLY = []
    VOTES = []
    NEW_FOLLOWER = []
    #print(user_id)
    for i in notifications:
        #print(i)
        if i[0] == "LIKE":
            LIKES.append(i[1])
        if i[0] == "DISLIKE":
            DISLIKES.append(i[1])    
        if i[0] == "REPLY":
            REPLY.append(i[1])
        if i[0] == "VOTES":
            VOTES.append(i[1])        
        if i[0] == "NEW FOLLOWER":
            NEW_FOLLOWER.append(i[1])    
    balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session["user"])
    return render_template(f"notifications.html",
        LIKES=LIKES,
        DISLIKES=DISLIKES,
        REPLY=REPLY,
        VOTES=VOTES,
        NEW_FOLLOWER=NEW_FOLLOWER,
        
        daily_votes_left=daily_votes_left,
        monthly_votes_left=monthly_votes_left,
        yearly_votes_left=yearly_votes_left,
        balance=balance,
        daily_pool=daily_pool, 
        monthly_pool=monthly_pool, 
        yearly_pool=yearly_pool
    )


@app.route("/tribunal", methods=['GET','POST'])
def tribunal():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    if "email" not in session:
        return redirect(url_for('login'))
    helpers.log_function("request", request, session_user=session['user'])
    
    search_json = {}
    json_search_clauses = "None"
    search = "None"

    if request.method == 'POST':
        search = request.form.get("search")   
        reset = request.form.get("reset")
        save_algo = request.form.get("save_algo")
        
        if save_algo != "None" and save_algo != None:
            returned_search_arguments = request.form.get("search_arguments")
            print("CURRENT ARGS TO BE SAVED", returned_search_arguments)
            database.SAVE_CURRENT_ALGO(returned_search_arguments)
            
        if reset != "None" and save_algo != None:
            print("CLICKED RESET")
            return redirect(url_for("home"))
        

        date_check = request.form.get("date_check")  
        order_check = request.form.get("order_check")  
        and_or_clauses, where_clauses, hi_eq_low, num_search_text = helpers.GET_ALL_QUERY_INFO_FROM_REQUEST_FORM(request)
        clauses_dict = [
            and_or_clauses, 
            where_clauses, 
            hi_eq_low, 
            num_search_text
        ]
        json_search_clauses = database.TURN_CLAUSES_INTO_JSON(search, date_check, order_check, clauses_dict, session["user"])
    
    # GRAB THE ARGS FROM QUERY BEFORE THE CURRENT PAGE [GET OR POST]
    returned_search_arguments = request.form.get("search_arguments")
    # print(returned_search_arguments)

    new_json_search_clauses = helpers.COMPOSE_SEARCHARGS_AND_JSONCLAUSE(returned_search_arguments, json_search_clauses)
    '''
    print("COMPOSE_SEARCHARGS_AND_JSONCLAUSE")
    print(new_json_search_clauses)
    print("===================================")
    '''
    page_no = request.form.get("page_number")
    #print("CURRENT PAGE NUMBER:", type(page_no), page_no)
    # print("===================================")

    if page_no == None or str(page_no) == "None":
        page_no = 1

    #TODO: what I may have to do is do a similar query to the one below, but just returning a path list, grab all the paths that meet the criteria, then stick is back into
    # a function that returns the correct info with the search value in there as welll

    file_ids_list, usernames_list, paths_list, dates_list, post_sources_list, daily_left, monthly_left, yearly_left, day_votes, month_votes, year_votes, user_balance, dailypool, monthlypool, yearlypool, daily_votes_singular,  monthly_votes_singular, yearly_votes_singular, likes, dislikes,searcher_has_liked,searcher_has_disliked, num_replies, uploader_is_subbed, search_arguments = database.universal_dataset_function(search_type="home", page_no=page_no, search_user=session["user"], custom_clauses=new_json_search_clauses, tribunal=True)
    # print("hello??", num_replies)
    #print(searcher_has_liked)
    #print(searcher_has_disliked)
    
    #FOR DIABLING OR ACTIVATING SCROLL LOGIC
    numposts = len(file_ids_list)
    if numposts < 29: # this 100 number needs to be better coded, hard coding is going to cause issues
        can_scroll = False
    else:
        can_scroll = True


    # GRAB STUFF IT'S IT'S EMPTY EITHE RWAY
    if len(file_ids_list) == 0:
        print("IS EMPTY")
        user_balance, daily_left, monthly_left, yearly_left, dailypool, monthlypool, yearlypool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session['user'])
    
    username_len = len(usernames_list)
    # print("USERNAMES LEN", username_len, usernames_list)

    text_list = []
    age_18_list = []
    source_list = []
    image_path_list = []
    distro_details_list = []
    for i in range(len(usernames_list)): # GETTING POST INFO FROM PATH
        my_path = f"static/#UserData/{usernames_list[i]}/files/{paths_list[i]}"
        post_text, post_age_18, post_sources, post_image_path, distro_details = helpers.get_postinfo_from_path(my_path)
        age_18_list.insert(i, post_age_18)
        source_list.insert(i, post_sources)
        text_list.insert(i, post_text)
        image_path_list.insert(i, post_image_path)
        distro_details_list.insert(i,distro_details)

    lengths_of_text_files = []
    for i in text_list:
        lengths_of_text_files.append(len(i))

    # GET SEARCH FAVOURITES
    search_favourites = database.GET_SEARCH_FAVOURITES_BY_USERNAME(session["user"])
    favourites_len = len(search_favourites)
    if favourites_len > 20:
        favourites_len = 20

    return render_template('tribunal.html',
                            message="tribunal.html page",
                           
                            usernames_list=usernames_list,
                            file_ids_list=file_ids_list,
                            session_username=session["user"],
                            username_len=username_len,
                           
                            paths_list=paths_list,
                            dates_list=dates_list,
                            post_sources_list=post_sources_list,
                            likes=likes,
							dislikes=dislikes,
							searcher_has_liked=searcher_has_liked, 
							searcher_has_disliked=searcher_has_disliked,
                            num_replies=num_replies,
                            uploader_is_subbed=uploader_is_subbed,
                            
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
                            distro_details_list=distro_details_list,
                            
                            search_arguments=search_arguments,
                            page_no=page_no,
                            can_scroll=can_scroll,
                            
                            search_favourites=search_favourites,
                            favourites_len=favourites_len,
                            
                           )



@app.route("/patch_notes", methods=['GET'])
def patch_notes():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    if "email" not in session:
        return redirect(url_for('login'))
        
    helpers.log_function("request", request, session_user=session['user'])
    balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session["user"])

    return render_template(f"patch_notes.html",
        daily_votes_left=daily_votes_left,
        monthly_votes_left=monthly_votes_left,
        yearly_votes_left=yearly_votes_left,
        balance=balance,
        daily_pool=daily_pool, 
        monthly_pool=monthly_pool, 
        yearly_pool=yearly_pool
    )


@app.route("/newsletter", methods=['GET'])
def newsletter():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    if "email" not in session:
        return redirect(url_for('login'))
    helpers.log_function("request", request, session_user=session['user'])
    balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS(session["user"])
    return render_template(f"newsletter.html",

    )

@app.route("/cover_page", methods=['GET'])
def cover_page():
    helpers.log_function("request", request)
    balance, daily_votes_left, monthly_votes_left, yearly_votes_left, daily_pool, monthly_pool, yearly_pool = database.GET_VOTES_AND_BALANCE_AND_PAYOUTS("")
    return render_template(f"cover_page.html",
        daily_pool=daily_pool, 
        monthly_pool=monthly_pool, 
        yearly_pool=yearly_pool
    )

@app.route("/edit_bio", methods=['GET', "POST"])
def edit_bio():
    if helpers.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    
    if "email" not in session:
        return redirect(url_for('login'))
    
    helpers.log_function("request", request, session_user=session['user'])
    new_bio = request.form.get("edit_bio")  
    new_bio = helpers.POST_TEXT_CHECK(new_bio)
    helpers.CHANGE_BIO(new_bio, session['user'])
    return redirect(url_for("user_profile"))


if __name__ == '__main__':
    #SUBTITLE Network Societey and it's Future
    
    #my_port = 443
    
    host = "0.0.0.0" #could be local host
    # http://165.227.35.71:8088/
    # database.USER_FULL_RESET()

    #TURNING CONSOLE LOGGING ON OR OFF
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    thread = Thread(target = distribution_algorithm.TESTING_TIMING, args = ())
    thread.start()

    app.run(host=host, port="8096", debug=False, use_reloader=False)  # host is to get off localhost
    #serve(app, host=host,port="8091")    

    # If the debugger is on, I can change my files in real time after saving
    pass
