from flask import Flask, render_template
import os

# Get the absolute path to the root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(ROOT_DIR, '..', 'templates')
STATIC_DIR = os.path.join(ROOT_DIR, '..', 'static')

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

def run_flask_app():
    app.run(host='0.0.0.0', port=5000)
