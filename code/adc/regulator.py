#!/usr/bin/env python3

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import RPi.GPIO as GPIO

TARGET_TEMPERATURE = 40
HEATER_PIN = 5

def main():
    i2c = busio.I2C(board.SCL, board.SDA)

    # wir verwenden den 1115
    ads = ADS.ADS1115(i2c)
    # Channel 0 auslesen
    chan_0 = AnalogIn(ads, ADS.P0)

    # GPIO.setmode(GPIO.BOARD)
    GPIO.setup(HEATER_PIN, GPIO.OUT)

    print("{:>5}\t{:>5}\t{:>5}\t{}".format('raw0', 'v0', 'temp', 'on'))

    while True:
        heater_voltage = chan_0.voltage
        temperature = (heater_voltage - 1.25) / 0.05
        heater_on = temperature < TARGET_TEMPERATURE 
        GPIO.output(HEATER_PIN, GPIO.HIGH if heater_on else GPIO.LOW)

        print("{:>5}\t{:>5.3f}\t{:>5.3f}\t{}"
            .format(chan_0.value, heater_voltage, temperature, heater_on))
        time.sleep(0.5)

if __name__ == '__main__':
	main()
