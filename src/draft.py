# coding=utf-8
"""
@author: Jan
@file: sketch.py
@time: 2018/7/11 11:22
"""
from flask import Flask, render_template,request

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

@app.route('/alarm_setTime/', methods=['GET', 'POST'])  
def alarm_setTime():
    if request.method =='POST':
        result1= request.form['on_off']
        result2= result.form['alarm_settime']
        return result1,result2


if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=5000)    # 執行我們的伺服器！