import RPi.GPIO as GPIO

TouchPin = 27

def setup():
	GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
	
	GPIO.setup(TouchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	

def loop():
	while True:
		if GPIO.input(TouchPin) == GPIO.LOW:
			print ('you touch')
			
		else:
			print ('no')
			

def destroy():
	GPIO.cleanup()                     # Release resource

if _name_ == '_main_':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()