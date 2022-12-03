import waitress
import os
from flask import Flask
from app import app

def main():
    app.debug = True
    os.environ["FLASK_APP"] = "run.py"
    os.environ["FLASK_ENV"] = "development" #to autoreload when we make changes to our site, changes from production to dev mode
    os.environ["FLASK_DEBUG"] = "1"
    host = "127.0.0.1" # 0.0.0.0 runs on localhost/127.0.0.1
    port = 8080
    print(f'hosting on {host}:{port}')
    
    waitress.serve(app, host=host, port=port) #production server w/ waitress

if __name__  == '__main__':
    app.run(port=8080, debug=True, host="127.0.0.1")
    # main()