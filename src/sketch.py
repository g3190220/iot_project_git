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

import doremi

epd = epd2in9.EPD()
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

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
        #state update
        logging.info("epd2in9 Demo")
        logging.info("init and Clear")
        epd.init(epd.lut_full_update)    
        epd.Clear(0xFF)
        state_image = Image.new('1', (epd.height, epd.width), 255)
        state_draw = ImageDraw.Draw(state_image)
        state_draw.text((10, 10), "HOW_ARE_YOU", font = font18, fill = 0)
        epd.display(epd.getbuffer(state_image))
    return render_template('SmartNote.html')
   

@app.route('/note_submit/', methods=['GET', 'POST'])
def note_submit(): 
    if request.method == 'POST': 
        result= request.form['note_text']
        print(result)
    return render_template('SmartNote.html')

@app.route('/control_led/', methods=['GET', 'POST'])  
def control_led():
    if request.method == 'POST':
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(12, GPIO.OUT)
        time_=request.form.get("time_get")
        flag=1
        print('You turn on your pi alarm!')
        while flag:
           now = datetime.datetime.now()
           now_c=now.strftime("%-I:%M%P")
           if time_== now_c:
                print("time's up!")
                flag=0
                doremi.doReMi()
                GPIO.cleanup()
                return render_template('SmartNote.html')         
        #print('It is %s'%(now_c))
        #print('our alarm is %s'%(time_))
        #return render_template('SmartNote.html')
           
if __name__ == '__main__':
    app.secret_key='12345'
    app.debug=True
    app.run(host='0.0.0.0',port=5000,threaded=True)    # 執行我們的伺服器！

