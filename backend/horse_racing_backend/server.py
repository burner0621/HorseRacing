from flask import Flask
from flask_cors import CORS
from routers import api
import json

def main():
    app = Flask(__name__)
    api.init_app(app)

    CORS(app, supports_credentials=True)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['CORS_RESOURCES'] = {r"*": {"origins": "*"}}

    global host, port
    host = "0.0.0.0"
    port = 5555
    try:
        with open("config/main.json") as f:
            config = json.load(f)
            host = config['host']
            port = config['port']
    except Exception as e:
        print ("Config file read error.")
    
    app.run(host = host, port = port, debug = True)

if __name__ == '__main__':
    main ()
