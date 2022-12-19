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
    category_posts = modules.UNIVERSAL_FUNCTION(1)
    #print(category_posts[0][2])
    #print(type(category_posts[0][2]))
    #print(len(category_posts[0][2]))
    return render_template('home.html',
        msg=category_posts[0][2]
    )
    
@app.route("/add_connection/<User_id>", methods=['POST'])
def add_connection(User_id):
    modules.INSERT_CONNECTION(1, User_id)
    return redirect(url_for('home'))

    
@app.route("/remove_connection/<User_id>", methods=['POST'])
def remove_connection(User_id):
    modules.DELETE_CONNECTION(1, User_id)
    return redirect(url_for('home'))
    
    


if __name__ == '__main__':
    host = "0.0.0.0" 
    # http://165.227.35.71:8088/
    app.run(host=host, port="8096", debug=False, use_reloader=False)  
