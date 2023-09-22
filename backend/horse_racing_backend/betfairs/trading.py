# Import libraries
import betfairlightweight
from betfairlightweight import filters
import pandas as pd
import json

import sys
sys.path.append ("..")
from utils.logging import tradingLogger

class Trading:
    def __init__(self):
        self.trading = None
        try:
            with open('./config/credentials.json') as f:
                cred = json.load(f)
                my_username = cred['username']
                my_password = cred['password']
                my_app_key = cred['app_key']
                certs_path = cred['certs_path']
                        
            self.trading = betfairlightweight.APIClient(username=my_username,
                                                password=my_password,
                                                app_key=my_app_key,
                                                certs=certs_path)
            self.login ()
        except Exception as e:
            tradingLogger.debug(f"config/credentials.json file read failed.", exc_info = True)
            return      

    def login(self):
        try:
            self.trading.login()
            tradingLogger.info("===   Login successful.   ===")
        except Exception as e:
            tradingLogger.debug(f"Login failed", exc_info=True)

    def getCountries(self):
        try:
            countries = self.trading.betting.list_countries()
            countries = pd.DataFrame({
                'Country': [country_result.country_code for country_result in countries],
                'MarketCount': [country_result.market_count for country_result in countries]
            }).set_index('Country').sort_index()

            return countries
        except Exception as e:
            tradingLogger.debug ("getCountries() failed.", exc_info=True)
            return []

    def getListMarketCatalog(self, maxNum, eventIds):
        mf = self.makeMarketFilter(eventIds=eventIds)
        try:
            market_catalogues = self.trading.betting.list_market_catalogue(
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
            return tmp
        except Exception as e:
            tradingLogger.debug ("getListMarketCatalog() failed.", exc_info=True)
            return None

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
        try:
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
        except Exception as e:
            tradingLogger.debug ("makeMarketFilter() failed.", exc_info=True)
            return None

    '''
        cc: country code ====>  e.x   cc: AU
    '''
    def getEvents(self, cc, eventTypeIds):
        try:
            cList = self.getCountries()
            if cc not in [country['Country'] for country in cList]:
                return {"success": False, "msg": "CountryCode is wrong."}
            
            mf = self.makeMarketFilter(
                    marketCountries=[cc],
                    eventTypeIds=eventTypeIds,
                )
            events = self.trading.betting.list_events(filter=mf)

            rlt = []
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

                rlt.append (event)
            
            return rlt
        except Exception as e:
            tradingLogger.debug ("getEvents() failed.", exc_info=True)
            return []
        
tradingObj = Trading ()