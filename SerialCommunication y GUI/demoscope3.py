import serial
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.fftpack
import pandas as pd

stopsignal = False

def stopevent(event):
	global stopsignal
	stopsignal = True

def scope():
	# configure the serial connections (the parameters differs on the device you are connecting to)
	ser = serial.Serial(
	    port='/dev/ttyUSB0',#'/dev/ttyACM0',
	    baudrate=115200,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS
	)
	global stopsignal
	try:
		if ser.isOpen():
			ser.close()	
		ser.open()
	except Exception:
		print("Error abriendo el puerto.")
		exit()

	if ser.isOpen():
		i = 0
		t = np.linspace(0, 0.5, 501)
		x = np.zeros(501)
		y = np.zeros(501)

		fig = plt.figure()
		ax = fig.add_subplot(1,1,1)
		ax.axis([0, 0.5, 0, 3])
		ax.set_title('Senales analogicas en tiempo real')
		lines1, = ax.plot(t, x, c='b', alpha = 0.7)
		lines2, = ax.plot(t, y, c='r', alpha = 0.7)
		ax.legend([lines1,lines2],['Canal 1','Canal 2'])
		
		#cid = lines1.figure.canvas.mpl_connect('button_press_event', stopevent)
		#cid = lines2.figure.canvas.mpl_connect('button_press_event', stopevent)
		cid = lines1.figure.canvas.mpl_connect('close_event', stopevent)
		cid = lines2.figure.canvas.mpl_connect('close_event', stopevent)
		
		
		
		plt.ion()
		plt.show()

		fig.canvas.draw()

		os.system('clear')
		ser.reset_input_buffer()
	
		while not stopsignal:
	
			b = ser.read(size=4)
		
		
			b1i = b[0]
			b2i = b[1]
			b3i = b[2]
			b4i = b[3]
			if b1i >= 128:
			
				d1 = (b1i & 0x20) >> 5
				d2 = (b3i & 0x20) >> 5

				bi = (((b1i & 0x1F) << 7) + (b2i & 0x7F)) *5/4095
				bj = (((b3i & 0x1F) << 7) + (b4i & 0x7F))#/819

				x = np.delete(x,0)
				x = np.append(x,bi)
	
				y = np.delete(y,0)
				y = np.append(y,bj)

				if (i == 0 or tt == True) and not stopsignal:
					tt = True
					if ser.in_waiting == 0:
						now = time.time()
					
						os.system('clear')
						print('Canal analogico 1: '+"%.4f"%bi+'\tCanal digital 1: '+str(d1)+'\n')
						print('Canal analogico 2: '+"%.4f"%bj+'\tCanal digital 2: '+str(d2))
		
						lines1.set_ydata(x)
						lines2.set_ydata(y)
						fig.canvas.draw()

						plt.pause(0.001)

						tt = False
	
				i = (i+1)%100
			
			else:
				print("Bad sync")
				ser.reset_input_buffer()

		ser.close()
		os.system('clear')
	plt.close()
	stopsignal = False

def storedata(adqtime):
	# configure the serial connections (the parameters differs on the device you are connecting to)
	ser = serial.Serial(
	    port='/dev/ttyUSB0',#'/dev/ttyACM0',
	    baudrate=115200,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS
	)
	global stopsignal
	try:
		if ser.isOpen():
			ser.close()	
		ser.open()
	except Exception:
		print("Error abriendo el puerto.")
		exit()

	if ser.isOpen():
		
		os.system('clear')
		ser.reset_input_buffer()

		security = 0;
		
		with open("anag1.csv", 'w') as fx, open("anag2.csv", 'w') as fy, open("dig1.csv", 'w') as fd1, open("dig2.csv", 'w') as fd2, open("error_report.txt", 'w') as fe:

			for i in range(1000*adqtime+4):
	
				b = ser.read(size=4)
		
				b1i = b[0]
				b2i = b[1]
				b3i = b[2]
				b4i = b[3]
				if b1i >= 128:
			
					d1 = (b1i & 0x20) >> 5
					d2 = (b3i & 0x20) >> 5

					bi = (((b1i & 0x1F) << 7) + (b2i & 0x7F)) *5/4095
					bj = (((b3i & 0x1F) << 7) + (b4i & 0x7F))#/819

					if(security<4):
						pass
					else:
						fx.write("%f\n"%bi)
						fy.write("%f\n"%bj)
						
						fd1.write("%d\n"%d1)
						fd2.write("%d\n"%d2)
			
				else:
					d1 = (b1i & 0x20) >> 5
					d2 = (b3i & 0x20) >> 5

					bi = (((b1i & 0x1F) << 7) + (b2i & 0x7F)) *5/4095
					bj = (((b3i & 0x1F) << 7) + (b4i & 0x7F))#/819

					fx.write("%f\n"%bi)
					fy.write("%f\n"%bj)
					
					#fd1.write("%d\n"%d1)
					#fd2.write("%d\n"%d2)

					fe.write("Error en la posicion %d"%i)
					ser.reset_input_buffer()

				security = security+1;

		ser.close()
		os.system('clear')

def plotsignal():
	t = np.linspace(0.0, 59.999, 60000) # np.linspace(0.0, 4.999, 5000)
	x = pd.read_csv('anag1.csv', header=None, squeeze = True).values
	y = pd.read_csv('anag2.csv', header=None, squeeze = True).values
	d1 = pd.read_csv('dig1.csv', header=None, squeeze = True).values
	d2 = pd.read_csv('dig2.csv', header=None, squeeze = True).values
	plt.plot(t, x, c='b', alpha = 0.7)
	plt.plot(t, y, c='r', alpha = 0.7)
	#plt.plot(t, d1, c='g', alpha = 0.5)
	#plt.plot(t, d2, c='y', alpha = 0.5)
	plt.ion()
	plt.show()
	os.system('clear')

def plotfourier():
	t = np.linspace(0.0, 59.999, 60000)
	x = pd.read_csv('anag1.csv', header=None, squeeze = True).values
	y = pd.read_csv('anag2.csv', header=None, squeeze = True).values
	xf = scipy.fftpack.fft(x)
	yf = scipy.fftpack.fft(y)
	f = np.linspace(0.0, 1.0/(2.0*59.999/60000), 60000/2)

	fig, ax = plt.subplots()
	ax.plot(f, 2.0/60000 * np.abs(xf[:60000//2]), c='b', alpha = 0.7)
	ax.plot(f, 2.0/60000 * np.abs(yf[:60000//2]), c='r', alpha = 0.7)
	plt.ion()
	plt.show()
	os.system('clear')

def plothistogram():
	x = pd.read_csv('anag1.csv', header=None, squeeze = True)
	y = pd.read_csv('anag2.csv', header=None, squeeze = True)
	d1 = pd.read_csv('dig1.csv', header=None, squeeze = True)
	d2 = pd.read_csv('dig2.csv', header=None, squeeze = True)
	x.plot.hist(color='b', alpha=0.7)
	y.plot.hist(color='r', alpha=0.7)
	#d1.plot.hist(color='g', alpha=0.5)
	#d2.plot.hist(color='y', alpha=0.5)
	plt.ion()
	plt.show()
	os.system('clear')
	print('Canal analogico 1:')
	print(x.describe())
	print('\nCanal analogico 2:')
	print(y.describe())

def activar_envio(dpar):
	dpar_dict = {'Galv+Sharp': b'\x02', 'Pasos+Sharp': b'\x22', 'Galv+Cnt': b'\x12'}
	# configure the serial connections (the parameters differs on the device you are connecting to)
	ser = serial.Serial(
	    port='/dev/ttyUSB0', #'/dev/ttyACM0',
	    baudrate=115200,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS
	)
	global stopsignal
	try:
		if ser.isOpen():
			ser.close()	
		ser.open()
	except Exception:
		print("Error abriendo el puerto.")
		exit()

	if ser.isOpen():
		
		ser.write(dpar_dict[dpar])
		
		ser.close()
		os.system('clear')


def alejar():
	# configure the serial connections (the parameters differs on the device you are connecting to)
	ser = serial.Serial(
	    port='/dev/ttyUSB0',#'/dev/ttyACM0',
	    baudrate=115200,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS
	)
	global stopsignal
	try:
		if ser.isOpen():
			ser.close()	
		ser.open()
	except Exception:
		print("Error abriendo el puerto.")
		exit()

	if ser.isOpen():
		
		ser.write(b'\x03')
		
		ser.close()
		os.system('clear')

def acercar():
	# configure the serial connections (the parameters differs on the device you are connecting to)
	ser = serial.Serial(
	    port='/dev/ttyUSB0',#'/dev/ttyACM0',
	    baudrate=115200,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS
	)
	global stopsignal
	try:
		if ser.isOpen():
			ser.close()	
		ser.open()
	except Exception:
		print("Error abriendo el puerto.")
		exit()

	if ser.isOpen():
		
		ser.write(b'\x13')
		
		ser.close()
		os.system('clear')

def move_Zahlrohr(distn):
	dist_array = [b'\x05',b'\x15',b'\x25',b'\x35',b'\x45',b'\x55',b'\x65',b'\x75',b'\x85',b'\x95',b'\xa5',b'\xb5',b'\xc5',b'\xd5',b'\xe5',b'\xf5']
	dist_dict = {'0': b'\x05', '1': b'\x15', '2': b'\x25', '3': b'\x35', '4': b'\x45', '5': b'\x55',
				 '6': b'\x65', '7': b'\x75', '8': b'\x85', '9': b'\x95', 'a': b'\xa5', 'b': b'\xb5',
				 'c': b'\xc5', 'd': b'\xd5', 'e': b'\xe5', 'f': b'\xf5'}
	#configure the serial connections (the parameters differs on the device you are connecting to)
	ser = serial.Serial(
	    port='/dev/ttyUSB0',#'/dev/ttyACM0',
	    baudrate=115200,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS
	)
	global stopsignal
	try:
		if ser.isOpen():
			ser.close()	
		ser.open()
	except Exception:
		print("Error abriendo el puerto.")
		exit()

	if ser.isOpen():
		
		ser.write(dist_dict[distn])
		
		ser.close()
		os.system('clear')

def move_Zahlrohr_sharp(distn):
	# dist_dict = {'0': b'\x03', '1': b'\x13', '2': b'\x23', '3': b'\x33', '4': b'\x43', '5': b'\x53',
	# 			 '6': b'\x63', '7': b'\x73', '8': b'\x83', '9': b'\x93', 'a': b'\xa3', 'b': b'\xb3',
	# 			 'c': b'\xc3', 'd': b'\xd3', 'e': b'\xe3', 'f': b'\xf3'}
	#dist_dict = {'8.3': b'\x03', '10'  : b'\x13', '11.7': b'\x23', '13.4': b'\x33', '15.1': b'\x43', '16.8': b'\x53',
	#			 '18.5': b'\x63', '20.2': b'\x73', '21.9': b'\x83', '23.6': b'\x93', '25.3': b'\xa3', '27'  : b'\xb3',
	#			 '28.7': b'\xc3', '30.4': b'\xd3', '32.1': b'\xe3', '33.8': b'\xf3'}

	dist_dict = {'8.3': b'\x05', '10'  : b'\x15', '11.7': b'\x25', '13.4': b'\x35', '15.1': b'\x45', '16.8': b'\x55',
				 '18.5': b'\x65', '20.2': b'\x75', '21.9': b'\x85', '23.6': b'\x95', '25.3': b'\xa5', '27'  : b'\xb5',
				 '28.7': b'\xc5', '30.4': b'\xd5', '32.1': b'\xe5', '33.8': b'\xf5'}	
	# configure the serial connections (the parameters differs on the device you are connecting to)
	ser = serial.Serial(
	    port='/dev/ttyUSB0',#'/dev/ttyACM0',
	    baudrate=115200,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS
	)
	global stopsignal
	try:
		if ser.isOpen():
			ser.close()	
		ser.open()
	except Exception:
		print("Error abriendo el puerto.")
		exit()

	if ser.isOpen():
		
		ser.write(dist_dict[distn])
		
		ser.close()
		os.system('clear')

def move_noria(obsid):
	#obsid_dict = {'0': b'\x04', '1': b'\x14', '2': b'\x24', '3': b'\x34', '4': b'\x44', '5': b'\x54',
	#		 '6': b'\x64', '7': b'\x74', '8': b'\x84', '9': b'\x94', 'a': b'\xa4', 'b': b'\xb4',
	#		 'c': b'\xc4', 'd': b'\xd4', 'e': b'\xe4', 'f': b'\xf4'}
	obsid_arr = [b'\x04',b'\x14',b'\x24',b'\x34',b'\x44',b'\x54',b'\x64',b'\x74']
	# configure the serial connections (the parameters differs on the device you are connecting to)
	ser = serial.Serial(
	    port='/dev/ttyUSB0',#'/dev/ttyACM0',
	    baudrate=115200,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS
	)
	global stopsignal
	try:
		if ser.isOpen():
			ser.close()	
		ser.open()
	except Exception:
		print("Error abriendo el puerto.")
		exit()

	if ser.isOpen():
		
		ser.write(obsid_arr[obsid])
		
		ser.close()
		os.system('clear')
