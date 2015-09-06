# pot_touch_led_lcd.py

import pyupm_i2clcd as lcd
import mraa
import time
import sys
import math

# analog input - pot
# Adding Potentiometer
potPin = 0
pot = mraa.Aio(potPin)
potVal = 0
potGrnVal = 0
potBluVal = 0

# Adding light sensor
lightPin = 1
lum = mraa.Aio(lightPin)
lumVal = 0

# Adding temperature sensor
tempPin = 2
temp = mraa.Aio(tempPin)
tempVal = 0


# Adding LED
ledPin = mraa.Gpio(4)
ledPin.dir(mraa.DIR_OUT)
ledPin.write(0)

# Adding buzzer
buzPin = mraa.Gpio(8)
buzPin.dir(mraa.DIR_OUT)
buzPin.write(0)

# Adding button
touchPin = mraa.Gpio(3)
touchPin.dir(mraa.DIR_IN)

# Adding LCD
lcdDisplay = lcd.Jhd1313m1(0, 0x3E, 0x62)
while True:
    while touchPin.read() == 1:
        # turn led on
        ledPin.write(1)
        time.sleep(3)
        # wait 3 second to get pot value
        # turn buzzer on
        #buzPin.write(1)
        time.sleep(1)
        buzPin.write(0)

        # read pot/print/convert to string/display on lcd
        potVal = int(pot.read() * .249)
        lumVal = float(lum.read())
        tmp1Val = float(temp.read())
        '''
        const int B=4275;                 // B value of the thermistor
        const int R0 = 100000;            // R0 = 100k
        float R = 1023.0/((float)a)-1.0;
        R = 100000.0*R;
        flot temperature=1.0/(log(R/100000.0)/B+1/298.15)-273.15;//convert to temperature via datasheet ;
        '''
        bVal = 4275
        # resistanceVal = (1023 - tmp1Val) * 10000 / tmp1Val

        resistanceVal = float(1023.0 / (tmp1Val) - 1.0) * 100000.0
        celsiusVal = 1 / (math.log(resistanceVal / 10000) / bVal + 1 / 298.15) - 273.15
        # fahrVal = (celsiusVal * (9 / 5)) + 32
        tempVal = celsiusVal

        print "Pot: " + str(potVal) + " Lumens: " + str(lumVal) + " Temp: " + str(tempVal)

        potStr = "P:" + str(potVal) + "L:" + str(lumVal)
        lcdDisplay.setCursor(0, 0)
        lcdDisplay.setColor(potVal, 0, 0)
        lcdDisplay.write(potStr)

        lumStr = "Temp: " + str(tempVal)
        lcdDisplay.setCursor(1, 0)
        lcdDisplay.write(lumStr)

        time.sleep(3)
        potgrnVal = int(pot.read() * .249)
        # Print "Green: " + str(potgrnVal)
        lcdDisplay.setColor(potVal, potgrnVal, 0)
        time.sleep(3)
        potbluVal = int(pot.read() * .249)
        # Print "Blue: " + str(potbluVal)
        lcdDisplay.setColor(potVal, potgrnVal, potbluVal)


        # turn led off
    ledPin.write(0)

    # turn buzzer off
    buzPin.write(0)
