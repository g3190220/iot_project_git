#!/usr/local/bin/python
import time
import RPi.GPIO as GPIO

def doReMi():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(32, GPIO.OUT)
    p = GPIO.PWM(32, 50)
    p.start(50)

    p.ChangeFrequency(523)
    time.sleep(0.5)
    p.ChangeFrequency(523)
    time.sleep(0.5)
    p.ChangeFrequency(659)
    time.sleep(0.5)
    p.ChangeFrequency(659)
    time.sleep(0.5)
    p.ChangeFrequency(880)
    time.sleep(0.5)
    p.ChangeFrequency(880)
    time.sleep(0.5)
    p.ChangeFrequency(659)
    time.sleep(1)
    p.ChangeFrequency(784)
    time.sleep(0.5)
    p.ChangeFrequency(784)
    time.sleep(0.5)
    p.ChangeFrequency(659)
    time.sleep(0.5)
    p.ChangeFrequency(659)
    time.sleep(0.5)
    p.ChangeFrequency(587)
    time.sleep(0.5)
    p.ChangeFrequency(587)
    time.sleep(0.5)
    p.ChangeFrequency(523)
    time.sleep(0.5)
   
    p.stop()
    GPIO.cleanup()

doReMi()