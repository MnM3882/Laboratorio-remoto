import serial
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=262144,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

t = np.linspace(0, 10, 50)
y = np.zeros(50)
plt.ion()

ser.isOpen()

while 1:
	b = ser.read(size=2)
	b1i = b[0]
	b2i = b[1]

	par1 = b1i >> 7
	par2 = b2i >> 7

	d1 = (b1i & 0x40) >> 6
	d2 = (b1i & 0x20) >> 5
	
	bi = (((b1i & 0x1F) << 7) + (b2i & 0x7F))/4095

	os.system('clear')
	print('\nAnag1: '+"%.4f"%bi+' Dig1: '+str(d1)+' Dig2: '+str(d2)+' Par1: '+str(par1)+' Par2: '+str(par2))

	y = np.delete(y,0)
	y = np.append(y,bi)
	
	plt.clf()
	plt.axis([0, 10, 0, 1])
	plt.plot(t, y)
	plt.pause(0.00001)
	

ser.close()
exit()
