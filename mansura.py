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
    posts = modules.UNIVERSAL_FUNCTION()
    # followers = modules.GET_FOLLOWERS_BY_USER_ID(3)
    for i in posts:
        print(i)
        
    return render_template('home.html',
        posts=posts,
    )
    
@app.route("/add_connection/<User_id>", methods=['POST'])
def add_connection(User_id):
    modules.INSERT_CONNECTION(1, User_id)
    followers = modules.GET_FOLLOWERS_BY_USER_ID(3)
    return render_template("connection_change.html",
        followers=followers)
    #return redirect(url_for('home'))

    
@app.route("/remove_connection/<User_id>", methods=['POST'])
def remove_connection(User_id):
    modules.DELETE_CONNECTION(1, User_id)
    followers = modules.GET_FOLLOWERS_BY_USER_ID(3)
    return render_template("connection_change.html",
        followers=followers)
    
@app.route("/categories", methods=['GET', 'POST'])
def categories():
    categories = modules.GET_ALL_CATEGORIES()
    print(categories)        
    return render_template("categories.html",
        categories=categories)

@app.route("/category/<cat_id>", methods=['GET', 'POST'])
def category(cat_id):
    posts = modules.UNIVERSAL_FUNCTION(cat_id=cat_id)
    
    return render_template('home.html',
        posts=posts,
    )
    


if __name__ == '__main__':
    host = "0.0.0.0" 
    # http://165.227.35.71:8088/
    app.run(host=host, port="8096", debug=False, use_reloader=False)  
