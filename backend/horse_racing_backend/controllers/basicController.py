from utils import getCountryCode, getTimeRageInADay
from utils.constants import *
import betfairlightweight
import pandas as pd
from .controller import Controller
from datetime import datetime
import json
import pytz

import sys
sys.path.append('..')


class BasicController(Controller):

    def __init__(self):
        super().__init__()

    def getEventsInToday(self, eventTypeIds, timeZone):
        if timeZone is None or len(timeZone.strip()) == 0:
            return {
                "success": False,
                "msg": "Time zone parameter should be not empty. Check this parameter again."
            }
        if timeZone not in pytz.all_timezones:
            return {
                "success": False,
                "msg": "Time zone parameter is invalid."
            }
        if eventTypeIds is None or len(eventTypeIds) == 0:
            return {
                "success": False,
                "msg": "Event type id array parameter should be not empty. Check this parameter again."
            }

        countryCode = getCountryCode(timeZone)
        if countryCode is None:
            return {
                "success": False,
                "msg": "Time Zone parameter is wrong. Please enter the correct time zone."
            }

        cList = self.getCountries()
        if countryCode not in [country[COUNTRY] for country in cList]:
            return {"success": False, "msg": "CountryCode is wrong."}

        [startTime, endTime] = getTimeRageInADay(timeZone)
        events = self.getEvents(countryCode, eventTypeIds,
                                # "2023-09-22T23:59:59Z")
                                endTime.strftime("%Y-%m-%dT%H:%M:%SZ"))
        eList = []
        for event in events:
            trs = self.getTimeRanges([event[EVENT_VENUE]], 'MINUTES')
            tmp = []
            for tr in trs:
                if (endTime - datetime.strptime(tr['from'], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.UTC)).seconds < 0:
                    continue
                tmp.append(tr)
            event['Time Ranges'] = tmp
            eList.append(event)

        return {
            "success": True,
            "data": eList
        }

    def getCountries(self):
        countries = self.trading.betting.list_countries()

        cList = [{'Country': countryResult.country_code,
                  'MartketCount': countryResult.market_count} for countryResult in countries]

        return cList

    def getEvents(self, countryCode, eventTypeIds, endTime):
        mf = self.makeMarketFilter(
            marketCountries=[countryCode],
            eventTypeIds=eventTypeIds,
            marketStartTime={
                "to": endTime
            }
        )
        eventsToday = self.trading.betting.list_events(filter=mf)

        eventsTodayObj = [{'Event Name': eventObject.event.name,
                           'Event ID': eventObject.event.id,
                           'Event Venue': eventObject.event.venue,
                           'Country Code': eventObject.event.country_code,
                           'Time Zone': eventObject.event.time_zone,
                           'Open Date': eventObject.event.open_date,
                           'Market Count': eventObject.market_count} for eventObject in eventsToday]

        return eventsTodayObj

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
        print (len (pl))
        try:
            pl_df = pd.DataFrame(pl[0]._data['profitAndLosses']).assign(marketId=pl[0].market_id)
            print (pl_df, ">>>>>")
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
