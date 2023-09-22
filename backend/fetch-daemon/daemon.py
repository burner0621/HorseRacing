# Import libraries
import betfairlightweight
from betfairlightweight import filters
import pandas as pd
import numpy as np
import os
import datetime
import json
import logging

trading = None

def login():
    try:
        trading.login()
        print("===   Login successful.   ===")
    except Exception as e:
        print(f"Login failed: {str(e)}")


def connectDatabase():
    from mongoengine import connect
    try:
        with open('./config/db.json') as f:
            dbConfig = json.load(f)
            mongoUri = dbConfig['mongoUri']
        try:
            connect (mongoUri)
            print("===   Database Connection successful.   ===")
        except Exception as e:
            print(f"Database connection failed. {str(e)}")
            return
    except Exception as e:
        print(f"config/db.json file read failed. {str(e)}")
        return

def getCountries():
    countries = trading.betting.list_countries()
    countries = pd.DataFrame({
        'Country': [country_result.country_code for country_result in countries],
        'MarketCount': [country_result.market_count for country_result in countries]
    }).set_index('Country').sort_index()

    return countries

def getListMarketCatalog(maxNum, eventIds):
    mf = makeMarketFilter(eventIds=eventIds)
    try:
        market_catalogues = trading.betting.list_market_catalogue(
            filter=mf,
            max_results='100',
            sort='FIRST_TO_START'
        )
        rlt  = []
        for mc in market_catalogues:
            tmp = {
                'marketName': mc.market_name,
                'marketId': mc.market_id,
                'marketStartTime': mc.market_start_time, # datetime.datetime
                'total_matched': mc.total_matched,
                'competition': {
                    'id': mc.competition.id,
                    'name': mc.competition.name
                },
                'marketCatalogueDescription': {
                    'bettingType': mc.description.betting_type,
                    'bspMarket': mc.description.bsp_market,
                    'clarifications': mc.description.clarifications,
                    'discountAllowed': mc.description.discountAllowed, #bool
                    'eachWayDivisor': mc.description.each_way_divisor,
                    'marketBaseRate': mc.description.market_base_rate,
                    'marketTime': mc.description.market_time, #datetime.datetime
                    'marketType': mc.description.marketType,
                    'persistenceEnalbled': mc.description.persistence_enalbled, #bool
                    'regulator': mc.description.regulator,
                    'rules': mc.description.rules,
                    'rulesHasDate': mc.description.rulesHasDate, #bool
                    'suspendTime': mc.description.suspendTime,
                    'turnInPlayEenabled': mc.description.turn_in_play_enabled, #bool
                    'wallet': mc.description.wallet
                }
            }
            tmpRunners = []
            for runner in mc.runners:
                tmpRunner = {
                    "handicap": runner.handicap,
                    "metadata": runner.metadata,
                    "runnerName": runner.runner_name,
                    "selectionId": runner.selection_id,
                    "sortPriority": runner.sort_priority
                }
                tmpRunners.append (tmpRunner)
            tmp['runners'] = tmpRunners
            rlt.append (tmp)
    except Exception as e:
        print ()    
    return tmp


def makeMarketFilter(
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


'''
    cc: country code ====>  e.x   cc: AU
'''
def getEvents(cc, eventTypeIds):
    cList = getCountries()
    if cc not in [country['Country'] for country in cList]:
        return {"success": False, "msg": "CountryCode is wrong."}
     
    mf = makeMarketFilter(
            marketCountries=[cc],
            eventTypeIds=eventTypeIds,
        )
    events = trading.betting.list_events(filter=mf)

    for eventObject in events:
        id = eventObject.event.id

        event = {
            'eventId': eventObject.event.id,
            'eventName': eventObject.event.name,
            'eventVenue': eventObject.event.venue,
            'timeZone': eventObject.event.time_zone,
            'openDate': eventObject.event.open_date,
            'marketCount': eventObject.market_count,
            'countryCode': cc
        }


def main():
    try:
        with open('./config/credentials.json') as f:
            cred = json.load(f)
            my_username = cred['username']
            my_password = cred['password']
            my_app_key = cred['app_key']
            certs_path = cred['certs_path']
    except Exception as e:
        print(f"config/credentials.json file read failed. {str(e)}")
        return

    global trading
    trading = betfairlightweight.APIClient(username=my_username,
                                           password=my_password,
                                           app_key=my_app_key,
                                           certs=certs_path)

    login()
    dbObj = connectDatabase()
    getCountries()


if __name__ == "__main__":
    main()
