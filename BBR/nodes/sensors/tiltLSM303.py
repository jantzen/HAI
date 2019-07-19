from BBR.nodes.sensors.tilt import Tilt
import Adafruit_LSM303
import time
import struct

class Tilt_LSM303( Tilt ):
    def __init__(self, efferents, LSM303_REGISTER_ACCEL_OUT_X_L_A, LSM303_ADDRESS_ACCEL,LSM303_REGISTER_ACCEL_CTRL_REG1_A, i2c=None,delay=0.1, **kwargs):
        Tilt.__init__(self, efferents, delay)
        self._accel_out = LSM303_REGISTER_ACCEL_OUT_X_L_A
        self._accel_address = LSM303_ADDRESS_ACCEL
        self._accel_register = LSM303_REGISTER_ACCEL_CTRL_REG1_A
         
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C

        self._accel = i2c.get_i2c_device(self._accel_address, **kwargs)
        self._accel.write8(self._accel_register, 0X27)


    def read(self):
        accel_raw = self._accel.readList(self._accel_out | 0X80, 6)
        accel = struct.unpack('<hhh', accel_raw)
        accel = (accel [0] >> 4, accel [1] >> 4, accel [2] >>4)

        
        if(accel[0] < -175 or accel[0] > 350 or accel[1]>475 or accel[1] < -550 ):
            return 1
        else:
            return 0



       
        
          
