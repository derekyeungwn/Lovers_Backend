from flask import Flask, render_template
from resources.dating import datings

app = Flask(__name__)

app.register_blueprint(datings)

@app.route('/', methods=['GET'])
def home():
    return render_template('./index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8888')