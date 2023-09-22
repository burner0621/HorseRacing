
import pandas as pd
import numpy as np
import os
import datetime
import json

from betfairs.trading import tradingObj
from utils.logging import daemonLogger

def connectDatabase():
    from mongoengine import connect
    try:
        with open('./config/db.json') as f:
            dbConfig = json.load(f)
            dbname = dbConfig['dbname']
            host = dbConfig['host']
            port = dbConfig['port']
            username = dbConfig['username']
            password = dbConfig['password']
        try:
            connect (db=dbname, username=username, password=password, host="mongodb://%s:%s@%s:%d/%s" %(username, password, host, port, dbname))
            daemonLogger.info("===   Database Connection successful.   ===")
        except Exception as e:
            daemonLogger.debug(f"Database connection failed.", exc_info=True)
            return
    except Exception as e:
        daemonLogger.debug(f"config/db.json file read failed.", exc_info=True)
        return

def main():
    connectDatabase()
    print (tradingObj.getCountries())

if __name__ == "__main__":
    main()
