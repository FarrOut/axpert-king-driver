#!/usr/bin/python
from api import get_general_status
import logging
import json

# ------------------ Parameters ----------------------
_period = 1000 # Milliseconds between readings

# -------------------- Functions ---------------------

def _get_json():
    logging.debug('Converting to JSON')
    _json = json.dumps(get_general_status())
    return _json

# ----------------- Main Body -------------------------

print(_get_json())
