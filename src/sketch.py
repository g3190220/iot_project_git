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
@app.route('/Go_back/', methods=['GET','POST'])
def Go_back():
    print("go_back")
    return render_template('SmartNote.html') 
    print("i am sajl")
    
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
        #放插圖
        state_image = Image.new('1', (epd.height, epd.width), 255)
        state_draw = ImageDraw.Draw(state_image)
        bmp = Image.open(os.path.join(picdir, '666.bmp'))
        bmp.thumbnail( (62.94,89.76) )
        state_image.paste(bmp, (235,45))
        #畫直線
        state_draw.rectangle((10, 10, 100, 40), fill = 0)
        state_draw.text((15, 15), "My STATE", font = font18, fill = 255)
        #state_draw.line([(0, 12), (epd.width,12)],fill = 0, width = 3)
        state_draw.text((10, 50), result, font = font18, fill = 0)
        epd.display(epd.getbuffer(state_image))
    return render_template('SmartNote.html')
   

@app.route('/note_submit/', methods=['GET', 'POST'])
def note_submit(): 
    if request.method == 'POST': 
        result= request.form['note_text']
        #note update
        logging.info("epd2in9 Demo")
        logging.info("init and Clear")
        epd.init(epd.lut_full_update)    
        epd.Clear(0xFF)
        #放插圖
        note_image = Image.new('1', (epd.height, epd.width), 255)
        note_draw = ImageDraw.Draw(note_image)
        bmp = Image.open(os.path.join(picdir, '666.bmp'))
        bmp.thumbnail( (62.94,89.76) )
        state_image.paste(bmp, (235,45))
        #畫直線
        note_draw.rectangle((10, 10, 100, 40), fill = 0)
        note_draw.text((15, 15), "My NOTE", font = font18, fill = 255)
        #state_draw.line([(0, 12), (epd.width,12)],fill = 0, width = 3)
        note_draw.text((10, 50), result, font = font24, fill = 0)
        epd.display(epd.getbuffer(note_image))
    return render_template('SmartNote.html')

@app.route('/control_led/', methods=['GET', 'POST'])  
def control_led():
    if request.method == 'POST':
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(12, GPIO.OUT)
        time_=request.form.get("time_get")
        flag=1
        print('You turn on your pi alarm!')
        #alrm update
        logging.info("epd2in9 Demo")
        logging.info("init and Clear")
        epd.init(epd.lut_full_update)    
        epd.Clear(0xFF)
        #放插圖
        alarm_image = Image.new('1', (epd.height, epd.width), 255)
        alarm_draw = ImageDraw.Draw(alarm_image)
        bmp = Image.open(os.path.join(picdir, '2in13d.bmp'))
        bmp.thumbnail( (106,52) )
        alarm_image.paste(bmp, (180,90))
        #畫直線
        alarm_draw.text((15, 15),'You turn on your pi alarm!', font = font18, fill = 0)
        alarm_draw.line([(0, 12), (epd.width,12)],fill = 0, width = 3)
        epd.display(epd.getbuffer(alarm_image))
        while flag:
           now = datetime.datetime.now()
           now_c=now.strftime("%-I:%M%P")
           if time_== now_c:
                print("time's up!")
                wakeup_image = Image.new('1', (epd.height, epd.width), 255)
                wakeup_draw = ImageDraw.Draw(wakeup_image)
                wakeup_draw.text((15, 15),'Times up!!', font = font18, fill = 0)
                wakeup_draw.line([(0, 12), (epd.width,12)],fill = 0, width = 3)
                epd.display(epd.getbuffer(wakeup_image))
                flag=0
                doremi.doReMi()
                return render_template('SmartNote.html')         
        #print('It is %s'%(now_c))
        #print('our alarm is %s'%(time_))
        #return render_template('SmartNote.html')
           
if __name__ == '__main__':
    app.secret_key='12345'
    app.debug=True
    app.run(host='0.0.0.0',port=5000,threaded=True)    # 執行我們的伺服器！

