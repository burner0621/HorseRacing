from mongoengine import *
import datetime
from .colManager import ColManager

import sys
sys.path.append ("..")
from utils.logging import horseLogger

class Horse(ColManager):
    def __init__(self, database):
        super().__init__(database, "Horse")
    
    def saveHorse(self, horse_obj):
        try:
            horse_count = self.manager.count_documents ({"id": horse_obj['id']})
            if horse_count > 0:
                self.manager.update_one(
                    {"id": horse_obj['id']},
                    {"$set": horse_obj}
                )
            else:
                self.manager.insert_one (horse_obj)
        except:
            horseLogger.error ("saveTrack() failed.", exc_info=True)

    