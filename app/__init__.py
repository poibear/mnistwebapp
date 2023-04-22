from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thesecretcode' #use flask_wtf to prevent csrf attacks

from app import views_ext