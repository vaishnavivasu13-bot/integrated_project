print("Hello World")
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "GlamCart is Ready"

if __name__ == '_main_':
    app.run(debug=True, port=5000)