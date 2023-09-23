import sys
from flask import Blueprint,request

basicRouter = Blueprint('basic', __name__)
sys.path.append("..")
from controllers.basicController import BasicController

basicController = BasicController()

@basicRouter.route ('/get_events/', methods=["GET"])
def get_events():
    if request.method == 'GET':
        betDate = request.args.get('date')
        return basicController.getEvents (betDate, [7], 'AU')