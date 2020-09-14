#!/usr/bin/python
from api import get_general_status
import logging
import array
import time
import sys
from datetime import datetime

# ------------------ Parameters ----------------------

buffer         = []
buffer_size    = 5 # How many datasets to accumulate before publishing
period         = 1 # Seconds between readings

# -------------------- Functions ---------------------

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
