from mongoengine import *
import datetime
from .colManager import ColManager
from .horse import Horse

import sys
sys.path.append ("..")
from utils.logging import trackLogger

class Track(ColManager):
    def __init__(self, database):
        super().__init__(database, "Track")
    
    def saveTrack(self, track_obj):
        try:
            track_count = self.manager.count_documents ({"date": track_obj['date'], "name": track_obj['name']})
            if track_count > 0:
                self.manager.update_one(
                    {"date": track_obj['date'], "name": track_obj['name']},
                    {"$set": track_obj}
                )
            else:
                self.manager.insert_one (track_obj)
        except:
            trackLogger.error ("saveTrack() failed.", exc_info=True)
    