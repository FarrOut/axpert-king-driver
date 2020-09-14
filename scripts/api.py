#!/usr/bin/python

from driver import send_command

import time
import logging
import sys
import re

# ------------------ API Commands ----------------------

def get_general_status():
    logging.debug('Querying device general status...')
    _cmd = 'QPIGS'
    _crc = 'ss'
    _res, _crc_valid = send_command(_cmd, _crc)

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

    return _dataset

# -------------------- Main Body ----------------------------
