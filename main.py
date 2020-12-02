import os
from flask import Flask,render_template
# from flask_httpauth import HTTPBasicAuth
# from flask_login import LoginManager
# from flask_admin import Admin,BaseView,expose
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
# from flask_babelex import Babel
# from flask_marshmallow import Marshmallow
from config import Config

basedir = os.path.abspath(os.path.dirname(__file__))

# create Flask app instance
app = Flask(__name__,
template_folder="appFront/dist",
static_folder="appFront/dist/vueStatic")
# babel = Babel(app)
# app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'

secret_key = app.config['SECRET_KEY'] = 'zonesion123'

# auth = HTTPBasicAuth()

# Create login manager instance
# login_manager = LoginManager()  
# login_manager.init_app(app)  
# login_manager.login_view = 'login'

# cross-domain
CORS(app, supports_credentials=True)
# Loading config file
app.config.from_object(Config)
Config.init_app(app)

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)
db.init_app(app)

# Create admin instance
# admin = Admin(app,name='后台管理系统', template_mode='bootstrap3')

# create api instance
api = Api(app)


# Initialize Marshmallow
# ma = Marshmallow(app)
@app.route("/")
def index():
    return render_template('index.html')