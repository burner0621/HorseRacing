from mongoengine import *
import datetime
from .colManager import ColManager

import sys
sys.path.append ("..")
from utils.logging import eventLogger
from utils import getTimeRangeOfCountry

class Event(ColManager):
    def __init__(self, database):
        super().__init__(database, "Event")
    
    def saveList(self, dList):
        for d in dList:
            eventCount = self.manager.count_documents ({"eventId": d["eventId"]})
            if (eventCount > 0):
                updateObj = {}
                if len(d['eventVenue']) > 0: updateObj['eventVenue'] = d['eventVenue']
                if len(d['timeZone']) > 0: updateObj['timeZone'] = d['timeZone']
                if d['openDate'] is not None: updateObj['openDate'] = d['openDate']
                if len(d['countryCode']) > 0: updateObj['countryCode'] = d['countryCode']
                
                eventDocument = self.manager.find_one ({"eventId": d["eventId"]})
                updateMarkets = d['markets']
                addMarkets = []
                for market in eventDocument['markets']:
                    flg = False
                    for marketDocument in d['markets']:
                        if marketDocument['marketId'] == market['marketId']:
                            flg = True
                            break
                    if flg == False: addMarkets.append (market)
                
                updateObj['markets'] = updateMarkets + addMarkets
                self.manager.update_one(
                    {"eventId": d['eventId']},
                    {"$set": updateObj}
                )
            else:
                self.manager.insert_one (d)
    
    def getDocumentsByDate(self, dateStr, eventTypeIds, countryCode, marketType):
        [minDate, maxDate] = getTimeRangeOfCountry(dateStr, countryCode.upper())
        events = self.manager.find ({
            "eventVenue": {"$ne": ""},
            "countryCode": countryCode.upper(),
            "markets.marketStartTime": {"$gt": minDate, "$lt": maxDate},
            "markets.marketCatalogueDescription.marketType": marketType,
            "markets.marketCatalogueDescription.raceType": {"$ne": "Harness"}
        })
        return list(events)

    def getDocumentsByFromDate(self, dateStr, eventTypeIds, countryCode):
        [minDate, maxDate] = getTimeRangeOfCountry(dateStr, countryCode.upper())
        events = self.manager.find ({
            "eventVenue": {"$ne": ""},
            "countryCode": countryCode.upper(),
            "markets.marketStartTime": {"$gt": minDate},
            "markets.marketCatalogueDescription.marketType": "WIN",
            "markets.marketCatalogueDescription.raceType": {"$ne": "Harness"}
        })

        return list(events)

    def getDocumentsByMarketId(self, market_id):
        events = self.manager.find({"markets.marketId": market_id})
        return list(events)