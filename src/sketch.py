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

app = Flask(__name__)      

@app.route('/SmartNote/', methods=['GET','POST'])

def Hello():
    return render_template('SmartNote.html')
@app.route('/Go_back/')
def Go_back():
    return render_template('SmartNote.html')

@app.route('/state_submit/', methods=['GET', 'POST'])

def state_submit(): 
    if request.method == 'POST': 
        result= request.form['state_text']
        print(result)
    return render_template('SmartNote.html')

@app.route('/note_submit/', methods=['GET', 'POST'])
def note_submit(): 
    if request.method == 'POST': 
        result= request.form['note_text']
        print(result)
    return render_template('SmartNote.html')

@app.route('/control_led/', methods=['GET', 'POST'])  
def control_led():
    # blinking function
    #def blink(pin):
        #GPIO.output(pin,GPIO.HIGH)
        #ime.sleep(1)
        #GPIO.output(pin,GPIO.LOW)
        #time.sleep(1)
        #return
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
                return render_template('SmartNote.html')         
        #print('It is %s'%(now_c))
        #print('our alarm is %s'%(time_))
        #return render_template('SmartNote.html')
           


if __name__ == '__main__':
    app.secret_key='12345'
    app.debug=True
    app.run(host='0.0.0.0',port=5000)    # 執行我們的伺服器！
