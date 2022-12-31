from flask import *
from os import *
import base64


import python.MODULES as modules

# CONFIG
TEMPLATE_DIR = path.abspath('./templates')
STATIC_DIR = path.abspath('./static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = 'demokey'

@app.route('/', methods=['GET', 'POST'])  # homepage
def home():
    print("test================")
    return redirect(url_for('post_logic', person_id=0,page_no=0 ))
    
@app.route("/<person_id>/<page_no>", methods=['GET', 'POST'])
def post_logic(person_id, page_no):
    modules.log_function("request", request)
    if "email" not in session: 
        return redirect(url_for("login"))
    
    query, posts, new_page_no, posts_per_page, can_scroll, person_id = modules.UNIVERSAL_FUNCTION(
        searcher=session["user"],
        page_no=int(page_no)+1,
        person_id=person_id
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

    )
    
@app.route("/post_tribunal/<page_no>", methods=['GET', "POST"])
def post_tribunal(page_no):
    modules.log_function("request", request)
    query, posts, new_page_no, posts_per_page, can_scroll, person_id = modules.UNIVERSAL_FUNCTION(
        searcher=session["user"], 
        searcher_id=session["id"],
        page_no=int(page_no)+1,
        post_tribunal=True
    )
    offset_calc = int(int(page_no) * int(posts_per_page))
    
    can_vote = modules.CHECK_USER_IS_GLOBAL_ADMIN(session["id"])

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
        can_vote=can_vote
        #fucking hate javascript
    ) 
 
@app.route("/favourites/<page_no>", methods=['GET', 'POST'])
def favourites(page_no):
    modules.log_function("request", request)
    query, posts, new_page_no, posts_per_page, can_scroll, person_id = modules.UNIVERSAL_FUNCTION(
        searcher=session["user"], 
        searcher_id=session["id"],
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
    
@app.route("/person/<person_id>", methods=['GET', 'POST'])
def person(person_id):
    modules.log_function("request", request)
    posts = modules.UNIVERSAL_FUNCTION(searcher=session["user"], person_id=person_id)
    
    return render_template('home.html',
        posts=posts,
    )
    
@app.route("/add_connection/<User_id>", methods=['POST'])
def add_connection(User_id):
    modules.log_function("request", request)
    
    modules.INSERT_CONNECTION(1, User_id) if modules.GET_ALL_INTERACTIONS(session["id"]) else print("too much traffic")
    followers = modules.GET_FOLLOWERS_BY_USER_ID(3)
    return render_template("connection_change.html",
        followers=followers)

@app.route("/remove_connection/<User_id>", methods=['POST'])
def remove_connection(User_id):
    modules.log_function("request", request)
    modules.DELETE_CONNECTION(1, User_id)
    followers = modules.GET_FOLLOWERS_BY_USER_ID(3)
    return render_template("update_connection.html",
        followers=followers)
    
@app.route("/people/<sort_method>/<letter>", methods=['GET', 'POST'])
def people(sort_method, letter):
    modules.log_function("request", request)
    people = modules.GET_ALL_PEOPLE(sort_method=sort_method, letter=letter) #TODO: By letter
    people = list(modules.triple_split(people, 3))

    alpha_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    return render_template("people.html",
        people=people,
        alpha_chars=alpha_chars
        )

@app.route("/request_form/<request_type>", methods=['GET', 'POST'])
def request_form(request_type):
    modules.log_function("request", request)
    #print("request_type", request_type)
    if request.method == "POST":     
        if request_type == "post":
            
            post_title = request.form["post_title"]
            post_title = modules.clean_title(post_title)
            #print("post_title", post_title)
            
            description = request.form["description"]
            description = modules.COMMENT_TEXT_CHECK(description)
            #print("description", description)
            
            link = request.form["post_link"]
            #print("link", link)
            
            person_name = request.form["chosen_name"]
            people = person_name.split(",")
            print("person_name", person_name)
            
            # CHANGE TO POST

            modules.INSERT_POST(Post_title=post_title, 
                                Post_description=description, 
                                Post_link=link, 
                                Post_live="false", 
                                Person=person_name, 
                                User_id=session["id"]
                                )
        elif request_type == "person":
            
            post_title = request.form["post_title"]
            post_title = modules.clean_title(post_title)
            #print("post_title", post_title)
            
            description = request.form["description"]
            description = modules.COMMENT_TEXT_CHECK(description)
            #print("description", description)
            
            link = request.form["post_link"]
            # print("link", link)

            person_name = request.form["person_name"]
            
            modules.INSERT_REQUEST(
                User_id=session["id"],
                Post_title=post_title,
                Description=description,
                Link=link,
                Person_name=person_name
                )  

            
    return render_template(f'request_form.html',
        request_type=request_type
    )

@app.route("/search_users_by_text", methods=['GET'])
def search_users_by_text():
    # GOTTA BE A BETTER WAY to get the query
    print(request.url)
    query_text = str(request.url).split("person_name=")[1]

    if modules.CHECK_INJECTION(query_text):
        users = modules.GET_USERS_BY_TEXT(query_text)
    else:
        users = ["None"]
    return render_template(f'update_user_search.html',
        users=users
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
        print(email)
        print(password)
        if modules.CHECK_INJECTION(email) and modules.CHECK_INJECTION(password):
            print(1)
            signed_in = modules.validate_user_from_session(email, password)
            
            if signed_in[0]: # First element in dict is bool for success/failure
                session["id"] = signed_in[1]
                session["user"] = signed_in[2]
                session["email"] = email
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
            print("new_bad_word", new_bad_word)
            if new_bad_word != None:
                modules.INSERT_TRIBUNAL_WORD(new_bad_word.lower())
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
    print(blocked_words)
    return render_template(f"word_tribunal.html",
        blocked_words=blocked_words
    )

@app.route("/update_like/<Post_id>", methods=['GET', 'POST'])
def update_like(Post_id):
    modules.log_function("request", request)
    modules.LIKE_LOGIC(Post_id, session["id"]) if modules.GET_ALL_INTERACTIONS(session["id"]) else print("too much traffic")
    return render_template(f"update_like.html",
        likes=modules.GET_NUM_LIKES_BY_POST_ID(Post_id))

@app.route("/update_fave/<Post_id>", methods=['GET', 'POST'])
def update_fave(Post_id):
    modules.log_function("request", request)
    modules.FAVE_LOGIC(Post_id, session["id"]) if modules.GET_ALL_INTERACTIONS(session["id"]) else print("too much traffic")
    return render_template(f"update_fave.html",
        faves=modules.GET_NUM_FAVES_BY_POST_ID(Post_id)
        )
    
@app.route("/update_view/<Post_id>", methods=['GET', 'POST'])
def update_view(Post_id):
    modules.log_function("request", request)
    modules.INSERT_VIEWS(Post_id, session["id"]) if modules.GET_ALL_INTERACTIONS(session["id"]) else print("too much traffic")
    return render_template(f"update_view.html",
        views=modules.GET_NUM_VIEWS_BY_POST_ID(Post_id)
        )
    
@app.route("/update_comment/<Post_id>", methods=['GET', 'POST'])
def update_comment(Post_id):
    modules.log_function("request", request)
    input_field = request.form.get("input_field")
    how_many = 11
    
    print("comment update:")
    print("POST ID       :", Post_id)
    print("input_field   :", input_field)
    print("howmany       :", how_many)
    if modules.CHECK_INJECTION(input_field):
        modules.INSERT_COMMENTS(Post_id=Post_id, User_id=session["id"], Comment_text=input_field) if modules.GET_ALL_INTERACTIONS(session["id"]) else print("too much traffic")
    
    return redirect(url_for('comment_section', Post_id=Post_id,how_many=how_many, order="date"))

@app.route("/update_post_html/<Post_id>", methods=['GET', 'POST'])
def update_post_html(Post_id):
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
    modules.log_function("request", request)
    print("Post_id", Post_id)
    print("approval type", approval)

    
    return render_template(f"update_post.html",
        updated_html=modules.GET_POST_HTML_BY_ID(Post_id)
        )

@app.route("/comment_section/<Post_id>/<how_many>/<order>", methods=['GET', 'POST'])
def comment_section(Post_id, how_many, order):
    modules.log_function("request", request)
    transformed_comments = modules.TRANSFRM_COMMENT_ARRAY_INTO_HTML(modules.GET_N_COMMENTS(Post_id=Post_id, N=how_many, new_comment=modules.JANKY_COMMENT_CHECK(how_many), check_order=order))
    
    return render_template(f"update_comments.html",
        comments=transformed_comments,
        )

@app.route("/contact", methods=['GET'])
def contact():
    if "email" not in session:
        return redirect(url_for('login'))
    modules.log_function("request", request, session_user=session['user'])
    
    return render_template(f"contact.html",


    )

@app.route("/structure_search_by_phrase/<page_no>", methods=['GET', 'POST'])
def structure_search_by_phrase(page_no):
    searched_value = ""
    if request.method == "POST": 
        searched_value = request.form["searched_value"]
        print(searched_value)
        #TODO: CHECK SEARCH FOR STUPID SHIT

    query, posts, new_page_no, posts_per_page, can_scroll, person_id = modules.UNIVERSAL_FUNCTION(
        searcher=session["user"],
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
        
        search_phrase=searched_value
    )        

if __name__ == '__main__':
    host = "0.0.0.0" 
    # http://165.227.35.71:8088/
    app.run(host=host, port="8097", debug=False, use_reloader=False)  
