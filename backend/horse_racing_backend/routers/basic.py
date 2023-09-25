import sys
from flask_restx import Namespace, Resource, fields

api = Namespace('api/basic', description='Basic controllers')
sys.path.append("..")
from controllers.basicController import BasicController

basicController = BasicController()

@api.route ('/events/<date>')
class EventList(Resource):
    def get(self, date):
        return basicController.getEvents (date.strip(), [7], 'AU')

@api.route ('/events/bankroll/<date>')
class Bankroll(Resource):
    def get(self, date):
        return basicController.getBankrollInDay(date)