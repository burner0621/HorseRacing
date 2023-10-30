
import pandas as pd
import os
import time
import json
from datetime import datetime
import threading
from betfairs.trading import tradingObj
from utils.logging import daemonLogger

from feedFromXML.src.parse import buildRaceProfile, parse

from models.dbManager import dbManager

def connectDatabase():
    from mongoengine import connect
    try:
        with open('./config/db.json') as f:
            dbConfig = json.load(f)
            dbname = dbConfig['dbname']
            host = dbConfig['host']
            port = dbConfig['port']
            username = dbConfig['username']
            password = dbConfig['password']
        try:
            connect (db=dbname, username=username, password=password, host="mongodb://%s:%d/%s" %(host, port, dbname))
            daemonLogger.info("===   Database Connection successful.   ===")
        except Exception as e:
            daemonLogger.error("Database connection failed.", exc_info=True)
            return
    except Exception as e:
        daemonLogger.error("config/db.json file read failed.", exc_info=True)
        return

def daemonSaveEvent(interval, event):
    while True:
        if event.is_set(): break
        events = tradingObj.getEvents('au', [7])
        dbManager.eventCol.saveList (events)
        time.sleep(interval)

def daemonSaveMarketBook(interval):
    while True:
        events = dbManager.eventCol.getDocumentsByFromDate (datetime.utcnow().strftime("%Y-%m-%d"), [7], "AU")
        for event in events:
            for market in event['markets']:
                marketBooks = tradingObj.getMarketBooks ([market['marketId']])
                if len(marketBooks) > 0:
                    marketBook = marketBooks [0]
                    if marketBook['status'] == 'OPEN':
                        dbManager.marketBookCol.saveBook (marketBook)
        time.sleep (interval)

def daemonSaveXMLData():
    races = buildRaceProfile ()
    for race in races:
        dbManager.raceCol.saveRace (race)

def main():
    connectDatabase()

    # daemonSaveXMLData ()

    while True:
        evt = threading.Event()
        saveEvent = threading.Thread(target=daemonSaveEvent, args=(15,evt))
        # saveMarketBook = threading.Thread(target=daemonSaveMarketBook, args=(15,))
        saveEvent.start ()
        time.sleep (3600)
        evt.set ()
        print (">>>>>>>")
        time.sleep (30)
        # saveMarketBook.start ()

if __name__ == "__main__":
    main()
