import betfairlightweight
import pandas as pd
from .controller import Controller
from datetime import datetime
import sys
sys.path.append('..')
from models.dbManager import dbManager
from utils.JSONEncoder import JSONEncoder
from utils.constants import *
from utils.logging import basicControllerLogger

class BasicController(Controller):

    def __init__(self):
        super().__init__()

    def getEvents(self, betDate, eventTypeIds, countryCode, marketType):
        if eventTypeIds is None or len(eventTypeIds) == 0:
            return {
                "success": False,
                "msg": "Event type id array parameter should be not empty. Check this parameter again."
            }
        
        eList = dbManager.eventCol.getDocumentsByDate (betDate, eventTypeIds, countryCode, marketType)
        data = []
        for e in eList:
            if e['eventId'] == 32707774: continue
            e['_id'] = str(e['_id'])
            
            lastMarket = e['markets'][-1]
            if (lastMarket['marketStartTime'] - datetime.now()).seconds > 0:
                if lastMarket['marketBook']['status'] == 'CLOSED': continue
            tmp = {
                "venue": e['eventVenue'],
                "markets": [{"startTime": market['marketStartTime'].strftime("%Y-%m-%dT%H:%M:%SZ"),
                             "marketId": market['marketId'],
                             "venue": e['eventVenue'],
                             "status":market['marketBook']['status'],
                             "totalMatched": market['totalMatched'],
                            } 
                            for market in e['markets'] if market["marketCatalogueDescription"]["marketType"] == "WIN"]
            }
            data.append (tmp)
        return {
            "success": True,
            "data": data
        }

    '''
    req = 0: rest api request
    req = 1: full market book data
    req = 2: custome find
    '''
    def getMarketBookById(self, market_id, req = 0, match={}):
        try:
            if len(market_id) == 0:
                return {
                    "success": False, 
                    "msg": "Market ID parameter is invalid."
                }
            if req == 0 or req == 1:
                marketBook = dbManager.marketBookCol.getDocumentsByID (market_id)

                if len(marketBook)==0:
                    return {
                        "success": False, 
                        "msg": "No market book data with this market id: %s." % market_id
                    }
                if req == 0:
                    return {
                        "success": True,
                        "data": {
                            "totalMatched": marketBook[0]['totalMatched'],
                            "totalAvailable": marketBook[0]['totalAvailable'],
                            "runnerLen": len(list(marketBook[0]['runners']))
                        }
                    }
                elif req == 1:
                    try:
                        return marketBook[0]
                    except Exception as e:
                        return None
            elif req == 2:
                marketBook = dbManager.marketBookCol.getDocumentsByID (market_id, match)
                try:
                    return marketBook[0]
                except Exception as e:
                    return None

            
        except Exception as e:
            basicControllerLogger.error ("getMarketBookById() call failed.", exc_info=True)
            return {
                "success": False,
                "msg": "server failed with getMarketBookById()"
            }

    def getRunners(self, market_id):
        try:
            if len(market_id) == 0:
                return {
                    "success": False, 
                    "msg": "Market ID parameter is invalid."
                }
            eventObj = dbManager.eventCol.getDocumentsByMarketId (market_id)
            if len(eventObj)==0:
                return {
                    "success": False, 
                    "msg": "No event data with this market id: %s." % market_id
                }
            eventObj = eventObj[0]
            rlt_market = None
            for market in eventObj['markets']:
                if market['marketId'] == market_id:
                    rlt_market = market
                    break
            if rlt_market is None:
                return {
                    "success": False, 
                    "msg": "No market data in event object with this market id: %s." % market_id
                }
            rlt = []
            for runner in rlt_market['runners']:
                metadata = runner['metadata']
                market_book = self.getMarketBookById (market_id, 1)
                market_book_sp = self.getMarketBookById (market_id, 2, {"runners.sp.actualSp": {"$gt": 0}})
                betfair_odds = 0
                status = ''
                if market_book is not None and market_book['inplay'] == False:
                    try:
                        for book_runner in market_book['runners']:
                            if runner['selectionId'] == book_runner['selectionId']:
                                # if book_runner['ex'] == {}: break
                                # if 'availableToBack' not in dict(book_runner['ex']): break
                                # if len(book_runner['ex']['availableToBack']) == 0: break
                                # betfair_odds = int(book_runner['ex']['availableToBack'][0]['price']
                                if book_runner['sp'] == {}: break
                                if 'nearPrice' not in dict(book_runner['sp']): break
                                betfair_odds = book_runner['sp']['nearPrice']
                                if book_runner['status'] is not None and book_runner['status'] != 0 and book_runner['status'] != '':
                                    status = book_runner['status']
                                break
                    except:
                        pass
                if market_book_sp is not None and market_book['inplay'] == True:
                    try:
                        for book_runner in market_book_sp['runners']:
                            if runner['selectionId'] == book_runner['selectionId']:
                                if book_runner['sp'] == {}: break
                                if 'actualSp' not in dict(book_runner['sp']): break
                                betfair_odds = book_runner['sp']['actualSp']
                                break
                    except:
                        pass
                if (status == 'ACTIVE'):
                    rlt.append ({
                        "file": metadata['COLOURS_FILENAME'],
                        "priority": runner['sortPriority'],
                        "selectionId": runner['selectionId'],
                        "name": runner['runnerName'],
                        "jockeyName": metadata['JOCKEY_NAME'],
                        "clothNum": metadata['CLOTH_NUMBER'],
                        "betfairOdds": betfair_odds
                    })
            return {
                "success": True,
                "data": rlt
            }

        except Exception as e:
            basicControllerLogger.error ("getRunners() call failed.", exc_info=True)
            return {
                "success": False,
                "msg": "server failed with getRunners()"
            }
        
    def getTurnoverInDay(self, date):
        events =  self.getEvents(date, [7], 'AU')
        bankRoll = 0
        for event in events:
            for market in event['markets']:
                bankRoll += market['totalMatched']
        return bankRoll