# Import libraries
import betfairlightweight
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
                        'wallet': mc.description.wallet if mc.description.wallet is not None else '',
                        'raceType': mc.description.race_type if mc.description.race_type is not None else ''
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
                
                marketBooks = self.getMarketBooks ([tmp['marketId']])
                tmp['marketBook'] = marketBooks[0]
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
                    # marketTypeCodes=['WIN']
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

                martketCatalogues = self.getListMarketCatalog (eventObject.market_count, [event['eventId']])
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

    def getMarketBooks (self, marketIds):
        try:
            priceFilter = self.getPriceFilter (['EX_BEST_OFFERS', 'SP_AVAILABLE', 'SP_TRADED', 'EX_ALL_OFFERS', 'EX_TRADED'])
            marketBooks = self.trading.betting.list_market_book (market_ids = marketIds, price_projection=priceFilter)
            return self.convertMarketBookToData (marketBooks)
        except Exception as e:
            return []
    def convertMarketBookToData (self, marketBooks):
        try:
            marketBooksList = []
            for marketBook in marketBooks:
                tmp = {}
                tmp['betDelay'] = marketBook.bet_delay if marketBook.bet_delay is not None else 0
                tmp['bspReconciled'] = marketBook.bsp_reconciled if marketBook.bsp_reconciled is not None else None
                tmp['complete'] = marketBook.complete if marketBook.complete is not None else None
                tmp['crossMatching'] = marketBook.cross_matching if marketBook.cross_matching is not None else None
                tmp['inplay'] = marketBook.inplay if marketBook.inplay is not None else None
                tmp['isMarketDataDelayed'] = marketBook.is_market_data_delayed if marketBook.is_market_data_delayed is not None else None
                tmp['lastMatchTime'] = marketBook.last_match_time if marketBook.last_match_time is not None else None
                tmp['marketId'] = marketBook.market_id if marketBook.market_id is not None else ''
                tmp['numbersOfActiveRunners'] = marketBook.number_of_active_runners if marketBook.number_of_active_runners is not None else 0
                tmp['numbersOfWinners'] = marketBook.number_of_winners if marketBook.number_of_winners is not None else 0
                tmp['numbersOfRunners'] = marketBook.number_of_runners if marketBook.number_of_runners is not None else 0
                tmp['publishTime'] = marketBook.publish_time if marketBook.publish_time is not None else None
                tmp['runnersVoidable'] = marketBook.runners_voidable if marketBook.runners_voidable is not None else None
                tmp['status'] = marketBook.status if marketBook.status is not None else ''
                tmp['totalAvailable'] = marketBook.total_available if marketBook.total_available is not None else 0
                tmp['totalMatched'] = marketBook.total_matched if marketBook.total_matched is not None else 0
                tmp['version'] = marketBook.version if marketBook.version is not None else 0

                if marketBook.streaming_update is not None:
                    su = marketBook.streaming_update
                    tmp['rc'] = su['rc'] if 'rc' in su else {}

                if marketBook.market_definition is not None:
                    md = marketBook.market_definition
                    tmpMd = {}
                    tmpMd['bettingType'] = md.betting_type if md.betting_type is not None else ''
                    tmpMd['bspMarket'] = md.bsp_market if md.bsp_market is not None else None
                    tmpMd['discountAllowed'] = md.bsp_market if md.discount_allowed is not None else None
                    tmpMd['eventId'] = md.event_id if md.event_id is not None else 0
                    tmpMd['eventTypeId'] = md.event_id if md.event_type_id is not None else 0
                    tmpMd['marketBaseRate'] = md.market_base_rate if md.market_base_rate is not None else 0
                    tmpMd['marketTime'] = md.market_time if md.market_time is not None else None
                    tmpMd['marketType'] = md.market_type if md.market_type is not None else ''
                    tmpMd['openDate'] = md.open_date if md.open_date is not None else None
                    tmpMd['persistenceEnabled'] = md.persistence_enabled if md.persistence_enabled is not None else None
                    tmpMd['regulators'] = md.regulators if md.regulators is not None else ''
                    tmpMd['settledTime'] = md.settled_time if md.settled_time is not None else None
                    tmpMd['suspendTime'] = md.suspend_time if md.suspend_time is not None else None
                    tmpMd['timezone'] = md.timezone if md.timezone is not None else ''
                    tmpMd['turnInPlayEnabled'] = md.turn_in_play_enabled if md.turn_in_play_enabled is not None else None
                    tmpMd['venue'] = md.venue if md.venue is not None else ''
                    tmpMd['raceType'] = md.race_type if md.race_type is not None else ''

                    tmp['marketDefinition'] = tmpMd

                if marketBook.runners is not None:
                    runners = []
                    for runner in marketBook.runners:
                        tmpRunner = {}
                        tmpRunner['adjustmentFactor'] = runner.adjustment_factor if runner.adjustment_factor is not None else 0
                        tmpRunner['handicap'] = runner.handicap if runner.handicap is not None else 0
                        tmpRunner['lastPriceTraded'] = runner.last_price_traded if runner.last_price_traded is not None else 0
                        tmpRunner['removalDate'] = runner.removal_date if runner.removal_date is not None else None
                        tmpRunner['selectionId'] = runner.selection_id if runner.selection_id is not None else 0
                        tmpRunner['status'] = runner.status if runner.status is not None else ''
                        tmpRunner['totalMatched'] = runner.total_matched if runner.total_matched is not None else 0
                        tmpRunner['ex'] = {
                            'availableToBack':[{
                                "price": atb.price,
                                "size": atb.size
                            } for atb in runner.ex.available_to_back] if runner.ex.available_to_back is not None or len(runner.ex.available_to_back) == 0 else [],
                            'availableToLay':[{
                                "price": atl.price,
                                "size": atl.size
                            } for atl in runner.ex.available_to_lay] if runner.ex.available_to_lay is not None or len(runner.ex.available_to_lay) == 0 else [],
                            'tradedVolume':[{
                                "price": tv.price,
                                "size": tv.size
                            } for tv in runner.ex.traded_volume] if runner.ex.traded_volume is not None or len(runner.ex.traded_volume) == 0 else [],
                        } if runner.ex is not None else {}
                        tmpRunner['sp'] = {
                            'actualSp': runner.sp.actual_sp if runner.sp.actual_sp is not None else 0,
                            'farPrice': runner.sp.far_price if runner.sp.far_price is not None else 0,
                            'nearPrice': runner.sp.near_price if runner.sp.near_price is not None else 0,
                            'backStakeTaken': [{
                                "price": bst.price,
                                "size": bst.size
                            } for bst in runner.sp.back_stake_taken] if runner.sp.back_stake_taken is not None or len(runner.sp.back_stake_taken) == 0 else [],
                            'layLiabilityTaken': [{
                                "price": llt.price,
                                "size": llt.size
                            } for llt in runner.sp.lay_liability_taken] if runner.sp.lay_liability_taken is not None or len(runner.sp.lay_liability_taken) == 0 else [],
                        } if runner.sp is not None else {}
                        tmpRunner['matches'] = [{
                            "betId": rbm.bet_id if rbm.bet_id is not None else '',
                            "matchDate": rbm.match_date,
                            "matchId": rbm.match_id if rbm.match_id is not None else '',
                            "price": rbm.price if rbm.price is not None else 0,
                            "side": rbm.side if rbm.side is not None else '',
                            "size": rbm.size if rbm.size is not None else 0,
                        } for rbm in runner.matches] if runner.matches is not None or len(runner.matches) == 0 else []
                        tmpRunner['orders'] = [{
                            "avgPriceMatched": rbo.avg_price_matched if rbo.avg_price_matched is not None else 0,
                            "betId": rbo.bet_id if rbo.bet_id is not None else '',
                            "bspLiability": rbo.bsp_liability if rbo.bsp_liability is not None else 0,
                            "orderType": rbo.order_type if rbo.order_type is not None else '',
                            "persistenceType": rbo.persistence_type if rbo.persistence_type is not None else '',
                            "placedDate": rbo.placed_date if rbo.placed_date is not None else None,
                            "price": rbo.price if rbo.price is not None else 0,
                            "side": rbo.side if rbo.side is not None else '',
                            "sizeCancelled": rbo.size_cancelled if rbo.size_cancelled is not None else None,
                            "sizeLapsed": rbo.size_lapsed if rbo.size_lapsed is not None else 0,
                            "sizeMatched": rbo.size_matched if rbo.size_matched is not None else 0,
                            "sizeRemaining": rbo.size_remaining if rbo.size_remaining is not None else 0,
                            "sizeVoided": rbo.size_voided if rbo.size_voided is not None else 0,
                            "status": rbo.status if rbo.status is not None else '',
                        } for rbo in runner.orders] if runner.orders is not None or len(runner.orders) == 0 else []

                        runners.append (tmpRunner)
                    tmp['runners'] = runners

                marketBooksList.append (tmp)
            return marketBooksList
        except Exception as e:
            tradingLogger.error ("getMarketBooks() function call failed.", exc_info=True)
            return []

    def getPriceFilter (self, priceData):
        return betfairlightweight.filters.price_projection (
            price_data=priceData,
        )
    
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