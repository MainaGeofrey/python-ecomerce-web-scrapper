import logging.config
import sys
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv



from logger import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)
Log = logging.getLogger(__name__)
Log.info("Configuring logging")

class MySQLConnection:
    #def __init__(self, host, user, password, database, ssl_ca=None):
    def __init__(self) -> None:
        load_dotenv()
        
        self.host = os.environ.get('DB_HOST')
        self.user = os.environ.get('DB_USERNAME')
        self.password = os.environ.get('DB_PASSWORD')
        self.database = os.environ.get('DB_CONNECTION')
        self.ssl_ca = None
        
        #'ssl_verify_cert': True,  # enable SSL verification
        #'ssl_ca': '/path/to/ca.pem',  # path to CA certificate

    def connect(self):
        config = {
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'database': self.database,
            'ssl_verify_cert': True if self.ssl_ca else False,
            'ssl_ca': self.ssl_ca,
        }
        
        try:
            self.conn = mysql.connector.connect(**config)
            self.cursor = self.conn.cursor()
        except ERROR as error:
            """Log error"""
            pass

    def execute(self, query, params=None):
        if not self.conn:
            self.connect()
            
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except ERROR as error:
            """Log error"""
            pass
        

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except ERROR as error:
            """Log error"""
            pass
