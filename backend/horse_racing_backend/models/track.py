from mongoengine import *
import datetime
from .colManager import ColManager

import sys
sys.path.append ("..")
from utils.logging import eventLogger

class Track(ColManager):
    def __init__(self, database):
        super().__init__(database, "Track")
    
    def saveTrack(self, track_obj):
        pass
    