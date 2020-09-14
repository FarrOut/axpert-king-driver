#!/usr/bin/python
from api import get_general_status
import logging
import array
import time
import sys
from datetime import datetime
import mysql.connector
import threading

# ------------------ Parameters ----------------------

buffer         = []
buffer_size    = 5 # How many datasets to accumulate before publishing
period         = 1 # Seconds between readings

db                = None
db_host           = '10.59.10.34'
db_port           = 3306
db_user           = 'Skyenet'
db_pass           = 'OLZEh1PcXQ5tgESh'
db_name           = 'db_myinverter'
# -------------------- Functions ---------------------

def _create_db_connection(_host, _user, _pass, _database):
    logging.info('Creating connection to database...')

    global db

    try:
        db = mysql.connector.connect(
            database=_database,
            host=_host,
            user=_user,
            password=_pass
        )
        print(db)

    except:
        logging.exception('Error creating connection to database')

def _create_db_table(_name):
    logging.info('Creating table [' + _name +'] on database.')
    mycursor = db.cursor()

    _sql = 'CREATE TABLE IF NOT EXISTS ' + str(_name) + ' ('
    _sql = _sql + 'ID int NOT NULL AUTO_INCREMENT PRIMARY KEY' + ', '
    _sql = _sql + 'Timestamp timestamp' + ', '
    _sql = _sql + 'GridVoltage float'
    _sql = _sql + ')'
    mycursor.execute(_sql)

def _publish(_batch):
    try:
        print('Publishing:',_batch)
        logging.debug('Publishing to DB')
        return True
    except:
        return False

def _parse_data(_dataset):
    _timestamp  = datetime.now()
    _volt       = _dataset["grid_voltage"]

    _record     = (_timestamp, _volt)
    return _record

# ----------------- Main Body -------------------------
# thread = threading.Thread(target=_create_db_connection(db_host, db_user, db_pass, db_name))
# thread.start()

# wait here for the result to be available before continuing
# thread.join()
_create_db_connection(db_host, db_user, db_pass, db_name)
_create_db_table('inverter')

logging.info('Starting worker.')

while True:
    try:
        _data = get_general_status()["data"]
        _record = _parse_data(_data)

        print(_record)
        buffer.append(_record)

        if len(buffer) >= buffer_size:
            _publish(buffer)
            buffer = []

        time.sleep(period)
    except KeyboardInterrupt:
        _msg = 'Task stopped by user. Exiting gracefully.'
        print(_msg)
        logging.info(_msg)
        sys.exit(0)
    except:
        logging.exception('Error publishing data')
