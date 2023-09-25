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
                updateMarkets = eventDocument['markets']
                addMarkets = []
                for market in d['markets']:
                    flg = False
                    for marketDocument in updateMarkets:
                        if marketDocument['marketId'] == market['marketId']:
                            marketDocument = market['marketId']
                            flg = True
                            break
                    if flg == False: addMarkets.append (marketDocument)
                
                updateObj['markets'] = updateMarkets + addMarkets

                self.manager.update_one(
                    {"eventId": d['eventId']},
                    {"$set": updateObj}
                )
            else:
                self.manager.insert_one (d)
    
    def getDocumentsByDate(self, dateStr, eventTypeIds, countryCode):
        [minDate, maxDate] = getTimeRangeOfCountry(dateStr, countryCode.upper())
        events = self.manager.find ({
            "eventVenue": {"$ne": ""},
            "countryCode": countryCode.upper(),
            "markets.marketStartTime": {"$gt": minDate, "$lt": maxDate},
        })
        return list(events)

    def getDocumentsByFromDate(self, dateStr, eventTypeIds, countryCode):
        [minDate, maxDate] = getTimeRangeOfCountry(dateStr, countryCode.upper())
        events = self.manager.find ({
            "eventVenue": {"$ne": ""},
            "countryCode": countryCode.upper(),
            "markets.marketStartTime": {"$gt": minDate},
        })

        return list(events)

# class Competition(EmbeddedDocument):
#     id = IntField(required = True)
#     name = StringField (max_legnth = 255, required = True)

# class Runner(EmbeddedDocument):
#     handicap = StringField (max_length=32, required = True)
#     metadata = DictField()
#     runnerName = StringField (max_length=255, required = True)
#     selectionId = IntField ()
#     sortPriority = StringField (max_length=32, required = True)

# class MarketCatalogueDescription(EmbeddedDocument):
#     bettingType = StringField (max_length=32, required = True)
#     bspMarket =  StringField (max_length=32, required = True)
#     clarifications = StringField (max_length=32, required = True)
#     discountAllowed = BooleanField (required = True, default = False)
#     eachWayDivisor = StringField (required = True)
#     marketBaseRate = StringField (required = True)
#     marketTime = DateTimeField()
#     marketType = StringField (required = True)
#     persistenceEnalbled = BooleanField ()
#     regulator = StringField (required = True)
#     rules = StringField (required = True)
#     rulesHasDate = BooleanField ()
#     suspendTime = DateTimeField ()
#     turnInPlayEenabled = BooleanField ()
#     wallet = StringField (required = True)

# class Market(EmbeddedDocument):
#     marketId = StringField (max_length=16, required = True)
#     marketName = StringField (max_length=255, required = True)
#     marketStartTime = DateTimeField(required = True)
#     eventId = IntField ()
#     totalMatched = FloatField ()
#     marketCatalogueDescription = EmbeddedDocumentField (MarketCatalogueDescription)
#     competition = EmbeddedDocumentField (Competition)
#     runners = ListField (EmbeddedDocumentField(Runner))
#     createdAt = DateTimeField (default = datetime.datetime.utcnow())

# class Event(Document):
#     eventId = IntField (max_length=16, required = True)
#     eventName = StringField (max_length=255, required = True)
#     eventVenue = StringField (max_length=64)
#     timeZone = StringField (max_length=255, required = True)
#     openDate = DateTimeField (required = True)
#     marketCount = IntField (required = True)
#     countryCode = StringField (max_length=16, required = True)
#     markets = ListField (EmbeddedDocumentField(Market), default=list)
#     createdAt = DateTimeField (default = str (datetime.datetime.utcnow().timestamp() * 1000))
