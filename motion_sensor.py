import time, sys, signal, atexit
import pyupm_biss0001 as upmMotion
import pyupm_grove as grove
import pyupm_buzzer as upmBuzzer
import pyupm_grove as grove
import mraa

# Instantiate a Grove Motion sensor on GPIO pin D7
myMotion = upmMotion.BISS0001(7)

# Create the Grove LED object using GPIO pin 3
led = grove.GroveLed(3)

# Create the buzzer object using GPIO pin 6
buzzer2 = upmBuzzer.Buzzer(6)

button = grove.GroveButton(8)



#buzzer = mraa.Gpio(8)
#buzzer.dir(mraa.DIR_OUT)


# Print the name
print(led.name())
print(buzzer2.name())


## Exit handlers ##
# This function stops python from printing a stacktrace when you hit control-C
def SIGINTHandler(signum, frame):
    raise SystemExit


# This function lets you run code on exit, including functions from myMotion
def exitHandler():
    print("Exiting")
    sys.exit(0)


# Register exit handlers
atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)


# Read the value every second and detect motion
while (1):
    print ('Button value: '+str(button.value()))

    if (myMotion.value()):
        print("Detecting moving object")
        led.on()
        #buzzer2.playSound(upmBuzzer.SI, 1000000)
        #buzzer2.stopSound()
        #buzzer.write(1)

    else:
        print("No moving objects detected")
        led.off()
        buzzer2.stopSound()
    time.sleep(1)
