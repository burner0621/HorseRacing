import sys
from flask_restx import Namespace, Resource, fields

api = Namespace('api/basic', description='Basic controllers')
sys.path.append("..")
from controllers.basicController import BasicController

basicController = BasicController()

@api.route ('/events/<date>')
class EventList(Resource):
    def get(self, date):
        return basicController.getEvents (date.strip(), [7], 'AU', "WIN")

@api.route ('/events/getrunners/<market_id>')
class GetRunners(Resource):
    def get(self, market_id):
        return basicController.getRunners (market_id)
    
@api.route ('/events/bankroll/<date>')
class Bankroll(Resource):
    def get(self, date):
        return basicController.getBankrollInDay(date)

@api.route ('/marketbooks/<market_id>')
class MarketBook(Resource):
    def get(self, market_id):
        return basicController.getMarketBookById(market_id)
