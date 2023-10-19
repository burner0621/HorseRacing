import pymongo
import json

from .event import Event
from .track import Track
from .horse import Horse
from .race import Race
from .marketBook import MarketBook
from .marketIds import MarketIds

import sys
sys.path.append ("..")
from utils.logging import dbLogger

class DbManager:
    def __init__(self):
        self.login ()

    def login(self):
        try:
            with open('./config/db.json') as f:
                dbConfig = json.load(f)
                dbname = dbConfig['dbname']
                host = dbConfig['host']
                port = dbConfig['port']
            try:
                self.client = pymongo.MongoClient ("mongodb://%s:%d" %(host, port))
                self.database = self.client[dbname]
                dbLogger.info("===   Database Connection successful.   ===")
                self.eventCol = Event(self.database)
                self.trackCol = Track(self.database)
                self.horseCol = Horse(self.database)
                self.raceCol = Race(self.database)
                self.marketBookCol = MarketBook(self.database)
                self.marketIdsCol = MarketIds (self.database)
            except Exception as e:
                dbLogger.error(f"Database connection failed.", exc_info=True)
                return
        except Exception as e:
            dbLogger.error(f"config/db.json file read failed.", exc_info=True)
            return
        
    def saveManyEvent(self, eventList):
        eList = self.eventCol.insert_many (eventList)
        return eList


dbManager = DbManager()