#!/usr/local/bin/python
import time
import RPi.GPIO as GPIO

def doReMi():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12, GPIO.OUT)
    p = GPIO.PWM(12, 50)
    p.start(50)

    p.ChangeFrequency(523)
    time.sleep(0.6)
    p.ChangeFrequency(523)
    time.sleep(0.6)
    p.ChangeFrequency(784)
    time.sleep(0.6)
    p.ChangeFrequency(784)
    time.sleep(0.6)
    p.ChangeFrequency(880)
    time.sleep(0.6)
    p.ChangeFrequency(880)
    time.sleep(0.6)
    p.ChangeFrequency(784)
    time.sleep(1)
    p.ChangeFrequency(698)
    time.sleep(0.6)
    p.ChangeFrequency(698)
    time.sleep(0.6)
    p.ChangeFrequency(659)
    time.sleep(0.6)
    p.ChangeFrequency(659)
    time.sleep(0.6)
    p.ChangeFrequency(587)
    time.sleep(0.6)
    p.ChangeFrequency(587)
    time.sleep(0.6)
    p.ChangeFrequency(523)
    time.sleep(0.6)
   
    p.stop()
    GPIO.cleanup()