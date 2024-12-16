# app/__init__.py

from flask import Flask
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'temp')  # You can change 'temp' to another directory if you like


# Import routes after app is initialized
from app.routes import *
