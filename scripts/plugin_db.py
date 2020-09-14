#!/usr/bin/python
from api import get_general_status
import logging
import array
import time
import sys

# ------------------ Parameters ----------------------

buffer         = []
buffer_size    = 5
period         = 1 # Seconds between readings

# -------------------- Functions ---------------------

def _publish(_batch):
    try:
        print('Publishing:',_batch)
        logging.debug('Publishing to DB')
        return True
    except:
        return False

# ----------------- Main Body -------------------------
logging.info('Starting worker.')

while True:
    try:
        buffer.append(get_general_status())
                
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
