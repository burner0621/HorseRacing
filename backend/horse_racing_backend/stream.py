import threading
import json
from betfairs.trading import tradingObj
from betfairlightweight import StreamListener
from betfairlightweight.filters import (
    streaming_market_filter,
    streaming_market_data_filter,
)

from utils.logging import streamLogger

from models.dbManager import dbManager
import queue
import time
from datetime import datetime

marketIds = []
output_queue = queue.Queue()

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
            streamLogger.info("===   Database Connection successful.   ===")
        except Exception as e:
            streamLogger.error("Database connection failed.", exc_info=True)
            return
    except Exception as e:
        streamLogger.error("config/db.json file read failed.", exc_info=True)
        return

def feedStreamData(evt):

    listener = StreamListener(output_queue=output_queue)
    dbManager.marketIdsCol.saveData ([])

    while True:
        if evt.is_set(): break
        dbMarketIds = dbManager.marketIdsCol.getData ()
        marketIdSet = set(dbMarketIds)

        events = tradingObj.getEvents('au', [7])
        marketIds = []
        for event in events:
            tmp = [market['marketId'] for market in event['markets']]
            marketIds += tmp
        
        tmpSet = marketIdSet.copy()
        marketIdSet.update (marketIds)

        newMarketIds = marketIdSet - tmpSet

        dbManager.marketIdsCol.saveData (list(marketIdSet))
            

        stream = tradingObj.trading.streaming.create_stream(listener=listener)
        market_filter = streaming_market_filter(
            market_ids=list(newMarketIds)
        )
        market_data_filter = streaming_market_data_filter(
            fields=["SP_PROJECTED", "SP_PROJECTED", "EX_MARKET_DEF", "EX_BEST_OFFERS_DISP", "EX_BEST_OFFERS", "EX_ALL_OFFERS", "EX_TRADED", "EX_TRADED_VOL"], ladder_levels=3
        )
        try:
            streaming_unique_id = stream.subscribe_to_markets(
                market_filter=market_filter,
                market_data_filter=market_data_filter,
                conflate_ms=1000,  # send update every 1000ms
            )
            t = threading.Thread(target=stream.start, daemon=True)
            t.start()
        except Exception as e:
            print (e)
        print ("finished feed......")
        time.sleep (3600)
def getQueueData(): 
    while True:
        marketBooks = output_queue.get()
        
        mbs = tradingObj.convertMarketBookToData (marketBooks)

        for marketBook in mbs:
            dbManager.marketBookCol.saveBook (marketBook)
            for runner in marketBook['runners']:
                try:
                    print(
                        runner['sp']['actualSp'],
                        runner['sp']['nearPrice'],
                        runner['sp']['farPrice'],
                        marketBook['marketId']
                    )
                except:
                    pass
        print ("########################################")


def main():
    connectDatabase()
    
    getQueueDataEvent = threading.Thread(target=getQueueData)
    getQueueDataEvent.start()
    while True:
        evt = threading.Event ()
        feedStreamDataEvent = threading.Thread(target=feedStreamData, args=(evt,))
        feedStreamDataEvent.start()
        # time.sleep (3600)
        time.sleep (1800)
        evt.set()

if __name__ == "__main__":
    main()
