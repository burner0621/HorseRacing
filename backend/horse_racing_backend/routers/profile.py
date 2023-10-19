import sys
from flask_restx import Namespace, Resource, fields

api = Namespace('api/profile', description='Profile controllers')

sys.path.append("..")
from controllers.profileContoller import ProfileController

profileController = ProfileController()

@api.route ('/races/horse/<horse_id>')
class RaceList(Resource):
    def get(self, horse_id):
        print (horse_id)
        return profileController.getRaceList ("horse", horse_id)
