import sys
sys.path.append("..")
from controllers.basicController import BasicController

basicController = BasicController()
def systemRouter(app):
    app.add_url_rule("/basic/get_events_in_today", "/basic/get_events_in_today", basicController.getEventsInToday, methods=["POST"])