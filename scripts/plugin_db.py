#!/usr/bin/python
from api import get_general_status
import logging

# ------------------ Parameters ----------------------
log_level       = logging.DEBUG
log_filename    = 'plugin-db.log'

_period = 1000 # Milliseconds between readings

# -------------------- Functions ---------------------

def _publish():
    logging.debug('Publishing to DB')    

# ----------------- Main Body -------------------------

while True:
    try:
        ... # doing your stuff
    except:
        pass
