from mongoengine import *
import datetime

class Event(Document):
    eventId = StringField (max_length=20, required = True)
    createdAt = DateTimeField (default = str (datetime.datetime.utcnow().timestamp() * 1000))
    countryCode = StringField (max_length=20, required = True)
    eventName = StringField (max_length=20, required = True)
    eventVenue = StringField (max_length=20, required = True)
    timeZone = StringField (max_length=20, required = True)
    openDate = StringField (max_length=20, required = True)
    marketCount = IntField (required = True)

class Market(Document):
    marketId = StringField (max_length=20, required = True)
    createdAt = DateTimeField (default = str (datetime.datetime.utcnow().timestamp() * 1000))
