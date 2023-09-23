import sys
sys.path.append ("..")
from utils.logging import colManagerLogger

class ColManager:
    def __init__(self, database, colName):
        if database is None:
            colManagerLogger.error ("database object is None.")
            return None
        if colName is None or len(colName.strip()) == 0:
            colManagerLogger.error ("Collection Name is None or empty.")
            return None
        self.database = database
        self.colName = colName
        try:
            self.manager = self.database [self.colName]
        except Exception as e:
            colManagerLogger.error ("%s collection calling failed" % colName, exc_info=True)
    
    def insertMany (self, dList):
        return self.manager.insert_many (dList)