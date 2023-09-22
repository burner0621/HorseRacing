# logging customize

import logging
import logging.config

logging.config.fileConfig(fname='config/logging.conf', disable_existing_loggers=False)

daemonLogger = logging.getLogger("daemon.py")
tradingLogger = logging.getLogger("betfairs/trading")