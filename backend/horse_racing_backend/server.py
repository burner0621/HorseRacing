from flask import Flask
from routers.system import systemRouter

app = Flask(__name__)

def main():
    systemRouter (app)
    app.run(debug = True)

if __name__ == '__main__':
    main ()
