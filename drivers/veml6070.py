import ustruct
import time
from micropython import const

_VEML6070_ADDR_ARA  = const(0x18 >> 1)
_VEML6070_ADDR_CMD  = const(0x70 >> 1)
_VEML6070_ADDR_LOW  = const(0x71 >> 1)
_VEML6070_ADDR_HIGH = const(0x73 >> 1)

_VEML6070_INTEGRATION_TIME = { "VEML6070_HALF_T": [0x00, 0],
                               "VEML6070_1_T": [0x01, 1],
                               "VEML6070_2_T": [0x02, 2],
                               "VEML6070_4_T": [0x03, 4]
                             }

# UV Risk Level dictionary. [0],[1] are the lower and uppper bounds of the range
_VEML6070_RISK_LEVEL = { "LOW": [0, 560],
                         "MODERATE": [561, 1120],
                         "HIGH": [1121, 1494],
                         "VERY HIGH": [1495, 2054],
                         "EXTREME": [2055, 9999]
                       }

class VEML6070:
    def __init__(self, i2c, _veml6070_it="VEML6070_1_T", ack=False):
        self.i2c = i2c
        # Check if the IT is valid
        if _veml6070_it not in _VEML6070_INTEGRATION_TIME:
            raise ValueError('Integration Time invalid. Valid values are: ',
                             _VEML6070_INTEGRATION_TIME.keys())

        # Check if ACK is valid
        if ack not in (True, False):
            raise ValueError("ACK must be 'True' or 'False'.")
        
        # Passed checks; set self values
        self._ack = int(ack)
        self._ack_thd = 0x00
        self._it = _veml6070_it
        
        ara_buf = bytearray(1)
        try:
            self.i2c.readfrom_into(_VEML6070_ADDR_ARA, ara_buf)
        except OSError:
            pass
        
        self.buf = bytearray(1)
        self.buf[0] = self._ack << 5 | _VEML6070_INTEGRATION_TIME[self._it][0] << 2 | 0x02
        self.i2c.writeto(_VEML6070_ADDR_CMD, self.buf)
    
    @property
    def uv_raw(self):
        """
        Reads and returns the value of the UV intensity.
        """
        lsb = bytearray(1)
        msb = bytearray(1)
        
        self.i2c.readfrom_into(_VEML6070_ADDR_LOW, lsb)
        self.i2c.readfrom_into(_VEML6070_ADDR_HIGH, msb)

        return msb[0] << 8 | lsb[0]
    
    def get_index(self, _raw):
        """
        Calculates the UV Risk Level based on the captured UV reading. Requres the ``_raw``
        argument (from ``veml6070.uv_raw``). Risk level is available for Integration Times (IT)
        1, 2, & 4. The result is automatically scaled to the current IT setting.
            LEVEL*        UV Index
            =====         ========
            LOW             0-2
            MODERATE        3-5
            HIGH            6-7
            VERY HIGH       8-10
            EXTREME         >=11
        * Not to be considered as accurate condition reporting.
          Calculation is based on VEML6070 Application Notes:
          http://www.vishay.com/docs/84310/designingveml6070.pdf
        """

        # get the divisor for the current IT
        div = _VEML6070_INTEGRATION_TIME[self._it][1]
        if div == 0:
            raise ValueError(
                "[veml6070].get_index only available for Integration Times 1, 2, & 4.",
                "Use [veml6070].set_integration_time(new_it) to change the Integration Time."
                )

        # adjust the raw value using the divisor, then loop through the Risk Level dict
        # to find which range the adjusted raw value is in.
        raw_adj = int(_raw / div)
        for levels in _VEML6070_RISK_LEVEL:
            tmp_range = range(_VEML6070_RISK_LEVEL[levels][0],
                              _VEML6070_RISK_LEVEL[levels][1])
            if raw_adj in tmp_range:
                risk = levels
                break

        return risk