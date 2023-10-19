from mongoengine import *
import datetime
from .colManager import ColManager

import sys
sys.path.append ("..")
from utils.logging import marketBookLogger

class MarketBook(ColManager):
    def __init__(self, database):
        super().__init__(database, "MarketBook")
    
    def insert(self, mb):
        self.manager.insert_one (mb)
    
    def saveBook(self, mb):
        if mb['publishTime'] is None or mb['publishTime'] == '': return
        try:
            count = self.manager.count_documents ({'marketId': mb['marketId'], 'publishTime': mb['publishTime']})
            if count > 0:
                self.manager.update_one(
                    {'marketId': mb['marketId'], 'publishTime': mb['publishTime']},
                    {"$set": mb}
                )
            else:
                self.manager.insert_one (mb)
        except:
            marketBookLogger.error ("saveBook() call failed", exc_info=True)
    
    def getDocumentsByID(self, market_id, match={}):
        match['marketId'] = market_id
        mbs = list(self.manager.find(match).sort("publishTime", -1))
        if len(mbs) == 0: return []
        tmp = []
        for mb in mbs:
            tmp_runners = []
            for runner in mb['runners']:
                if runner['status'] == 'ACTIVE':
                    tmp_runners.append (runner)
            mb['runners'] = tmp_runners
            tmp.append (mb)
        return tmp