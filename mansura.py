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
    modules.log_function("request", request)
    if "email" not in session: 
        return redirect(url_for("login"))
    
    posts = modules.UNIVERSAL_FUNCTION()
        
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
    return render_template("connection_change.html",
        followers=followers)
    
@app.route("/categories", methods=['GET', 'POST'])
def categories():
    modules.log_function("request", request)
    categories = modules.GET_ALL_CATEGORIES()
    print(categories)        
    return render_template("categories.html",
        categories=categories)

@app.route("/category/<cat_id>", methods=['GET', 'POST'])
def category(cat_id):
    modules.log_function("request", request)
    posts = modules.UNIVERSAL_FUNCTION(cat_id=cat_id)
    
    return render_template('home.html',
        posts=posts,
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
        return redirect(url_for("user_profile"))
    
    if request.method == 'GET':
        login_message = 'Please LOGIN'
        return render_template('login.html', message=login_message)
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        signed_in = modules.validate_user_from_session(email, password)

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
    modules.log_function("request", request)
    session.pop("email", None)  # remove data from session
    session.pop("user", None)  # remove data from session
    session.pop("password", None)  # remove data from session
    return redirect(url_for("login"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    #print("RENDERING TEMPLATE")
    # print('EXECUTING REGISTER FUNCTION')
    modules.log_function("request", request)
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
            
            has_bad_words = modules.USERNAME_PROFANITY_CHECK(registering_username)
            if not has_bad_words:
                #TODO: FIX THIS, SHOULD JUST BE A REGULAR INSERT?
                #TODO: ADD SUB DESCRIPTIONS TO PEOPLES PROFILES, MANY WILL HAVE SAME NAMES
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
            modules.log_function("error", e, function_name="register")
        return redirect(url_for("login"))
   
@app.route("/password_recovery", methods=['GET', 'POST'])
def password_recovery():
    modules.log_function("request", request)
    #print("LOADING PASSWORD RECOVERY")

    if request.method == "POST":
        recovery_email = request.form["email"]
        # print(recovery_email)
        modules.CREATE_AND_SEND_ONE_TIME_PASS_EMAIL(recovery_email)
        # my_email.send_email(recovery_email)
        return redirect(url_for('password_reset'))
    return render_template(f"password_recovery.html")

@app.route("/password_reset", methods=['GET', 'POST'])
def password_reset():#TODO: GET THIS WORKING, CHECK IF OEN TIME PASS IS THE SMAE
    if modules.CHECK_IF_MOBILE(request):
        return redirect(url_for('cover_page'))
    modules.log_function("request", request)

    if request.method == "POST":
        print("TEST 1 ")
        
        email = request.form["email"]
        password = request.form["password"]
        repeat_pass = request.form["check_password"]
        one_time_pass = request.form["One Time Password"]
        current_one_time_pass = modules.GET_ONE_TIME_PASS(email)
        
        print("email                :",email)
        print("password             :",password)
        print("repeat_pass          :",repeat_pass)
        print("one_time_pass        :",one_time_pass)
        print("current_one_time_pass:",current_one_time_pass)
        

        if (password == repeat_pass) and (one_time_pass == current_one_time_pass):
            modules.CHANGE_PASSWORD( email, password)
            return redirect(url_for("login"))
        else:
            return render_template(f"password_reset.html", message="Passwords are not the same! \nOr One Time Password is Incorrect!")
    else:
        return render_template(f"password_reset.html")







if __name__ == '__main__':
    host = "0.0.0.0" 
    # http://165.227.35.71:8088/
    app.run(host=host, port="8096", debug=False, use_reloader=False)  
