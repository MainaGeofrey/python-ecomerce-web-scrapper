import os
from dotenv import load_dotenv
import logging as Log
import logging.handlers
from logging import ERROR
 
handler = Log.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "../logs/scrap.log"))
formatter = Log.Formatter(Log.BASIC_FORMAT)
handler.setFormatter(formatter)
root = Log.getLogger()
  #The application will now log all messages with level INFO or above to file
  
"""include DEBUG and INFO levels""" #
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)

"""handle exception"""
"""make like php invokeable class """ ## i.e      something like this   Log.info(datetime.now())

class Logger:
    def __init__(self, level, message, file):
        self.level = level
        self.message = message
        self.file = file
        
    
    def log_fu