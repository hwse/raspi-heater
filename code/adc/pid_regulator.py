#!/usr/bin/env python3

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import RPi.GPIO as GPIO
import pid

TARGET_TEMPERATURE = 40
HEATER_PIN = 5

def regulate(power):
    # 0 < power < 100  
    on_time = power / 100.0
    off_time = 1.0 - on_time
    GPIO.output(HEATER_PIN, GPIO.HIGH)
    time.sleep(on_time)
    GPIO.output(HEATER_PIN, GPIO.LOW)
    time.sleep(off_time)

def main():
    i2c = busio.I2C(board.SCL, board.SDA)

    # wir verwenden den 1115
    ads = ADS.ADS1115(i2c)
    # Channel 0 auslesen
    chan_0 = AnalogIn(ads, ADS.P0)

    # GPIO.setmode(GPIO.BOARD)
    GPIO.setup(HEATER_PIN, GPIO.OUT)

    pid_regulator = pid.PID(1.5,0.2,0.6)
    pid_regulator.setPoint(TARGET_TEMPERATURE)

    print("{:>5}\t{:>5}\t{:>5}\t{}".format('raw0', 'v0', 'temp', 'pid'))

    while True:
        heater_voltage = chan_0.voltage
        temperature = (heater_voltage - 1.25) / 0.05
        
        pid_value = pid_regulator.update(temperature)
        pid_value = min(100, max(0, pid_value))
        
        print("{:>5}\t{:>5.3f}\t{:>5.3f}\t{:>5.3f}"
            .format(chan_0.value, heater_voltage, temperature, pid_value))
        regulate(pid_value)

if __name__ == '__main__':
	main()
