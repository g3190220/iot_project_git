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



logging.basicConfig(level=logging.DEBUG)


logging.info("epd2in9 Demo")
epd = epd2in9.EPD()
logging.info("init and Clear")
epd.init(epd.lut_full_update)
epd.Clear(0xFF)
            
        
epd.init(epd.lut_partial_update)    
epd.Clear(0xFF)
   