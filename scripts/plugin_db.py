#!/usr/bin/python
from api import get_general_status
import logging
import traceback
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
db_table          = 'inverter'
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

#
# This is the momement where Python Object becomes SQL...
#
def _addRecord(_timestamp, _volt):
    _sql = 'INSERT INTO ' + db_table + ' (Timestamp, GridVoltage) VALUES ('+ _timestamp + ',' + _volt + ')'

    _mycursor = db.cursor()
    _mycursor.execute(_sql)

def _publish(_batch):
    try:
        logging.debug('Publishing to DB')
        for _r in _batch:
            _timestamp, _grid_voltage = _r
            _addRecord(_timestamp, grid_voltage)

        db.commit()
    except Exception as e:
        raise

def _parse_data(_data):

    _timestamp  = datetime.now()
    _volt       = _data["grid_voltage"]

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

# while True:
for x in range(2):
    try:
        _data = get_general_status()
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
    except Exception as e:
        traceback.print_exc()
        logging.exception('Fatal Error')
        sys.exit(1)
