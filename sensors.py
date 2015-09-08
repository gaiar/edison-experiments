import pyupm_i2clcd as lcd
import pyupm_grove as grove
import pyupm_th02 as ths
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
        light_sensor = grove.GroveLight(self.PIN_LIGHT)
        light = light_sensor.value()
        self.SensorsData['light'] = light
        return light

    def get_uv_sensor_data(self):
        sensor_value = 0
        sensor_data_sum = 0
        uv = mraa.Aio(self.PIN_UV)
        i = 0
        for i in range(0, 1024):
            sensor_value = uv.read()
            sensor_data_sum += sensor_value
            time.sleep(0.002)
            i += 1
        sensor_data_sum = sensor_data_sum >> 10
        self.SensorsData['uv'] = float(sensor_data_sum * 4980.0 / 1023.0)
        return float(sensor_data_sum * 4980.0 / 1023.0)

    def get_encoder_data(self):
        return ''

    def get_temp_sensor_data(self):
        th02 = ths.TH02()
        temp = ths.getTemperature()
        self.SensorsData['temp'] = temp
        return temp

    def get_humidity_sensor_data(self):
        temp = ths.getHumidity()
        self.SensorsData['humidity'] = temp
        return temp


    def set_lcd_date(self):
        return ''

