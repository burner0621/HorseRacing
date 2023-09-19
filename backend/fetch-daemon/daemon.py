# Import libraries
import betfairlightweight
from betfairlightweight import filters
import pandas as pd
import numpy as np
import os
import datetime
import json

trading = None


def login():
    try:
        trading.login()
        print("===   Login successful.   ===")
    except Exception as e:
        print(f"Login failed: {str(e)}")


def connectDatabase():
    import mysql.connector
    try:
        with open('./config/db.json') as f:
            dbConfig = json.load(f)
            username = dbConfig['username']
            password = dbConfig['password']
            dbname = dbConfig['dbname']
            host = dbConfig['host']
    except Exception as e:
        print(f"config/db.json file read failed. {str(e)}")
        return

    try:
        mydb = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=dbname
        )
        print("===   Database Connection successful.   ===")
    except Exception as e:
        print(f"Database connection failed. {str(e)}")
        return

    return mydb


def getCountries():
    countries = trading.betting.list_countries()
    countries = pd.DataFrame({
        'Country': [country_result.country_code for country_result in countries],
        'MarketCount': [country_result.market_count for country_result in countries]
    }).set_index('Country').sort_index()

    return countries


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
def getEvents(cc):
    print ("fff")


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
