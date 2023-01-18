from flask import *
from os import *
import base64
import inspect

import python.MODULES as modules

# CONFIG
TEMPLATE_DIR = path.abspath('./templates')
STATIC_DIR = path.abspath('./static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = 'demokey'

@app.route('/', methods=['GET', 'POST'])  # homepage
def home():
    return redirect(url_for('post_logic', person_id=0,page_no=0 ))
    
@app.route("/<person_id>/<page_no>", methods=['GET', 'POST'])
def post_logic(person_id, page_no):
    modules.log_function("request", request)
    #if "email" not in session: 
    #    return redirect(url_for("login"))
    
    '''
    first_time = modules.CHECK_IF_SESSION_USER_FIRST_TIME(session["id"])
    if first_time:
        return redirect(url_for("first_time"))
    '''
    try:
        username = session["user"]
        session_id = session["id"]
    except:
        username = "Trial"
        session_id = 2
    
    query, posts, new_page_no, posts_per_page, can_scroll, person_id, tag_requests_ = modules.UNIVERSAL_FUNCTION(
        searcher=username,
        page_no=int(page_no)+1,
        person_id=person_id,
        )
    
    if str(person_id) != "0":
        person_page = "True"
        person_name = modules.GET_PERSON_NAME_BY_ID(person_id) 
    else:
        person_page = "False"
        person_name = "Home"
        
    offset_calc = int(int(page_no) * int(posts_per_page))
    return render_template('home.html',
        query=query,                   
        searcher=username,                   
        posts=posts,
        num_posts=len(posts),
        
        person_id=person_id,
        page_no=new_page_no,
        offset_calc=offset_calc,
        can_scroll=can_scroll,
        posts_per_page=posts_per_page,
        coming_from_person_page=person_page,
        person_name=person_name,
        subscribers=modules.GET_NUM_SUBSCRIBERS_BY_PERSON_ID(person_id),
        am_subscribed = modules.CHECK_IF_SUBSCRIBED(person_id, session_id)
    )
    
@app.route("/post_tribunal/<page_no>", methods=['GET', "POST"])
def post_tribunal(page_no):
    modules.log_function("request", request)
    if "email" not in session: 
        return redirect(url_for("login"))

    try:
        session_id = session["id"] 
        session_user = session["user"] 
    except:
        session_id = 2
        session_user = "Trial"
    
    query, posts, new_page_no, posts_per_page, can_scroll, person_id, tag_requests_ = modules.UNIVERSAL_FUNCTION(
        searcher=session["user"], 
        page_no=int(page_no)+1,
        post_tribunal=True
    )
    offset_calc = int(int(page_no) * int(posts_per_page))

    can_vote = modules.CHECK_USER_IS_GLOBAL_ADMIN(session_id)
    
    return render_template('home.html',
        query=query,                   
                           
        posts=posts,
        num_posts=len(posts),
        
        person_id=person_id,
        page_no=new_page_no,
        offset_calc=offset_calc,
        can_scroll=can_scroll,
        posts_per_page=posts_per_page,
        coming_from_tribunal="true",
        can_vote=can_vote,
        ADMINISTRATOR=modules.CHECK_IF_IT_IS_ME(session_id)
        #fucking hate javascript
    ) 
 
@app.route("/tag_tribunal/<page_no>", methods=['GET', "POST"])
def tag_tribunal(page_no):
    print("TRIBUNAL TYPE======================================================")
    modules.log_function("request", request)
    if "email" not in session: 
        return redirect(url_for("login"))

    try:
        session_id = session["id"] 
        session_user = session["user"] 
    except:
        session_id = 2
        session_user = "Trial"
    
    query, posts, new_page_no, posts_per_page, can_scroll, person_id, tag_requests = modules.UNIVERSAL_FUNCTION(
        searcher=session["user"], 
        page_no=int(page_no)+1,
        tag_tribunal=True,
    )
    offset_calc = int(int(page_no) * int(posts_per_page))

    can_vote = modules.CHECK_USER_IS_GLOBAL_ADMIN(session_id)
        
    return render_template('home.html',
        query=query,                   
                           
        posts=posts,
        num_posts=len(posts),
        
        person_id=person_id,
        page_no=new_page_no,
        offset_calc=offset_calc,
        can_scroll=can_scroll,
        posts_per_page=posts_per_page,
        coming_from_tag_tribunal="true",
        can_vote=can_vote,
        ADMINISTRATOR=modules.CHECK_IF_IT_IS_ME(session_id),
        tag_requests=tag_requests
    ) 
 
 
@app.route("/favourites/<page_no>", methods=['GET', 'POST'])
def favourites(page_no):
    modules.log_function("request", request)
    if "email" not in session: 
        return redirect(url_for("login"))
    
    try:
        session_id = session["id"]
        session_user = session["id"]  
    except:
        session_id = 2
    
    
    
    query, posts, new_page_no, posts_per_page, can_scroll, person_id, tag_requests_ = modules.UNIVERSAL_FUNCTION(
        searcher=session["user"], 
        page_no=int(page_no)+1,
        favourites=True
    )
    offset_calc = int(int(page_no) * int(posts_per_page))
    
    return render_template('home.html',
        query=query,                   
                           
        posts=posts,
        num_posts=len(posts),
        
        person_id=person_id,
        page_no=new_page_no,
        offset_calc=offset_calc,
        can_scroll=can_scroll,
        posts_per_page=posts_per_page,
        coming_from_favourites= "true" #fucking hate javascript
    )    
    
@app.route("/user_profile/<user_profile_name>/<page_no>", methods=['GET', 'POST'])
def user_profile(user_profile_name, page_no):
    '''
    # THERE IS SOMETHING BUGGY GOING ON IN THIS FUNCTION
    # GET_USER_ID_FROM_NAME(username)
    THIS seems to get run twice, and the second time returns the wrong name
    doesnt seem to effect the query tho
    ''' 
    modules.log_function("request", request)
    if "email" not in session: 
        return redirect(url_for("login"))  
    
    try:
        session_id = session["id"] 
        session_user = session["user"] 
    except:
        session_id = 2
        session_user = "Trial"
    
    print("user_profile_name", user_profile_name) 
    
    if user_profile_name == "home_profile":
        user_profile_id = session_id
    else:
        user_profile_id = modules.GET_USER_ID_FROM_NAME(user_profile_name)
    
    query, posts, new_page_no, posts_per_page, can_scroll, person_id, tag_requests_ = modules.UNIVERSAL_FUNCTION(
        searcher=session_user, 
        page_no=int(page_no)+1,
        profile_id=user_profile_id
    )
    offset_calc = int(int(page_no) * int(posts_per_page))
    user_strikes = modules.GET_USER_STRIKES_BY_ID(user_profile_id)
    return render_template('home.html',
        query=query,                   
                           
        posts=posts,
        num_posts=len(posts),
        
        person_id=person_id,
        page_no=new_page_no,
        offset_calc=offset_calc,
        can_scroll=can_scroll,
        posts_per_page=posts_per_page,
        user_profile_name=user_profile_name,
        coming_from_profile= "True", #fucking hate javascript
        user_profile_id=user_profile_id,
        
        username=modules.GET_USER_NAME_FROM_ID(user_profile_id),
        session_user=session_user,
        
        user_strikes=user_strikes,
        
        # I THINK THE NAMES OF THESE ARE WRONG OT SOME ASPECT OF THIS IS WRONG
        #BUT IT WORKS ANYWAY
        followers=modules.GET_FOLLOWERS_BY_USER_ID(user_profile_id),
        following=modules.GET_FOLLOWING_BY_USER_ID(user_profile_id)
    )
    
@app.route("/person/<person_id>", methods=['GET', 'POST'])
def person(person_id):
    modules.log_function("request", request)
    if "email" not in session: 
        return redirect(url_for("login"))
    
    try:
        session_id = session["id"] 
        session_user = session["user"] 
    except:
        session_id = 2
        session_user = "Trial"
                
    posts = modules.UNIVERSAL_FUNCTION(searcher=session_user, person_id=person_id)
    
    return render_template('home.html',
        posts=posts,
        
    )
    
@app.route("/add_connection/<User_id>", methods=['POST'])
def add_connection(User_id):
    modules.log_function("request", request)
    if "email" not in session: 
        return redirect(url_for("login"))    
        
    if not modules.GET_ALL_INTERACTIONS(session["id"]):
        return render_template(f"spam_page.html")
    
    modules.INSERT_CONNECTION(session["id"], User_id) 
    
    followers = modules.GET_FOLLOWERS_BY_USER_ID(3)
    return render_template("connection_change.html",
        followers=followers)

@app.route("/remove_connection/<User_id>", methods=['POST'])
def remove_connection(User_id):
    modules.log_function("request", request)
    if "email" not in session: 
        return redirect(url_for("login"))
    
    if not modules.GET_ALL_INTERACTIONS(session["id"]):
        return render_template(f"spam_page.html")
    
    modules.DELETE_CONNECTION(session["id"], User_id) 
    followers = modules.GET_FOLLOWERS_BY_USER_ID(3)
    return render_template("update_connection.html",
        followers=followers)
    
@app.route("/people/<sort_method>/<letter>", methods=['GET', 'POST'])
def people(sort_method, letter):
    #if "email" not in session: 
    #    return redirect(url_for("login"))
    modules.log_function("request", request)
    
    people = modules.GET_ALL_PEOPLE_TESTING(letter=letter)
    people = list(modules.triple_split(people, 3))

    alpha_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    return render_template("people.html",
        people=people,
        alpha_chars=alpha_chars
        )

@app.route("/request_form/<request_type>", methods=['GET', 'POST'])
def request_form(request_type):
    if "email" not in session: 
        return redirect(url_for("login"))
    modules.log_function("request", request)
    #print("request_type", request_type)
    if request.method == "POST":     
        if request_type == "post":
            
            post_title = request.form["post_title"]
            post_title = modules.clean_title(post_title)
            post_title = post_title.strip()
            #print("post_title", post_title)
            
            description = request.form["description"]
            description = modules.COMMENT_TEXT_CHECK(description)
            description = description.strip()
            #print("description", description)
            
            link = request.form["post_link"]
            link = link.strip()
            #print("link", link)
            
            person_name = request.form["chosen_name"]
            people = person_name.split(",")[:-1]
            print("person_name", people)
            
            # CHANGE TO POST
            # print("i got here")
            if not modules.GET_ALL_INTERACTIONS(session["id"]):
                return render_template(f"spam_page.html")
            
            modules.INSERT_POST(Post_title=post_title, 
                                Post_description=description, 
                                Post_link=link, 
                                Post_live="false", 
                                Person=people, 
                                User_id=session["id"]
                                ) 
        elif request_type == "person":
            
            person_post_title = request.form["post_title"]
            person_post_title = person_post_title.strip()
            #post_title = modules.clean_title(post_title)
            #print("post_title", post_title)
            
            person_description = request.form["description"]
            person_description = modules.COMMENT_TEXT_CHECK(person_description)
            person_description = person_description.strip()
            #print("description", description)
            
            person_link = request.form["post_link"]
            person_link = person_link.strip()
            # print("link", link)

            person_person_name = request.form["person_name"]
            person_person_name = person_person_name.split(",")[:-1]
            print("OG", person_person_name)
            
            upgraded_person_person_name = []
            for i in person_person_name:
                j = i.strip()
                if modules.CHECK_INJECTION(j): #this might be exessive
                    upgraded_person_person_name.append(j)
                
            print("NEW", upgraded_person_person_name)
            
            modules.log_function(msg_type="test", log_string=str(person_person_name), function_name=f"INSERT_PERSON")
            
            # print("person_name:", person_person_name)
            modules.INSERT_POST(Post_title=person_post_title, 
                                Post_description=person_description, 
                                Post_link=person_link, 
                                Post_live="false", 
                                Person=person_person_name, 
                                User_id=session["id"]
                )
            
    return render_template(f'request_form.html',
        request_type=request_type
    )

@app.route("/search_text_by_category/<type>", methods=['GET'])
def search_text_by_category(type):
    if "email" not in session: 
        return redirect(url_for("login"))    
    # GOTTA BE A BETTER WAY to get the query
    # print("request.url", request.url)
    query_text = str(request.url).split("name=")[1]
    
    if type == "user":
        print("1===============================")
        if modules.CHECK_INJECTION(query_text):
            users = modules.GET_USERS_BY_TEXT(query_text)
        else:
            users = ["None"]
        return render_template(f'update_user_search.html',
            users=users,
            message="None"
        )
    elif type == "algorithm":
        algorithm = modules.CHECK_ALGO_FUNCTION(query_text, session["user"])
        return render_template(f'update_user_search.html',
            users="None",
            algorithm=algorithm
            
        )
    elif type == "search_homepage":
        # query_text = request.form["person_name"]
        print("query_text",query_text)
        if modules.CHECK_INJECTION(query_text):
            new_algos, can_scroll, page_no = modules.GET_SEARCH_ALGORITHM_DETAILS(user_id=session['id'], search_type="home", limit_search=query_text)
        else:
            new_algos, can_scroll, page_no = modules.GET_SEARCH_ALGORITHM_DETAILS(user_id=session['id'], search_type="home")
        # print(new_algos)
        search_id, search_name = modules.GET_USER_CURRENT_SEARCH_ALGO_BY_ID(User_id=session['id'])
        return render_template(f"search_algo_home.html",
            algos=new_algos,
            search_type="home",
            search_id=search_id, 
            search_name=search_name,
            
            can_scroll=can_scroll,
            page_no=int(page_no)+1
        )   
    elif type == "chat_room_additions":
        users = modules.GET_REAL_USERS_BY_TEXT(query_text, session["id"])
        return render_template(f'update_user_search.html',
            users=users 
        )
    elif type == "chat_room_titles":
        # users = modules.GET_REAL_USERS_BY_TEXT(query_text)
        if modules.CHECK_CHAT_ROOM_NAME(query_text) == "True":
            chat_room_answer = "True"
        else:
            chat_room_answer = "False"
        # print("query_text", query_text)
        return render_template(f'update_user_search.html',
            users="None",
            message="None",
            algorithm="None",
            chat_room_answer=chat_room_answer, 
        )
    elif type == "chat_room_name":
        print("chat room name")

        chat_rooms_with_x_names = modules.GET_CHAT_ROOM_NAMES_BY_TEXT(query_text, user_id=session["id"])
        # chat_rooms_with_x_names = ["HELLO", "SHMELLO"]
        
        return render_template(f'update_user_search.html',
            users="None",
            message="None",
            algorithm="None",
            chat_room_answer="None", 
            chat_rooms_with_x_names=chat_rooms_with_x_names
        )
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    modules.log_function("request", request)
    if "email" in session:
        email = session["email"]  
        return redirect(url_for("home"))
    
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        #print(email)
        #print(password)
        if modules.CHECK_INJECTION(email) and modules.CHECK_INJECTION(password):
            # print(1)
            signed_in = modules.validate_user_from_session(email, password)
            
            if signed_in[0]: # First element in dict is bool for success/failure
                session["id"] = signed_in[1]
                session["user"] = signed_in[2]
                session["email"] = email
                
                if modules.CHECK_FIRST_TIME(session["id"]):
                    return redirect(url_for("intro_page"))
                else:
                    return redirect(url_for("home"))
            else:
                return render_template('login.html', message="wrong email or password, try again")
    return render_template('login.html', message="")

@app.route('/logout', methods=['GET'])
def logout():
    modules.log_function("request", request)
    # DON'T KNOW HOW WELL THIS ACTUALLY WORKS
    session.pop("email", None) 
    session.pop("user", None)
    session.pop("password", None)
    return redirect(url_for("login"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    modules.log_function("request", request)
    if "email" in session:
        return redirect(url_for("home"))
    if request.method == 'GET':
        sign_up_message = 'Please sign up'
        return render_template('register.html', message=sign_up_message)

    if request.method == 'POST':
        my_dict = request.form.to_dict(flat=False)
        try:
            registering_username = my_dict['username'][0]
            password = my_dict['password'][0]
            email = my_dict['email'][0]
            
            if modules.INSERT_USER(registering_username, password, email):
                return redirect(url_for('login'))
            else:
                return render_template('register.html', 
                return_message="\nEither name already exists, has profanity, or looks like an injection."
                )
  
        except Exception as e:
            modules.log_function("error", e, function_name="register")
        return redirect(url_for("login"))
   
@app.route("/password_recovery", methods=['GET', 'POST'])
def password_recovery():
    modules.log_function("request", request)
    if request.method == "POST":
        recovery_email = request.form["email"]
        modules.CREATE_AND_SEND_ONE_TIME_PASS_EMAIL(recovery_email)
        return redirect(url_for('password_reset'))
    return render_template(f"password_recovery.html")

@app.route("/password_reset", methods=['GET', 'POST'])
def password_reset():
    modules.log_function("request", request)
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        repeat_pass = request.form["check_password"]
        one_time_pass = request.form["One Time Password"]
        current_one_time_pass = modules.GET_ONE_TIME_PASS(email)
        if modules.CHECK_INJECTION(email) and modules.CHECK_INJECTION(password):
            if (password == repeat_pass) and (one_time_pass == current_one_time_pass):
                modules.CHANGE_PASSWORD( email, password)
                return redirect(url_for("login"))
            else:
                return render_template(f"password_reset.html", message="Passwords are not the same! \nOr One Time Password is Incorrect!")
        else:
            return render_template(f"password_reset.html", message="Or Email/Password is failing hack tests.")
    
    # GET REQUEST
    else:
        return render_template(f"password_reset.html")

@app.route("/word_tribunal", methods=['GET', "POST"])
def word_tribunal():
    if "email" not in session:
        return redirect(url_for('login'))
    modules.log_function("request", request, session_user=session['user'])
    
    if request.method == "POST":
        # THIS ALL ASSUMES THERE ARE REALLY ONLY 2 TYPES OF POST REQUESTS
        new_bad_word = request.form.get("bad_word")
        if modules.CHECK_INJECTION(new_bad_word):
            # print("new_bad_word", new_bad_word)
            if new_bad_word != None:
                if not modules.GET_ALL_INTERACTIONS(session["id"]):
                    return render_template(f"spam_page.html")
                modules.INSERT_TRIBUNAL_WORD(new_bad_word.lower(), session["id"]) 
            else:
                keep_phrase = request.form.get("keep_phrase")
                block_phrase = request.form.get("block_phrase")
                
                vote_type = None
                
                if keep_phrase != None:
                    phrase = keep_phrase.split(":")[0]
                    vote_type = "UP"
                else:
                    phrase = block_phrase.split(":")[0]
                    vote_type = "DOWN"
                word_id = modules.GET_WORD_PHRASE_ID_BY_NAME(phrase)
                modules.INSERT_INTO_PROFANITY_LIST_VOTES(word_id, session["id"], vote_type)
  
    blocked_words = modules.GET_ALL_TRIBUNAL_WORDS()
    # print(blocked_words)
    return render_template(f"word_tribunal.html",
        blocked_words=blocked_words,
        user_id=session["id"]
    )

@app.route("/update_like/<Post_id>", methods=['GET', 'POST'])
def update_like(Post_id):
    if "email" not in session: 
        return redirect(url_for("login"))    
    modules.log_function("request", request)
    if not modules.GET_ALL_INTERACTIONS(session["id"]):
        return render_template(f"spam_page.html")
    modules.LIKE_LOGIC(Post_id, session["id"]) 
    return render_template(f"update_like.html",
        likes=modules.GET_NUM_LIKES_BY_POST_ID(Post_id))
    
@app.route("/update_subscribe/<Person_id>", methods=['GET', 'POST'])
def update_subscribe(Person_id):
    if "email" not in session: 
        return redirect(url_for("login"))    
    modules.log_function("request", request)
    if not modules.GET_ALL_INTERACTIONS(session["id"]):
        return render_template(f"spam_page.html")
    
    modules.SUBSCRIBE_LOGIC(Person_id, session["id"]) 
    return render_template(f"update_sub.html",
        subscribers=modules.GET_NUM_SUBSCRIBERS_BY_PERSON_ID(Person_id),
        am_subscribed = modules.CHECK_IF_SUBSCRIBED(Person_id, session["id"])
        )
         

   
@app.route("/update_comment_like/<Comment_id>", methods=['GET', 'POST'])
def update_comment_like(Comment_id):
    if "email" not in session: 
        return redirect(url_for("login"))    
    modules.log_function("request", request)
    if not modules.GET_ALL_INTERACTIONS(session["id"]):
        return render_template(f"spam_page.html")
    
    modules.COMMENT_LIKE_LOGIC(Comment_id, session["id"])
    return render_template(f"update_comment_likes.html",
        comment_likes=modules.GET_NUM_COMMENT_VOTES_BY_ID(Comment_id),
        Comment_id=Comment_id
        )
    
@app.route("/update_follow/<user_profile_id>", methods=['GET', 'POST'])
def update_follow(user_profile_id):
    if "email" not in session: 
        return redirect(url_for("login"))    
    modules.log_function("request", request)
    if not modules.GET_ALL_INTERACTIONS(session["id"]):
        return render_template(f"spam_page.html")
    
    modules.CONNECTION_LOGIC(session["id"], user_profile_id) 
    return render_template(f"update_follow.html",
        new_following_count=len(modules.GET_FOLLOWERS_BY_USER_ID(user_profile_id))
        )

@app.route("/update_search_fave/<algo_id>", methods=['GET', 'POST'])
def update_search_fave(algo_id):
    if "email" not in session: 
        return redirect(url_for("login"))
    # print(algo_id)
    modules.log_function("request", request)
    if not modules.GET_ALL_INTERACTIONS(session["id"]):
        return render_template(f"spam_page.html")
    modules.SEARCH_FAVE_LOGIC(algo_id, session["id"]) 
    return render_template(f"update_fave_search.html",
        search_faves=modules.GET_NUM_SEARCH_FAVES_BY_SEARCH_ID(algo_id)
        )

@app.route("/update_fave/<Post_id>", methods=['GET', 'POST'])
def update_fave(Post_id):
    if "email" not in session: 
        return redirect(url_for("login"))    
    modules.log_function("request", request)
    if not modules.GET_ALL_INTERACTIONS(session["id"]):
        return render_template(f"spam_page.html")
    
    modules.FAVE_LOGIC(Post_id, session["id"])
    return render_template(f"update_fave.html",
        faves=modules.GET_NUM_FAVES_BY_POST_ID(Post_id)
        )
    
@app.route("/update_view/<Post_id>", methods=['GET', 'POST'])
def update_view(Post_id):
    if "email" not in session: 
        return redirect(url_for("login"))    
    modules.log_function("request", request)
    modules.INSERT_VIEWS(Post_id, session["id"]) # dont need to check here because views has internal clock
    return render_template(f"update_view.html",
        views=modules.GET_NUM_VIEWS_BY_POST_ID(Post_id)
        )
   
@app.route("/update_comment/<Post_id>", methods=['GET', 'POST'])
def update_comment(Post_id):
    if "email" not in session: 
        return redirect(url_for("login"))    
    modules.log_function("request", request)
    input_field = request.form.get("input_field")
    how_many = 11
    
    print("comment update:")
    print("POST ID       :", Post_id)
    print("input_field   :", input_field)
    print("howmany       :", how_many)
    if modules.CHECK_INJECTION(input_field):
        if not modules.GET_ALL_INTERACTIONS(session["id"]):
            return render_template(f"spam_page.html")
        modules.INSERT_COMMENTS(Post_id=Post_id, User_id=session["id"], Comment_text=input_field) 
    
    return redirect(url_for('comment_section', Post_id=Post_id,how_many=how_many, order="date"))

@app.route("/update_post_html/<Post_id>", methods=['GET', 'POST'])
def update_post_html(Post_id):
    if "email" not in session: 
        return redirect(url_for("login"))    
    modules.log_function("request", request)
    if request.method == 'POST':
        # print("Post_id", Post_id)
        post_link_embed = request.form.get("post_link_embed")
        print("post_link_embed", post_link_embed)
        modules.UPDATE_POST_HTML_BY_ID(Post_id, post_link_embed)

    
    return render_template(f"update_post.html",
        updated_html=modules.GET_POST_HTML_BY_ID(Post_id)
        )
    
@app.route("/update_post_tribunal/<Post_id>/<approval>", methods=['GET', 'POST'])
def update_post_tribunal(Post_id, approval):
    if "email" not in session: 
        return redirect(url_for("login"))
    modules.log_function("request", request)
    # print("Post_id", Post_id)
    # print("approval type", approval)
    if modules.CHECK_IF_IT_IS_ME(session["id"]):
        if approval == "approve":
            modules.UPDATE_POST_TO_LIVE(Post_id)
            modules.UPDATE_PERSON_TO_LIVE(modules.GET_PERSON_ID_BY_POST_ID(Post_id))
        elif approval == "deny":
            modules.DELETE_POST(Post_id)
            #if modules.CHECK_IF_IT_IS_ME(session["id"]):   
            #    modules.UPDATE_POST_TO_LIVE(Post_id)
        elif approval == "report_uploader":
            modules.UPDATE_USER_STRIKES(session["id"])
            modules.DELETE_POST(Post_id)
        elif approval == "delete_person":
            person_id = modules.GET_PERSON_ID_BY_POST_ID(Post_id)
            modules.UPDATE_USER_STRIKES(session["id"])
            modules.DELETE_POST(Post_id)
            modules.DELETE_PERSON(person_id)
    return render_template(f"update_post.html",
        updated_html=modules.GET_POST_HTML_BY_ID(Post_id)
        )


@app.route("/comment_section/<Post_id>/<how_many>/<order>", methods=['GET', 'POST'])
def comment_section(Post_id, how_many, order):
    if "email" not in session: 
        return redirect(url_for("login"))    
    modules.log_function("request", request)
    transformed_comments = modules.TRANSFRM_COMMENT_ARRAY_INTO_HTML(modules.GET_N_COMMENTS(Post_id=Post_id, N=how_many, new_comment=modules.JANKY_COMMENT_CHECK(how_many), check_order=order))
    
    return render_template(f"update_comments.html",
        comments=transformed_comments,
        )

@app.route("/contact", methods=['GET'])
def contact():
    #if "email" not in session:
    #    return redirect(url_for('login'))

    try:
        session_id = session["id"] 
        session_user = session["user"] 
    except:
        session_id = 2
        session_user = "Trial"
    modules.log_function("request", request, session_user=session_user)
    
    return render_template(f"contact.html",
    )

@app.route("/structure_search_by_phrase/<page_no>/<phrase_again>", methods=['GET', 'POST'])
def structure_search_by_phrase(page_no, phrase_again):
    #if "email" not in session: 
    #    return redirect(url_for("login"))   
    try:
        session_id = session["id"] 
        session_user = session["user"] 
    except:
        session_id = 2
        session_user = "Trial" 
        
    modules.log_function("request", request, session_user=session_user)
    searched_value = ""
    if request.method == "POST":
        try: 
            ''' 
            THIS TRY CATCH BASICALLY SAYS GET WHATS IN THE SEARCH BAR
            IF YOU'RE GETTING NOTHING FROM THE FORM, BUT STILL AT THIS FUNCTION,
            THEN YOU'RE DOING A SCROLL POST REQUEST
            SO REPLACE IT WITH THE TEXT IN THE URL
            '''
            searched_value = request.form["searched_value"]
        except Exception as e:
            searched_value = phrase_again

    if len(searched_value) == 0 :
        return redirect(url_for('post_logic', person_id=0,page_no=0 ))
    
    query, posts, new_page_no, posts_per_page, can_scroll, person_id, tag_requests_ = modules.UNIVERSAL_FUNCTION(
        searcher=session_user,
        page_no=int(page_no)+1,
        search_phrase=searched_value
        )
    
    offset_calc = int(int(page_no) * int(posts_per_page))

    return render_template('home.html',
        query=query,                   
                           
        posts=posts,
        num_posts=len(posts),
        
        person_id=person_id,
        page_no=new_page_no,
        offset_calc=offset_calc,
        can_scroll=can_scroll,
        posts_per_page=posts_per_page,
        coming_from_search="true",
        searcher=session_user,
        search_phrase=searched_value
    )        

@app.route("/search_algo_create", methods=['GET', 'POST'])
def search_algo_create():
    if "email" not in session: 
        return redirect(url_for("login"))    
    modules.log_function("request", request, session_user=session['user'])

    array_of_order_clauses = []
    array_of_where_clauses = []

    if request.method == "POST":
        if not modules.GET_NUM_SEARCH_ALGOS_TODAY_BY_ID(session["id"]):
                return render_template(f"search_algo_create.html",
                    failure_message="Already created 2 today, wait until tomorrow."
            )
        like_bias = request.form["likes_bias"]
        views_bias = request.form["views_bias"]
        faves_bias = request.form["faves_bias"]
        comments_bias = request.form["comments_bias"]
        comment_likes_bias = request.form["comment_likes_bias"]
        # subscriptions_bias = request.form["subscriptions_bias"]
        
        bias_dict = {
            "like_bias":like_bias, 
            "views_bias":views_bias, 
            "faves_bias":faves_bias, 
            "comments_bias":comments_bias, 
            "comment_likes_bias":comment_likes_bias
            # "subscriptions_bias":subscriptions_bias
        }
        for key,value in request.form.items():
            # print(key, value)
            if "Order" in key:
                array_of_order_clauses.append(key)
            elif "Where_" in key:
                # print("ADDING TO WHERE CLAUSE", key, value)
                array_of_where_clauses.append([key, value])
            elif key == "algo_name":
                algo_name = value
        # exit(0)
        #TODO: IMPLEMENT WHERE CLAUSES ONN THE BASIS OF THOSE CRITERION
        # print(f"ORDER CLAUSES\n{array_of_order_clauses}")
        # print("GOT HERE 2")
        full_order_by = modules.TRANSFER_SEARCH_ORDER_CLAUSE_TO_QUERY(array_of_order_clauses, bias_dict)
        # print(full_order_by)
        full_where = modules.TRANSFER_SEARCH_WHERE_TO_QUERY(array_of_where_clauses)
        algorithm = modules.CHECK_ALGO_FUNCTION(algo_name, session["user"])

        if algorithm.lower() == "False".lower():
            return render_template(f"search_algo_create.html",
                message="""<div class="text-danger">Algorithm Name Unavailable</div>"""  
            ) 
        
        #print("algo_name     :", algo_name)
        #print("full_order_by :", full_order_by)
        #print("full_where", full_where)
        modules.INSERT_SEARCH_ALGORITHM(Search_algorithm_name=algo_name, Search_where_clause=full_where, Search_order_clause=full_order_by, User_id=session["id"])
        return redirect(url_for('search_algo_home', search_type="home", page_no="0"))
                
    return render_template(f"search_algo_create.html",
    )
    
@app.route("/search_algo_home/<search_type>/<page_no>", methods=['GET', 'POST'])
def search_algo_home(search_type, page_no):
    if "email" not in session: 
        return redirect(url_for("login"))    
    print(page_no, "HERE")
    
    modules.log_function("request", request, session_user=session['user'])
    algos, can_scroll, new_page_no = modules.GET_SEARCH_ALGORITHM_DETAILS(user_id=session['id'], search_type=search_type, page_no=int(page_no)+1)
    search_id, search_name = modules.GET_USER_CURRENT_SEARCH_ALGO_BY_ID(User_id=session['id'])
    return render_template(f"search_algo_home.html",
        algos=algos,
        search_type=search_type,
        search_id=search_id, 
        search_name=search_name,
        
        can_scroll=can_scroll,
        page_no=int(new_page_no)
    )

@app.route("/update_search_algo_choice/<search_algo_id>", methods=['GET', 'POST'])
def update_search_algo_choice(search_algo_id):
    if "email" not in session: 
        return redirect(url_for("login"))
    modules.log_function("request", request, session_user=session['user'])      
        
    #print("search_algo_id:", search_algo_id)
    #print("user id       :", session["id"])
    if not modules.GET_ALL_INTERACTIONS(session["id"]):
        return render_template(f"spam_page.html")
    modules.SEARCH_FAVE_LOGIC(search_algo_id, session["id"])
    modules.UPDATE_CURRENT_SEARCH_BY_USER_ID(search_algo_id, session["id"])
    
    return render_template(f"update_chosen_algorithm.html"
    )

@app.route("/notifications/<page_no>", methods=['GET', 'POST'])
def notifications(page_no):
    if "email" not in session: 
        return redirect(url_for("login"))
    modules.log_function("request", request, session_user=session['user'])
        
    # notifications = modules.GET_NOTIFICATIONS(session["id"], page_no)
    
    return render_template(f"notifications.html",
        notifications="hello world"
    )
    
@app.route("/messages/<page_no>", methods=['GET', 'POST'])
def messages(page_no):
    if "email" not in session: 
        return redirect(url_for("login"))
    
    if int(page_no) <= 0:
        page_no = 0 
    
    modules.log_function("request", request, session_user=session['user'])
    
    if request.method == "POST":
        names = request.form["chosen_name"]
        room_name = request.form["room_name"]
        list_of_names = names.split(",")
        while("" in list_of_names):
            list_of_names.remove("")
        
        #print("list_of_names:",list_of_names)
        #print("room_name    :", room_name)
        creator_name = modules.GET_USER_NAME_FROM_ID(session["id"])
        list_of_names.insert(0, creator_name)
        if not modules.GET_ALL_INTERACTIONS(session["id"]):
            return render_template(f"spam_page.html")
        modules.INSERT_CHAT_ROOMS(Creator_id=session["id"], Room_name=room_name, list_of_names=list_of_names)
    
    chat_rooms = modules.GET_CHAT_ROOM_DETAILS(session["id"], int(page_no)+1)
    chat_invites = modules.GET_CHAT_INVITE_DETAILS(session["id"], int(page_no)+1)
    
    # print(chat_invites)
    return render_template(f"messages_home.html",
        page_no=int(page_no)+1,
        chat_rooms=chat_rooms,
        chat_invites=chat_invites
    )
   
@app.route("/chat_page/<room_id>/<page_no>", methods=['GET', 'POST'])
def chat_page(room_id, page_no): 
    if "email" not in session: 
        return redirect(url_for("login"))
    
    modules.log_function("request", request, session_user=session['user'])
    
    room_name = modules.GET_ROOM_NAME_BY_ID(room_id)
    room_messages, can_scroll = modules.GET_CHAT_MESSAGES(room_id, page_no=int(page_no)+1)
    chat_creator = modules.GET_CHAT_CREATOR_BY_ROOM(room_id)
    current_username = modules.GET_USER_NAME_FROM_ID(session["id"])
    # print(room_messages)
    
    return render_template(f"messages_page.html",
        page_no=int(page_no)+1,
        room_messages=room_messages,
        room_name=room_name,
        room_id=room_id,
        can_scroll=can_scroll,
        current_username=current_username,
        chat_creator=chat_creator
    )
    
@app.route("/update_message/<room_id>/<page_no>", methods=['GET', 'POST'])
def update_message(room_id, page_no):
    if "email" not in session: 
        return redirect(url_for("login"))    
    modules.log_function("request", request)
    
    query_text = request.form["user_message"]
    # encrypted = modules.encrypt_caesar(query_text)
    if not modules.GET_ALL_INTERACTIONS(session["id"]):
        return render_template(f"spam_page.html")
    modules.INSERT_CHAT_MESSAGE(User_id=session["id"], Room_id=room_id, Message=query_text) 
    
    room_name = modules.GET_ROOM_NAME_BY_ID(room_id)
    room_messages, can_scroll = modules.GET_CHAT_MESSAGES(room_id, page_no=int(page_no)+1)
    return render_template(f"update_message.html",
            page_no=int(page_no)+1,
            room_messages=room_messages,
            room_name=room_name,
            room_id=room_id,
            can_scroll=can_scroll
        )
    
@app.route("/chat_logic/<room_id>/<action>", methods=['GET', 'POST'])
def chat_logic(room_id, action):
    
    #print("room_id", room_id)
    #print("action", action)
    if action == "leave":
        print("leaving room")
        if not modules.GET_ALL_INTERACTIONS(session["id"]):
            return render_template(f"spam_page.html")
        if str(room_id) != "1":
            modules.LEAVE_CHAT_ROOM(session["id"], room_id)
        message="LEFT"
    elif action == "accept":
        print("joining room")
        message="JOINED"
        modules.INSERT_CHAT_ROOMS_USER(session["id"], room_id)
        modules.DELETE_CHAT_INVITE(session["id"], room_id)
        print(session["id"], room_id)
    elif action =="reject":
        print("removing invitation")
        message="REJECTED"
        modules.DELETE_CHAT_INVITE(session["id"], room_id)
    return render_template(f"chat_logic.html", message=message)

@app.route("/send_file_message/<post_id>", methods=['GET', 'POST'])
def send_file_message(post_id):
    
    user_id = session["id"]
    message_text = modules.GET_POST_HTML_BY_ID(post_id)
    # SIGN THE HTML SOMEHOW SO I KNOW IT'S COMING FROM INSIDE, WILL PROBABLY NEED TO CHANGE THIS 
    message_text += """
    <div hidden>
        @LOCAL HTML@
    </div>
    """
    chat_room_name = request.form["chat_room_name"]
    room_id = modules.GET_CHAT_ROOM_ID_BY_NAME(chat_room_name)
    
    print("chat_room_name",chat_room_name)
    print("user_id",user_id)
    print("message_text",message_text)
    print("room_id",room_id)
    
    if not modules.GET_ALL_INTERACTIONS(session["id"]):
        return render_template(f"spam_page.html")
    
    
    modules.INSERT_CHAT_MESSAGE(User_id=user_id, Room_id=room_id, Message=message_text)
    return render_template(f"update_sent_message.html",
        success_or_failure="SENT MESSAGE"
        )

@app.route("/kick_from_chat_room/<room_id>", methods=['GET', 'POST'])
def kick_from_chat_room(room_id):
    if "email" not in session: 
        return redirect(url_for("login"))    
    modules.log_function("request", request)
    # print("kicking user")
     
    # might be worth checkking if host user is the one who sent the kick?
    user_being_kicked = request.form["user_kicked_from_channel"]
    # print("user_being_kicked", user_being_kicked)
    User_id = modules.GET_USER_ID_FROM_NAME(user_being_kicked)
    if User_id != "NO ID":
        if not modules.GET_ALL_INTERACTIONS(session["id"]):
            return render_template(f"spam_page.html")
        modules.KICK_FROM_CHAT_ROOM(room_id, User_id) 
    
    # NOT SURE WHY I HAVE TO PUT KICK IN THE FILE
    return render_template(f"update_kick.html",
    )
    
@app.route("/leaderboards_home/<leaderboard_category>", methods=['GET', 'POST'])
def leaderboards_home(leaderboard_category):
    # print("hello world")
    modules.log_function("request", request)
    leaderboards = modules.LEADERBOARD_PERSON(leaderboard_category)        
    user_leaderboards = modules.LEADERBOARD_USER(leaderboard_category)
    
    print('user_leaderboards', user_leaderboards)        
    return render_template(f"leaderboards_home.html",
        people_leaderboards=leaderboards,
        user_leaderboards=user_leaderboards,
        
        leaderboard_category=leaderboard_category
    )
@app.route("/intro_page", methods=['GET'])
def intro_page():
    modules.log_function("request", request)
    
    return render_template(f"intro_page.html",
    )
@app.route("/test_page", methods=['GET', 'POST'])
def test_page():
    modules.log_function("request", request)
    print("VALUES COMING BACK FROM SEARCH ARRAY")
    for key,value in request.form.items():
        print(f"key{key} , value{value}")
    return render_template(f"test_page.html",
    )
    
@app.route("/request_tag/<Post_id>", methods=['GET', 'POST'])
def request_tag(Post_id):
    modules.log_function("request", request)
    chosen_names = request.form.get(f"chosen_names_{Post_id}")

    names = chosen_names.split(",")[:-1]
    
    if not modules.GET_ALL_INTERACTIONS(session["id"]):
        return render_template(f"spam_page.html")
    
    if not modules.CHECK_ACCOUNT_STATUS(session["id"]):
        # print(session["id"], F"is suspended for now. CANT {inspect.stack()[0][3]}")
        return '<div class="text-danger">Cant request tag, suspended until further notice</div>'
    
    num_current_tags = modules.GET_NUM_PEOPLE_BY_POST_ID(Post_id)
    num_requests = modules.GET_NUM_PEOPLE_REQUESTS_BY_POST_ID(Post_id)
    
    if (num_current_tags + num_requests) > 5:
        return '<div class="text-danger">Too many people tagged</div>'
    
    for name in names:
        if name != "None": # there is a frontend issue where i might get a none back
            modules.INSERT_POST_PERSON_REQUEST(Post_id=Post_id, Person_id=modules.GET_PERSON_ID_BY_NAME(name, session["id"]), User_id=session["id"])
    
    return render_template(f"update_poster_person_request.html",
    )

if __name__ == '__main__':
    host = "0.0.0.0" 
    # http://165.227.35.71:8088/
    app.run(host=host, port="8097", debug=False, use_reloader=False)  
