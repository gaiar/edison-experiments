__author__ = 'gaiar'
import upm
import mraa
import time



class Sensors:
    SensorsData = []

    PIN_BUZZER = 4
    PIN_LIGHT = 2
    PIN_UV = 3
    PIN_LED = 3
    PIN_ENCODER = 2
    PIN_BUTTON = 1
    PIN_SOUND = 7
    PIN_RELAY = 5



    def get_moisture_sensor_data(self):

        return ''

    def get_light_sensor_data(self):

        return ''

    def get_uv_sensor_data(self):
        sensor_value = 0
        sum = 0
        uv = mraa.Aio(self.PIN_UV)
        i=0
        for i in range(0,1024):
            sensor_value = uv.read()
            sum +=sensor_value
            time.sleep(0.002)
            i+=1
        sum = sum >> 10
        self.SensorsData['uv'] = float(sum*4980.0/1023.0)
        return float(sum*4980.0/1023.0)

    def get_encoder_data(self):
        return ''
    def get_ths_sensor_data(self):

        return ''