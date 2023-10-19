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

def feedStreamData():

    listener = StreamListener(output_queue=output_queue)

    while True:
        # events = dbManager.eventCol.getDocumentsByFromDate (datetime.utcnow().strftime("%Y-%m-%d"), [7], "AU")
        events = tradingObj.getEvents('au', [7])
        marketIds = []
        for event in events:
            marketIds = [market['marketId'] for market in event['markets']]
            # marketIdsDb = dbManager.marketIdsCol.getData ()
            # if len (marketIdsDb) == 0: marketIds = tmp
            # elif 'marketIds' not in marketIdsDb[0]: marketIds = tmp
            # else:
            #     for m in tmp:
            #         if m not in list(marketIdsDb[0]['marketIds']):
            #             marketIds.append (m)
            print (marketIds)
            if len(marketIds) == 0:
                continue
            
            # dbManager.marketIdsCol.saveData (marketIds)
            
            for marketId in marketIds:

                stream = tradingObj.trading.streaming.create_stream(listener=listener)
                market_filter = streaming_market_filter(
                    # market_ids=['1.219530316', '1.219530315', '1.219535798', '1.219535795']
                    market_ids=[marketId]
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
                    time.sleep (1)
                    # t.stop()
                    try:
                        stream.stop()
                    except:
                        pass
                except Exception as e:
                    print (e)
                time.sleep(0.5)
        print ("finished feed......")
        time.sleep (15)
def getQueueData(): 
    while True:
        marketBooks = output_queue.get()
        
        mbs = tradingObj.convertMarketBookToData (marketBooks)
        print (marketBooks[0]['marketId'], mbs[0]['runners'][0]['sp'], "FFFFFFFFFF")

        for marketBook in mbs:
            dbManager.marketBookCol.saveBook (marketBook)
            for runner in marketBook['runners']:
                try:
                    print(
                        runner['sp']['nearPrice'],
                        runner['sp']['farPrice'],
                        marketBook['marketId']
                    )
                except:
                    pass


def main():
    connectDatabase()
    # feedStreamData ()
    feedStreamDataEvent = threading.Thread(target=feedStreamData)
    feedStreamDataEvent.start()
    getQueueDataEvent = threading.Thread(target=getQueueData)
    getQueueDataEvent.start()

if __name__ == "__main__":
    main()
