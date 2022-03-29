from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from resources.dating import dating_bp
from resources.appCode import appCode_bp
from resources.login import login_bp
from resources.user import user_bp
from web.web import web_bp

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "derek1020"
jwt = JWTManager(app)

app.register_blueprint(dating_bp, url_prefix='/api/v1/datings')
app.register_blueprint(appCode_bp, url_prefix='/api/v1/appCode')
app.register_blueprint(login_bp, url_prefix='/api/v1/login')
app.register_blueprint(user_bp, url_prefix='/api/v1/users')
app.register_blueprint(web_bp, url_prefix='/')

if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port='8888')