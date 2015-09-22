import pyupm_i2clcd as upm_lcd
import pyupm_grove as grove
import pyupm_th02 as ths
import pyupm_rotaryencoder as rotary_encoder
import pyupm_guvas12d as upm_uv
import pyupm_buzzer as upm_buzzer
import pyupm_servo as upm_servo



class Sensors(object):
    SensorsData = {}

    PIN_BUZZER = 6
    PIN_LIGHT = 2
    PIN_UV = 3
    PIN_LED = 3
    PIN_ENCODER1 = 2
    PIN_ENCODER2 = 3
    PIN_BUTTON = 1
    PIN_SOUND = 7
    PIN_RELAY = 5


    GUVAS12D_AREF = 5.0
    SAMPLES_PER_QUERY = 1024

    encoder = rotary_encoder.RotaryEncoder(PIN_ENCODER1, PIN_ENCODER2)
    light_sensor = grove.GroveLight(PIN_LIGHT)
    uv = upm_uv.GUVAS12D(PIN_UV)
    th02 = ths.TH02()
    lcd = upm_lcd.Jhd1313m1(0, 0x3E, 0x62)
    buzzer = upm_buzzer.Buzzer(PIN_BUZZER)
    relay = grove.GroveRelay(0)
    button = grove.GroveButton(8)
    servo = upm_servo.Servo(5)
    led = grove.GroveLed(PIN_LED)

    led_state = False

    def __init__(self):
        self.encoder.initPosition(0)
        self.buzzer.stopSound()
        #self.led.off()

    def get_moisture_sensor_data(self):
        return ''

    def get_light_sensor_data(self):
        light = self.light_sensor.value()
        self.SensorsData['light'] = light
        return light

    def get_uv_sensor_data(self):
        sensor_value = self.uv.value(self.GUVAS12D_AREF, self.SAMPLES_PER_QUERY)
        self.SensorsData['uv'] = sensor_value
        return sensor_value

    def get_encoder_data(self):
        return self.encoder.position()

    def get_temp_sensor_data(self):
        temp = self.th02.getTemperature()
        self.SensorsData['temp'] = temp
        return int(temp)

    def get_humidity_sensor_data(self):
        temp = self.th02.getHumidity()
        self.SensorsData['humidity'] = temp
        return int(temp)

    def show_temp_and_humidity(self):
        self.lcd.clear()
        self.lcd.write(" Temp&Humidity  ")
        # lcd.write("<-")
        self.lcd.setCursor(1, 1)
        self.lcd.write(str(Sensors().get_temp_sensor_data()) + "C ")
        self.lcd.setCursor(1, 9)
        self.lcd.write(str(Sensors().get_humidity_sensor_data()) + "%")

    def show_light_and_uv(self):
        self.lcd.clear()
        self.lcd.write(" Light&UV  ")
        # lcd.write("<-")
        self.lcd.setCursor(1, 1)
        self.lcd.write(str(Sensors().get_light_sensor_data()))
        self.lcd.setCursor(1, 9)
        self.lcd.write(str(Sensors().get_uv_sensor_data()))

    def set_buzzer(self, value):
        self.buzzer.playSound(upm_buzzer.SI, 100000)

    def switch_light(self):
        print ('Current state:'+str(self.led_state))
        if (self.led_state):
            print ('LED OFF')
            self.led.off()
        else:
            print ('LED ON')
            self.led.on()

        self.led_state = not self.led_state
        print ('Switched state:'+str(self.led_state))

    def turn_off(self):
        del self.encoder
        del self.lcd
        del self.uv
        del self.light_sensor
        del self.th02

    def __str__(self):
        sensors_value = "====================\n"
        sensors_value += "Humidity: " + str(self.get_humidity_sensor_data()) + "% " + "\n"
        sensors_value += "Temperature: " + str(self.get_temp_sensor_data()) + "C " + "\n"
        sensors_value += "UV: " + str(self.get_uv_sensor_data()) + "\n"
        sensors_value += "Light: " + str(self.get_light_sensor_data()) + "\n"
        sensors_value += "===================="
        return sensors_value
