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

# ------------------ API Commands ----------------------

def get_general_status():
    logging.debug('Querying device general status...')
    _cmd = 'QPIGS'
    _crc = 'ss'
    _res, _crc_valid = _send_command(_cmd, _crc)
    print('Result received:' + str(_res)) #TODO debugging

    _regex = r"\b(\d{1,3}\.?\d{0,2})\b"
    _match = re.search(_regex, str(_res))
    _matches = [x.group() for x in re.finditer( _regex, str(_res))]

    _grid_volt                      = _matches[0]
    _grid_freq                      = _matches[1]
    _ac_output_volt                 = _matches[2]
    _ac_output_freq                 = _matches[3]
    _ac_output_apparent_power       = _matches[4]
    _ac_output_active_power         = _matches[5]
    _output_load_perc               = _matches[6]
    _bus_volt                       = _matches[7]
    _battery_volt                   = _matches[8]
    _battery_charging_current       = _matches[9]
    _battery_capacity               = _matches[10]
    _inverter_heat_sink_temp        = _matches[11]
    # _pv_input_current_for_battery   = _matches[12]
    # _pv_input_volt                  = _matches[13]
    # _battery_volt_from_scc          = _matches[14]
    # _battery_discharge_current      = _matches[15]
    # _device_status                  = _matches[16]

    _dataset = {
        "query_cmd": _cmd,
        "data": {
            "grid_voltage": _grid_volt
        }
    }

    _json = json.dumps(_dataset)

    print(_json)

# ------------------ Generic Functions ----------------------

def _send_command(_cmd, _crc):
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

con = serial.Serial(port=port, baudrate=baudrate, parity=parity, stopbits=stopbits, write_timeout=write_timeout, timeout=read_timeout)

get_general_status()
