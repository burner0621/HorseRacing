from flask import jsonify
import betfairlightweight
import pandas as pd
from .controller import Controller
from datetime import datetime
from bson import json_util
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
        
        eList = dbManager.eventCol.getDocuments (betDate, eventTypeIds, countryCode)
        data = []
        for e in eList:
            e['_id'] = str(e['_id'])
            data.append (e)
        # data = jsonify(data=[JSONEncoder().encode(doc) for doc in list(eList)])

        return json_util.dumps({
            "success": True,
            "data": data
        })

    def getCountries(self):
        countries = self.trading.betting.list_countries()

        cList = [{'Country': countryResult.country_code,
                  'MartketCount': countryResult.market_count} for countryResult in countries]

        return cList

    def getTimeRanges(self, venues, granularity):
        mf = self.makeMarketFilter(
            venues=venues,
        )
        timeRanges = self.trading.betting.list_time_ranges(
            filter=mf, granularity=granularity)
        timeRangeObj = [{
            'from': trObject['_data']['timeRange']['from'],
            'to': trObject['_data']['timeRange']['to'],
            'marketCount': trObject['_data']['marketCount']} for trObject in timeRanges]
        return timeRangeObj
    
    def getProfitAndLoss(self, marketIds, includeBspBets, includeSettledBets):
        pl = self.trading.betting.list_market_profit_and_loss(market_ids=marketIds, 
                                                 include_bsp_bets=includeBspBets, 
                                                 include_settled_bets=includeSettledBets)
        try:
            pl_df = pd.DataFrame(pl[0]._data['profitAndLosses']).assign(marketId=pl[0].market_id)
        except Exception as e:
            print ("getProfitAndLoss ===> ", e)

    def makeMarketFilter(
            self,
            textQuery=None,
            eventTypeIds=None,
            eventIds=None,
            competitionIds=None,
            marketIds=None,
            venues=None,
            bspOnly=None,
            turnInPlayEnabled=None,
            inPlayOnly=None,
            marketBettingTypes=None,
            marketCountries=None,
            marketTypeCodes=None,
            marketStartTime=None,
            withOrders=None,
            raceTypes=None
    ):
        return betfairlightweight.filters.market_filter(
            text_query=textQuery,
            event_type_ids=eventTypeIds,
            event_ids=eventIds,
            competition_ids=competitionIds,
            market_ids=marketIds,
            venues=venues,
            bsp_only=bspOnly,
            turn_in_play_enabled=turnInPlayEnabled,
            in_play_only=inPlayOnly,
            market_betting_types=marketBettingTypes,
            market_countries=marketCountries,
            market_type_codes=marketTypeCodes,
            market_start_time=marketStartTime,
            with_orders=withOrders,
            race_types=raceTypes
        )
