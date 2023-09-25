import betfairlightweight
import pandas as pd
from .controller import Controller
from datetime import datetime
import sys
sys.path.append('..')
from models.dbManager import dbManager
from utils.JSONEncoder import JSONEncoder
from utils.constants import *

class BasicController(Controller):

    def __init__(self):
        super().__init__()

    def getEvents(self, betDate, eventTypeIds, countryCode):
        if eventTypeIds is None or len(eventTypeIds) == 0:
            return {
                "success": False,
                "msg": "Event type id array parameter should be not empty. Check this parameter again."
            }
        
        eList = dbManager.eventCol.getDocumentsByDate (betDate, eventTypeIds, countryCode)
        data = []
        for e in eList:
            e['_id'] = str(e['_id'])
            tmp = {
                "venue": e['eventVenue'],
                "startTimes": [market['marketStartTime'].strftime("%Y-%m-%dT%H:%M:%SZ") for market in e['markets']]
            }
            data.append (tmp)

        return {
            "success": True,
            "data": data
        }
    
    def getTurnoverInDay(self, date):
        events =  self.getEvents(date, [7], 'AU')
        bankRoll = 0
        for event in events:
            for market in event['markets']:
                bankRoll += market['totalMatched']
        return bankRoll