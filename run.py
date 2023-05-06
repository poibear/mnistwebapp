#!/usr/bin/python3.10
#TODO: read multiple numbers with opencv
#import waitress
import os
from flask import Flask
from app import app, views

app.config['SECRET_KEY'] = 'secret1'

def main():
    app.debug = True
<<<<<<< HEAD
    app.config['SECRET_KEY'] = 'thesecretcode' #use flask_wtf to prevent csrf attacks

=======
    
>>>>>>> 705ab68e330c60ab3eb76786e939e860ef447fe8
    #app = Flask(__name__)
    os.environ["FLASK_APP"] = "run.py"
    os.environ["FLASK_DEBUG"] = "1"
    host = "127.0.0.1" # 0.0.0.0 runs on localhost/127.0.0.1
    port = 8000
    print(f'hosting on {host}:{port}')
    
    app.run(port=port, debug=True, host=host)
    #waitress.serve(app, host=host, port=port) #production server w/ waitress

if __name__  == '__main__':
    main()
