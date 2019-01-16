#!/usr/bin/env python3

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

def main():
	i2c = busio.I2C(board.SCL, board.SDA)

	# wir verwenden den 1115
	ads = ADS.ADS1115(i2c)

	# Channel 0 und 1 auslesen
	chan_0 = AnalogIn(ads, ADS.P0)
	chan_1 = AnalogIn(ads, ADS.P1)

	# Differentialmodus erlaubt Messung von Spannungsdifferenz
	#chan = AnalogIn(ads, ADS.P0, ADS.P1)

	print("{:>5}\t{:>5}\t{:>5}\t{:>5}".format('raw0', 'v0', 'raw1', 'v1'))

	while True:
		print("{:>5}\t{:>5.3f}\t{:>5}\t{:>5.3f}"
			.format(chan_0.value, chan_0.voltage, chan_1.value, chan_1.voltage))
		time.sleep(0.5)
	
if __name__ == '__main__':
	main()
