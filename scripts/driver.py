import serial
import time
import json
import logging

# -------------------- Main Body ----------------------------

con = serial.Serial(port=port, baudrate=baudrate, parity=parity, stopbits=stopbits, write_timeout=write_timeout, timeout=read_timeout)


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

# ------------------ API Commands ----------------------

def get_general_status():


# ------------------ Generic Functions ----------------------

def _send_command(_cmd, _crc):
    logging.DEBUG('Sending', _cmd, 'command to', port, '...')
    con.write(str(_cmd + _crc + cr))
    logging.DEBUG(_cmd, 'command sent to port', port, '. Reading response from device...')
    time.sleep(tx_delay) # Wait for Tx to complete.
    _res = con.read(size=64) #TODO unhardcode buffer size
    logging.DEBUG('Received', _res.size,'byte','response from device on port', port, 'for', _cmd,'command')
    return _res

def _crc_check(expected, actual):
    logging.DEBUG('CRC check...')
