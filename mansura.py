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
    message = "hello world"

    return render_template('home.html',
        msg= message 
    )


if __name__ == '__main__':
    host = "0.0.0.0" 
    # http://165.227.35.71:8088/
    app.run(host=host, port="8096", debug=False, use_reloader=False)  
