#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
import logging
from waveshare_epd import epd2in9
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import datetime
import json



logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in9 Demo")
    
    epd = epd2in9.EPD()
    logging.info("init and Clear")
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)
    
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    

   
    #paste thermometer image
    logging.info("4.read bmp file on window")
    bmp = Image.open(os.path.join(picdir, 'thermometer.bmp'))
    bmp.thumbnail( (64,64) )
    time_image.paste(bmp, (140,0))
    # 24h update 
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    time_now = datetime.datetime.now()
    date_string = time_now.strftime('%Y-%m-%d')
    week_string = [u'MON',u'TUE',u'WED',u'THU',u'FRI',u'SAT',u'SUN'][time_now.isoweekday() - 1]
    time_draw.text((10, 50), date_string, font = font24, fill = 0)
    time_draw.text((10, 90), week_string, font = font24, fill = 0)

# partial update
    logging.info("5.show time")
    while (True):
        time_draw.rectangle((10, 10, 120, 50), fill = 255)
        time_draw.text((10, 10), time.strftime('%H:%M:%S'), font = font24, fill = 0)
        newimage = time_image.crop([10, 10, 120, 50])
        time_image.paste(newimage, (10,10))  
        #開始顯示
        epd.display(epd.getbuffer(time_image))
        
        num = num + 1
        if(num == 10):
            break
            
    logging.info("Clear...")
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in9.epdconfig.module_exit()
    exit()

