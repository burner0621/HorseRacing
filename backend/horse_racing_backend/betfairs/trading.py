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
            tradingLogger.error(f"config/credentials.json file read failed.", exc_info = True)
            return      

    def login(self):
        try:
            self.trading.login()
            tradingLogger.info("===   Login successful.   ===")
        except Exception as e:
            tradingLogger.error(f"Login failed", exc_info=True)

    def getCountries(self):
        try:
            countries = self.trading.betting.list_countries()
            cList = [{'Country': countryResult.country_code,
                  'MartketCount': countryResult.market_count} for countryResult in countries]

            return cList
        except Exception as e:
            tradingLogger.error ("getCountries() failed.", exc_info=True)
            return []

    def getListMarketCatalog(self, maxNum, eventIds):
        mf = self.makeMarketFilter(eventIds=eventIds)
        try:
            market_catalogues = self.trading.betting.list_market_catalogue(
                filter=mf,
                max_results=str (maxNum),
                sort='FIRST_TO_START',
                market_projection=['MARKET_DESCRIPTION', 'EVENT', 'COMPETITION', 'RUNNER_DESCRIPTION', 'RUNNER_METADATA', 'MARKET_START_TIME']
            )
            rlt  = []
            for mc in market_catalogues:
                tmp = {
                    'marketName': mc.market_name if mc.market_name is not None else '',
                    'marketId': mc.market_id if mc.market_id is not None else '',
                    'marketStartTime': mc.market_start_time if mc.market_start_time is not None else None, # datetime.datetime
                    'totalMatched': mc.total_matched if mc.total_matched is not None else 0,
                    'marketCatalogueDescription': {
                        'bettingType': mc.description.betting_type if mc.description.betting_type is not None else '',
                        'bspMarket': mc.description.bsp_market if mc.description.bsp_market is not None else None,
                        'clarifications': mc.description.clarifications if mc.description.clarifications is not None else '',
                        'discountAllowed': mc.description.discount_allowed if mc.description.discount_allowed is not None else None, #bool
                        'eachWayDivisor': mc.description.each_way_divisor if mc.description.each_way_divisor is not None else '',
                        'marketBaseRate': mc.description.market_base_rate if mc.description.market_base_rate is not None else 0,
                        'marketTime': mc.description.market_time if mc.description.market_time is not None else None, #datetime.datetime
                        'marketType': mc.description.market_type if mc.description.market_type is not None else '',
                        'persistenceEnalbled': mc.description.persistence_enabled if mc.description.betting_type is not None else None, #bool
                        'regulator': mc.description.regulator if mc.description.regulator is not None else '',
                        'rules': mc.description.rules if mc.description.rules is not None else '',
                        'rulesHasDate': mc.description.rules_has_date if mc.description.rules_has_date is not None else None, #bool
                        'suspendTime': mc.description.suspend_time if mc.description.suspend_time is not None else None,
                        'turnInPlayEenabled': mc.description.turn_in_play_enabled if mc.description.turn_in_play_enabled is not None else None, #bool
                        'wallet': mc.description.wallet if mc.description.wallet is not None else ''
                    }
                }
                if mc.competition is not None:
                    tmp['competition'] = {
                        'id': mc.competition.id if mc.competition.id is not None else 0,
                        'name': mc.competition.name if mc.competition.name is not None else ''
                    }
                if mc.event is not None:
                    tmp['eventId'] = int(mc.event.id)
                if mc.runners is not None:
                    tmpRunners = []
                    profitAndLoses = self.getMarketProfitAndLoss ([tmp['marketId']])
                    for runner in mc.runners:
                        tmpRunner = {
                            "handicap": runner.handicap if runner.handicap is not None else 0,
                            "metadata": runner.metadata if runner.metadata is not None else {},
                            "runnerName": runner.runner_name if runner.runner_name is not None else '',
                            "selectionId": runner.selection_id if runner.selection_id is not None else 0,
                            "sortPriority": runner.sort_priority if runner.sort_priority is not None else 0
                        }
                        tmpRunners.append (tmpRunner)
                    if profitAndLoses is not None:
                        profitAndLosesDict = {str(pl['selectionId']): pl for pl in profitAndLoses}
                        tmpRunnersWithPL = tmpRunners; tmpRunners = []
                        for runner in tmpRunnersWithPL:
                            if str(runner['selectionId']) in profitAndLosesDict:
                                dictObj = profitAndLosesDict[str(runner['selectionId'])]
                                if dictObj['commissionAplied'] != 0: runner['commissionAplied'] = dictObj['commissionAplied']
                                if dictObj['ifLoss'] != 0: runner['ifLoss'] = dictObj['ifLoss']
                                if dictObj['ifWin'] != 0: runner['ifWin'] = dictObj['ifWin']
                                if dictObj['ifPlace'] != 0: runner['ifPlace'] = dictObj['ifPlace']
                            tmpRunners.append (runner)

                    tmp['runners'] = tmpRunners
                rlt.append (tmp)
            return rlt
        except Exception as e:
            tradingLogger.error ("getListMarketCatalog() failed.", exc_info=True)
            return []

    '''
        cc: country code ====>  e.x   cc: AU
    '''
    def getEvents(self, cc, eventTypeIds):
        try:
            cList = self.getCountries()
            cc = cc.upper()
            if cc not in [country['Country'] for country in cList]:
                tradingLogger.error ("Country code: \"%s\" is wrong. Please enter the correct parameters." % cc, exc_info=True)
            
            mf = self.makeMarketFilter(
                    marketCountries=[cc],
                    eventTypeIds=eventTypeIds,
                )
            events = self.trading.betting.list_events(filter=mf)

            rlt = []
            for eventObject in events:
                event = {
                    'eventId': int(eventObject.event.id) if eventObject.event.id is not None else 0,
                    'eventName': eventObject.event.name if eventObject.event.name is not None else '',
                    'eventVenue': eventObject.event.venue if eventObject.event.venue is not None else '',
                    'timeZone': eventObject.event.time_zone if eventObject.event.time_zone is not None else '',
                    'openDate': eventObject.event.open_date if eventObject.event.open_date is not None else None, # datetime.datetime
                    'marketCount': eventObject.market_count if eventObject.market_count is not None else 0,
                    'countryCode': eventObject.event.country_code if eventObject.event.country_code is not None else '',
                    'markets': []
                }

                martketCatalogues = self.getListMarketCatalog (50, [event['eventId']])
                event['markets'] = martketCatalogues

                rlt.append (event)
            
            return rlt
        except Exception as e:
            tradingLogger.error ("getEvents() failed.", exc_info=True)
            return []

    def getMarketProfitAndLoss(self, marketIds, includeBspBets = 'true', includeSettledBets = 'true'):
        if  isinstance(marketIds, list) == False:
            tradingLogger.error ("market_ids parameter is not list: %s" % str(marketIds), exc_info=True)
            return None
        if len (marketIds) == 0:
            tradingLogger.error ("market_ids parameter is emtpy: %s" % str(marketIds), exc_info=True)
            return None
        if includeBspBets not in ['true', 'false']:
            tradingLogger.error ("include_bsp_bets parameter is wrong: %s" % includeBspBets, exc_info=True)
            return None
        if includeSettledBets not in ['true', 'false']:
            tradingLogger.error ("include_settled_bets parameter is wrong: %s" % includeSettledBets, exc_info=True)
            return None
        try:
            pls = self.trading.betting.list_market_profit_and_loss(market_ids=marketIds, include_bsp_bets=includeBspBets, include_settled_bets=includeSettledBets)
            rlt  = []
            if pls is None: return rlt
            for pl in pls:
                for obj in pl.profit_and_losses:
                    tmp = {}
                    tmp['commissionAplied'] = pl.commission_applied if pl.commission_applied is not None else 0
                    tmp['ifLoss'] = obj.if_lose if obj.if_lose is not None else 0
                    tmp['ifWin'] = obj.if_win if obj.if_win is not None else 0
                    tmp['ifPlace'] = obj.if_place if obj.if_place is not None else 0
                    tmp['selectionId'] = obj.selection_id if obj.selection_id is not None else 0
                    rlt.append (tmp)
            return rlt
        except Exception as e:
            tradingLogger.error ("getMarketProfitAndLoss() called failed.", exc_info=True)
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
            tradingLogger.error ("makeMarketFilter() failed.", exc_info=True)
            return None


tradingObj = Trading ()