import sys
from flask_restx import Namespace, Resource, fields

api = Namespace('api/profile', description='Profile controllers')

sys.path.append("..")
from controllers.profileContoller import ProfileController

profileController = ProfileController()

@api.route ('/races/horse/<horse_id>')
class RaceHoseList(Resource):
    def get(self, horse_id):
        return profileController.getRaceList ("horse", horse_id)

@api.route ('/races/trainer/<trainer_id>')
class RaceTrainerList(Resource):
    def get(self, trainer_id):
        return profileController.getRaceList ("trainer", trainer_id)

@api.route ('/races/jockey/<jockey_id>')
class RaceJockeyList(Resource):
    def get(self, jockey_id):
        print (jockey_id)
        return profileController.getRaceList ("jockey", jockey_id)