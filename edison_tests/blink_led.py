__author__ = 'gaiar'

import mraa
import time

led = mraa.Gpio(3)

led.dir(mraa.DIR_OUT)

while True:

    try:
        # Blink the LED
        led.write(1)  # Send HIGH to switch on LED
        time.sleep(1)

        led.write(0)  # Send LOW to switch off LED
        time.sleep(1)

    except KeyboardInterrupt:  # Turn LED off before stopping
        led.write(0)
        break

    except IOError:  # Print "Error" if communication error encountered
        print
        "Error"
