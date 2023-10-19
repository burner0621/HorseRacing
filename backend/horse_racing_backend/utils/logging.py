# logging customize

import logging
import logging.config

logging.config.fileConfig(fname='config/logging.conf', disable_existing_loggers=False)

daemonLogger = logging.getLogger("daemon.py")
streamLogger = logging.getLogger("stream.py")
tradingLogger = logging.getLogger("betfairs/trading")
basicControllerLogger = logging.getLogger("controllers/basicConttroller")
profileControllerLogger = logging.getLogger("controllers/profileConttroller")
dbLogger = logging.getLogger("models/dbManager")
colManagerLogger = logging.getLogger("models/colManager")
eventLogger = logging.getLogger("models/event")
marketBookLogger = logging.getLogger("models/marketBook")
marketIdsLogger = logging.getLogger("models/marketIds")
trackLogger = logging.getLogger("models/track")
horseLogger = logging.getLogger("models/horse")
raceLogger = logging.getLogger("models/race")
algoLogger = logging.getLogger("prompts/algo")
utilsLogger = logging.getLogger("utils")