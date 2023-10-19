from mongoengine import *
import datetime
from .colManager import ColManager
from .horse import Horse

import sys
sys.path.append ("..")
from utils.logging import raceLogger

class Race(ColManager):
    def __init__(self, database):
        super().__init__(database, "Race")
    
    def saveRace(self, race_obj):
        try:
            cnt = self.manager.count_documents ({"track_id": race_obj['track_id'], "horse_id": race_obj['horse_id']})
            if cnt > 0:
                self.manager.update_one(
                    {"track_id": race_obj['track_id']},
                    {"$set": race_obj}
                )
            else:
                self.manager.insert_one (race_obj)

        except:
            raceLogger.error ("saveTrack() failed.", exc_info=True)
    
    def getRacesByHorse(self, horse_id):
        races = list(self.manager.find({"horse_id": int(horse_id)}).sort("date", -1))
        return races