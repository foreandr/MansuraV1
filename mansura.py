from flask import *
from os import *

import python.DB_READ as DB_READ

# CONFIG
TEMPLATE_DIR = path.abspath('./templates')
STATIC_DIR = path.abspath('./static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = 'demokey'

@app.route('/', methods=['GET', 'POST'])  # homepage
def home():
    return DB_READ.GET_PROFILE_IMAGE_BY_USER("foreandr")

if __name__ == '__main__':
    host = "0.0.0.0" 
    # http://165.227.35.71:8088/
    app.run(host=host, port="8096", debug=False, use_reloader=False)  

    pass