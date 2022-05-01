import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current)

from flask import Flask, render_template, render_template, request, flash
from flask_jwt_extended import JWTManager

from resources.test import test_bp
from resources.dating import dating_bp
from resources.appCode import appCode_bp
from resources.login import login_bp
from resources.user import user_bp
from resources.resetPassword import resetPassword_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "derek1020"
app.config["JWT_SECRET_KEY"] = "derek1020"

jwt = JWTManager(app)

app.register_blueprint(test_bp, url_prefix='/test')
app.register_blueprint(dating_bp, url_prefix='/api/v1/datings')
app.register_blueprint(appCode_bp, url_prefix='/api/v1/appCode')
app.register_blueprint(login_bp, url_prefix='/api/v1/login')
app.register_blueprint(user_bp, url_prefix='/api/v1/users')
app.register_blueprint(resetPassword_bp, url_prefix='/api/v1/resetPassword')

@app.route('/', methods = ['GET'])  
def index():  
   return render_template('index.html')

#Testing Code [start]


#Testing Code [end]

if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port='8888')