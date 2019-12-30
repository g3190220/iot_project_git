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

# get data from DHT sensor
def getDHTdata():
    DHT22Sensor = Adafruit_DHT.DHT22
    DHTpin = 4
    hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
    if hum is not None and temp is not None:
        hum = round(hum)
        temp = round(temp, 1)
    return temp, hum

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in9 Demo")
    epd = epd2in9.EPD()
    logging.info("init and Clear")
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)
            
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

        
    epd.init(epd.lut_partial_update)    
    epd.Clear(0xFF)
    # 24h update 
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    #paste thermometer image
    logging.info("4.read bmp file on window")
    bmp = Image.open(os.path.join(picdir, '2in13d.bmp'))
    bmp.thumbnail( (106,52) )
    time_image.paste(bmp, (142,90))
    #date,week,time
    time_now = datetime.datetime.now()
    date_string = time_now.strftime('%Y-%m-%d')
    week_string = [u'MONDAY',u'TUESDAY',u'WEDNESDAY',u'THUESDAY',u'FRIDAY',u'SATURDAY',u'SUNDAY'][time_now.isoweekday() - 1]
    time_draw.text((10, 70), date_string, font = font18, fill = 0)
    time_draw.text((10, 95), week_string, font = font18, fill = 0)
    #畫直線
    time_draw.line([(135, 0), (135,epd.height)],
    fill = 0, width = 3)
    while(True):
        #溫溼度計
        temp, hum = getDHTdata()
        temp_val=str(temp)
        hum_val=str(hum)

        time_draw.rectangle((200, 200, 225, 20), fill = 0)
        time_draw.text((144, 19), "Temp: "+temp_val+" °C", font = font18, fill = 0)
        newimage_1 = time_image.crop([200, 200, 225, 20])
        time_image.paste(newimage_1, (144, 19))  

        time_draw.rectangle((200, 200, 225, 20), fill = 0)
        time_draw.text((144, 55), "Hum: "+hum_val+" %", font = font18, fill = 0)
        newimage_2 = time_image.crop([200, 200, 225, 20])
        time_image.paste(newimage_2, (144, 55))  
        num=0
        # partial update
        logging.info("5.show time")
        while (num<20):
            time_draw.rectangle((10, 10, 120, 50), fill = 0)
            time_draw.text((10, 15), time.strftime('%H:%M:%S'), font = font24, fill = 255)
            newimage_3 = time_image.crop([10, 10, 120, 50])
            time_image.paste(newimage_3, (10,15))  
            epd.display(epd.getbuffer(time_image))
            num=num+1
                    
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