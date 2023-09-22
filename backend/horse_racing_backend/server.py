from flask import Flask
from flask_cors import CORS, cross_origin
from routers.basic import basicRouter
import json


def main():
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'application/json'

    app.register_blueprint(basicRouter, url_prefix='/api/basic')
    
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
