import RPi.GPIO as GPIO
import epd_2in9
import sys
import os
picdir = os.path.join(os.getcwd(), 'pic')
libdir = os.path.join(os.getcwd(), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
import logging
from waveshare_epd import epd2in9

from PIL import Image,ImageDraw,ImageFont
import traceback
import json
epd = epd2in9.EPD()

TouchPin = 27

def setup():
	GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
	
	GPIO.setup(TouchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	

def loop():
	while True:
		if GPIO.input(TouchPin) == GPIO.LOW:
			print("wait to touch...")
				
		else:
			print ('you touched!')
			epd_2in9.getDHTdata()
			epd_2in9.showtime()
			
			

def destroy():
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()