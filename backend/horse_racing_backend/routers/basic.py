import sys
from flask import Blueprint,request

basicRouter = Blueprint('basic', __name__)
sys.path.append("..")
from controllers.basicController import BasicController

basicController = BasicController()

@basicRouter.route ('/get_events_in_today/', methods=["POST"])
def get_events_in_today():
    if request.method == 'POST':
        eventTypeIds = request.json['eventTypeIds']
        timeZone = request.json['timeZone']
        return basicController.getEventsInToday (eventTypeIds, timeZone)