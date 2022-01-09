from flask import Flask, render_template
from resources.dating import dating_bp
from web.web import web_bp

app = Flask(__name__)

app.register_blueprint(dating_bp, url_prefix='/api/v1/datings')
app.register_blueprint(web_bp, url_prefix='/')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8888')