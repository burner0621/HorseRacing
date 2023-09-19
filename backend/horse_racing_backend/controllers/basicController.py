import betfairlightweight
from flask import request
import pandas as pd
from .controller import Controller
import json


class BasicController(Controller):

    def __init__(self):
        super().__init__()

    def getEventsInToday(self):
        if request.method == 'POST':
            countryCode = request.json['countryCode']
            eventTypeIds = request.json['eventTypeIds']
            endTime = request.json['endTime']
            print(eventTypeIds, len(eventTypeIds), "eventTypeIds")
        countryCode = 'au'
        cList = self.getCountries()
        countryCode = countryCode.upper()
        if countryCode not in cList['Country'].tolist():
            return {"success": False, "msg": "CountryCode is wrong."}

        events = self.getEvents(countryCode, eventTypeIds, endTime)
        print(len(events.values.tolist()))
        return {
            "success": True,
            "data": events.values.tolist()
        }

    def getCountries(self):
        countries = self.trading.betting.list_countries()
        countries = pd.DataFrame({
            'Country': [countryResult.country_code for countryResult in countries],
            'MarketCount': [countryResult.market_count for countryResult in countries]
        })
        return countries

    def getEvents(self, countryCode, eventTypeIds, endTime):
        mf = self.makeMarketFilter(
            marketCountries = [countryCode],
            eventTypeIds = eventTypeIds,
            marketStartTime = {
                "to": endTime
            }
        )
        eventsToday = self.trading.betting.list_events(filter=mf)
        eventsTodayObj = pd.DataFrame({
            'Event Name': [eventObject.event.name for eventObject in eventsToday],
            'Event ID': [eventObject.event.id for eventObject in eventsToday],
            'Event Venue': [eventObject.event.venue for eventObject in eventsToday],
            'Country Code': [eventObject.event.country_code for eventObject in eventsToday],
            'Time Zone': [eventObject.event.time_zone for eventObject in eventsToday],
            'Open Date': [eventObject.event.open_date for eventObject in eventsToday],
            'Market Count': [eventObject.market_count for eventObject in eventsToday]
        })
        return eventsTodayObj

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
