# coding=utf-8
"""
@author: Jan
@file: sketch.py
@time: 2018/7/11 11:22
"""
from flask import Flask,flash, render_template,request,jsonify
from werkzeug.datastructures import CombinedMultiDict, MultiDict
import datetime
import RPi.GPIO as GPIO
import time
import Adafruit_DHT

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


app = Flask(__name__)      

@app.route('/SmartNote/', methods=['GET','POST'])

def Hello():
    return render_template('SmartNote.html')
@app.route('/Go_back/')
def Go_back():
    return render_template('SmartNote.html')
# get data from DHT sensor
def getDHTdata():
    DHT22Sensor = Adafruit_DHT.DHT22
    DHTpin = 4
    hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
    if hum is not None and temp is not None:
        hum = round(hum)
        temp = round(temp, 1)
    return temp, hum
@app.route('/t_h_data/')
def t_h_submit():
    timeNow = time.asctime( time.localtime(time.time()) )
    temp, hum = getDHTdata()
    templateData = {
        'time': timeNow,
        'temp': temp,
        'hum' : hum
    }
    return render_template('SmartNote.html',**templateData)

@app.route('/state_submit/', methods=['GET', 'POST'])

def state_submit(): 
    if request.method == 'POST': 
        result= request.form['state_text']
        
    return render_template('SmartNote.html')
    logging.info("init and Clear")
    epd.init(epd.lut_full_update)   
    epd.Clear(0xFF)
    # state update 
    state_image = Image.new('1', (epd.height, epd.width), 255)
    state_draw = ImageDraw.Draw(state_image)
    state_draw.text((10, 10), result, font = font18, fill = 0)

@app.route('/note_submit/', methods=['GET', 'POST'])
def note_submit(): 
    if request.method == 'POST': 
        result= request.form['note_text']
        print(result)
    return render_template('SmartNote.html')

@app.route('/control_led/', methods=['GET', 'POST'])  
def control_led():
    # blinking function
    def blink(pin):
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(1)
        return
    GPIO.setmode(GPIO.BCM)
    if request.method == 'POST':
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(12, GPIO.OUT)
        time_=request.form.get("time_get")
        flag=1
        print('You turn on your pi alarm!')
        GPIO.setup(18, GPIO.OUT)
        while flag:
           now = datetime.datetime.now()
           now_c=now.strftime("%-I:%M%P")
           if time_== now_c:
                print("time's up!")
                flag=0
                for i in range(0,5):
                    blink(18)
                GPIO.cleanup()
                return render_template('SmartNote.html')         
        #print('It is %s'%(now_c))
        #print('our alarm is %s'%(time_))
        #return render_template('SmartNote.html')
           
if __name__ == '__main__':
    app.secret_key='12345'
    app.debug=True
    app.run(host='0.0.0.0',port=5000,threaded=True)    # 執行我們的伺服器！


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
    time_draw.line([(138, 0), (138,epd.height)],
    fill = 0, width = 3)
    #溫溼度計
    #temp, hum = getDHTdata()
    time_draw.text((144, 19), "Temp: 25.8°C", font = font18, fill = 0)
    time_draw.text((144, 55), "Hum: 65.8%", font = font18, fill = 0)
    num=0
    # partial update
    logging.info("5.show time")
    while (True):
        time_draw.rectangle((10, 10, 120, 50), fill = 0)
        time_draw.text((10, 15), time.strftime('%H:%M:%S'), font = font24, fill = 255)
        newimage = time_image.crop([10, 10, 120, 50])
        time_image.paste(newimage, (10,15))  
        epd.display(epd.getbuffer(time_image))
        num = num + 1
        if(num == 60):
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

