import time, sys, signal, atexit
import pyupm_rotaryencoder as upmRotaryEncoder

# Instantiate a Grove Rotary Encoder, using signal pins D2 and D3
myRotaryEncoder = upmRotaryEncoder.RotaryEncoder(2, 3);


## Exit handlers ##
# This function stops python from printing a stacktrace when you hit control-C
def SIGINTHandler(signum, frame):
	raise SystemExit

# This function lets you run code on exit, including functions from myRotaryEncoder
def exitHandler():
	print "Exiting"
	sys.exit(0)

# Register exit handlers
atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)


# Read the value every second and detect motion
while(1):
	print "Position: {0}".format(myRotaryEncoder.position())
	time.sleep(.1)