# coding=utf-8
"""
@author: Jan
@file: sketch.py
@time: 2018/7/11 11:22
"""
from flask import Flask, render_template,request,jsonify
from werkzeug.datastructures import CombinedMultiDict, MultiDict
import datetime

app = Flask(__name__)      

@app.route('/SmartNote/', methods=['GET','POST'])

def Hello():
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
    if request.method == 'POST': 
        now = datetime.datetime.now()
        now_c=now.strftime("%-I:%M%P")
        time_=request.form.get("time_get")
        print(time_)
        pirnt(now_c)
        # if time_== now_c
        #     print("time's up!")
    return render_template('SmartNote.html')
    
   
    
    


if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=5000)    # 執行我們的伺服器！
