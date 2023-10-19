from mongoengine import *
import datetime
from .colManager import ColManager
from .horse import Horse

import sys
sys.path.append ("..")
from utils.logging import marketIdsLogger

class MarketIds(ColManager):
    def __init__(self, database):
        super().__init__(database, "marketids")
    
    def saveData (self, marketIds):
        self.manager.delete_many ({})
        self.manager.insert_one({'marketIds': marketIds})
    
    def getData (self):
        return list(self.manager.find({}))