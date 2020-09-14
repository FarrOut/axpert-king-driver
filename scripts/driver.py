#!/usr/bin/python

import serial
import time
import json
import logging
import sys
import re

# ------------------ Parameters ----------------------

port           = 'COM3'
baudrate       = 2400
parity         = serial.PARITY_NONE
stopbits       = serial.STOPBITS_ONE
write_timeout  = 10
read_timeout   = 1
encoding       = 'ascii'
tx_delay       = 0.05 # Time to wait after writing before attempting to read response
cr             = '\r' # Carriage-Return Character


# ------------------ Functions ----------------------
def send_command(_cmd, _crc):
    logging.debug("Sending " + str(_cmd) + " command to port " + str(port))
    con.write(str(_cmd + _crc + cr).encode(encoding))
    logging.debug('Command sent')
    time.sleep(tx_delay) # Wait for Tx to complete.
    _res = con.read(size=64) #TODO unhardcode buffer size
    logging.debug('Received response of ' + str(sys.getsizeof(_res)) + 'byte(s)')
    # _crc_actual = 'Na' #TODO parse from read response
    # _crc_valid = _crc_check(_crc, _crc_actual)
    _crc_valid = bool(True) #TODO  debugging

    return _res.decode(encoding), _crc_valid

def _crc_check(expected, actual):
    logging.debug('CRC check...')
    return bool(true) #TODO override

# -------------------- Main Body ----------------------------
logging.basicConfig(filename='driver.log',level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Define serial connection
con = serial.Serial(port=port, baudrate=baudrate, parity=parity, stopbits=stopbits, write_timeout=write_timeout, timeout=read_timeout)
