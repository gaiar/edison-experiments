__author__ = 'gaiar'

import mraa

led = mraa.Gpio(13)

led.dir(mraa.DIR_OUT)

while True:
    led.write(1)
    led.write(0)
