#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.getcwd(), 'pic')
libdir = os.path.join(os.getcwd(), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
import logging
from waveshare_epd import epd2in9
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import datetime
import json

import Adafruit_DHT
import RPi.GPIO as GPIO

font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

logging.basicConfig(level=logging.DEBUG)


logging.info("epd2in9 Demo")
epd = epd2in9.EPD()
logging.info("init and Clear")
epd.init(epd.lut_full_update)
epd.Clear(0xFF)

wakeup_image = Image.new('1', (epd.height, epd.width), 255)
wakeup_draw = ImageDraw.Draw(wakeup_image)
wakeup_draw.text((15, 15),'Times up!!', font = font18, fill = 0)
wakeup_draw.line([(0, 12), (epd.width,12)],fill = 0, width = 3)
epd.display(epd.getbuffer(wakeup_image))
            
    
   