from mongoengine import *
import datetime
from .colManager import ColManager

import sys
sys.path.append ("..")
from utils.logging import eventLogger
from utils import getTimeRangeOfCountry

class MarketBook(ColManager):
    def __init__(self, database):
        super().__init__(database, "MarketBook")
    
    def insert(self, mb):
        self.manager.insert_one (mb)