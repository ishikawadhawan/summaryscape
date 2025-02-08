from flask_cors import CORS
from flask import Flask
from routes import routes

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests
app.register_blueprint(routes)

@app.route('/')
def home():
    return "Welcome to the Summary Scape Backend!"

if __name__ == '__main__':
    app.run(debug=True)
