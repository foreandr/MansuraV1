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
        posts_per_page=posts_per_page
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
    modules.INSERT_CONNECTION(1, User_id)
    followers = modules.GET_FOLLOWERS_BY_USER_ID(3)
    return render_template("connection_change.html",
        followers=followers)
    #return redirect(url_for('home'))

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


    
@app.route("/request_form/<request_type>", methods=['GET'])
def request_form(request_type):
    modules.log_function("request", request)
    print("request_type", request_type)
    
    return render_template(f'request_form.html',
        request_type=request_type
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
        signed_in = modules.validate_user_from_session(email, password)

        if signed_in[0]: # First element in dict is bool for success/failure
            session["id"] = signed_in[1]
            session["user"] = signed_in[2]
            session["email"] = email
            return redirect(url_for("home"))
        else:
            return render_template('login.html', message="wrong email or password, try again")

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
            
            has_bad_words = modules.USERNAME_PROFANITY_CHECK(registering_username)
            if not has_bad_words:
                if modules.INSERT_USER(registering_username, password, email):
                    return redirect(url_for('login'))
                else:
                    return render_template('register.html', 
                    return_message="Name already exists"
                )
            else:
                return render_template('register.html', 
                    return_message="Mansura thinks you either have a bad word, or something that could be used for an SQL attack of some kind."
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
def password_reset():#TODO: GET THIS WORKING, CHECK IF OEN TIME PASS IS THE SMAE
    modules.log_function("request", request)
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        repeat_pass = request.form["check_password"]
        one_time_pass = request.form["One Time Password"]
        current_one_time_pass = modules.GET_ONE_TIME_PASS(email)
        if (password == repeat_pass) and (one_time_pass == current_one_time_pass):
            modules.CHANGE_PASSWORD( email, password)
            return redirect(url_for("login"))
        else:
            return render_template(f"password_reset.html", message="Passwords are not the same! \nOr One Time Password is Incorrect!")
    else:
        return render_template(f"password_reset.html")

@app.route("/word_tribunal", methods=['GET', "POST"])
def word_tribunal():
    if "email" not in session:
        return redirect(url_for('login'))
    modules.log_function("request", request, session_user=session['user'])
    
    if request.method == "POST":
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

    return render_template(f"word_tribunal.html",
        blocked_words=blocked_words
    )

@app.route("/update_like/<Post_id>", methods=['GET', 'POST'])
def update_like(Post_id):
    modules.log_function("request", request)
    modules.LIKE_LOGIC(Post_id, session["id"])
    return render_template(f"update_like.html",
        likes=modules.GET_NUM_LIKES_BY_POST_ID(Post_id))

@app.route("/update_fave/<Post_id>", methods=['GET', 'POST'])
def update_fave(Post_id):
    print("helloo1")
    modules.log_function("request", request)
    modules.FAVE_LOGIC(Post_id, session["id"])
    return render_template(f"update_fave.html",
        faves=modules.GET_NUM_FAVES_BY_POST_ID(Post_id)
        )
    
@app.route("/update_view/<Post_id>", methods=['GET', 'POST'])
def update_view(Post_id):
    modules.log_function("request", request)
    modules.INSERT_VIEWS(Post_id, session["id"])
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
    
    modules.INSERT_COMMENTS(Post_id=Post_id, User_id=session["id"], Comment_text=input_field)
    return redirect(url_for('comment_section', Post_id=Post_id,how_many=how_many, order="date"))



@app.route("/comment_section/<Post_id>/<how_many>/<order>", methods=['GET', 'POST'])
def comment_section(Post_id, how_many, order):
    modules.log_function("request", request)
    transformed_comments = modules.TRANSFRM_COMMENT_ARRAY_INTO_HTML(modules.GET_N_COMMENTS(Post_id=Post_id, N=how_many, new_comment=modules.JANKY_COMMENT_CHECK(how_many), check_order=order))

    return render_template(f"update_comments.html",
        comments=transformed_comments,
        how_many=int(how_many)+1,
        comment_post_id=Post_id,
        commenting=modules.JANKY_COMMENT_CHECK(how_many),
        num_comments=modules.GET_COUNT_COMMENTS_BY_ID(Post_id)
        )



if __name__ == '__main__':
    host = "0.0.0.0" 
    # http://165.227.35.71:8088/
    app.run(host=host, port="8097", debug=False, use_reloader=False)  
