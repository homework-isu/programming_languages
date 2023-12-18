import re

import zmq
from datetime import timezone
import time
import sqlite3
import logging
from datetime import datetime


class LogOperator:

    def __init__(self, db_addr, filepath, env="prod"):
        self.filepath = filepath
        self.conn = sqlite3.connect(db_addr)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME,
                    local_utc INTEGER,
                    data TEXT
                )
            ''')
        if env == "prod":
            self.set_up_logger(filepath, logging.INFO)
        else:
            self.set_up_logger(filepath, logging.DEBUG)
        self.conn.commit()
        self.pattern = re.compile(r'^[ptm].*$', re.IGNORECASE)

    def set_up_logger(self, log_path, level=logging.INFO):
        logging.basicConfig(filename=log_path,
                            level=level,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        self.logger = logging.getLogger(log_path)

    def write_data(self, message):
        ok = self.pattern.search(message)
        if not ok:
            return
        self.logger.debug("received")
        timestamp_utc0 = datetime.now(timezone.utc)
        system_utc_offset = -time.timezone
        self.cursor.execute("INSERT INTO logs (timestamp, local_utc, data) VALUES (?, ?, ?)",
                            (timestamp_utc0, system_utc_offset, message))
        self.conn.commit()


def init_arduino_client(server_addr="tcp://127.0.0.1:5555"):
    context = zmq.Context()
    client = context.socket(zmq.SUB)
    client.connect(server_addr)
    client.subscribe('')
    return client


serverAddr = "tcp://192.168.0.102:5555"
localAddr = "tcp://127.0.0.1:5555"
dbName = "arduino_client_log.db"
log_file_path = 'arduino_client.log'

log_operator = LogOperator(dbName, log_file_path, "prod")
client = init_arduino_client(serverAddr)
time.sleep(1)

timeout = 0.1000
is_available = True
last_time_connected = 0

log_operator.logger.info("Client started")

while True:
    try:
        message = client.recv_string(zmq.NOBLOCK)
        if not is_available:
            log_operator.logger.info("Client works again")
            is_available = True
        #print(f"Received event: {message}")
        log_operator.write_data(message)
        last_time_connected = time.time()
    except zmq.error.Again as e:
        if is_available:
            is_available = False
            #print(f"Error: {e}")
            log_operator.logger.error(str(e))
        time.sleep(timeout)
    except zmq.error.ZMQError as e:
        #print(f"Error: {e}")
        log_operator.logger.error(str(e))

    else:
        time.sleep(1)
