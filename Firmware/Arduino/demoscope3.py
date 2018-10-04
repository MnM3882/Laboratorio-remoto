# A windows no le gusta clear
import serial
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.fftpack
import pandas as pd

stopsignal = False

# Funcion necesaria para detener las graficas en tiempo real
def stopevent(event):
	global stopsignal
	stopsignal = True

# Funcion para graficar las senales en tiempo real
def scope():
    
	# Configurar parametros de la comunicacion serial
	ser = serial.Serial(
	    port='COM4',#'/dev/ttyUSB0',#'/dev/ttyACM0',
	    baudrate=115200,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS
	)
	global stopsignal
    
    # Intentar abrir el puerto serial
	try:
		if ser.isOpen():
			ser.close()	
		ser.open()
	except Exception:
		print("Error abriendo el puerto.")
		exit()
        
    # Si se logra abrir, proceder a graficar en tiempo real
	if ser.isOpen():
        
        # Configurando el canvas y variables necesarias
        # Arreglos de los datos
		i = 0
		t = np.linspace(0, 0.5, 501)
		x = np.zeros(501)
		y = np.zeros(501)

        # Creando la figura
		fig = plt.figure()
		ax = fig.add_subplot(1,1,1)
		ax.axis([0, 0.5, 0, 5])
		ax.set_title('Senales en tiempo real')
		lines1, = ax.plot(t, x, c='b', alpha = 0.7)
		lines2, = ax.plot(t, y, c='r', alpha = 0.7)
		ax.legend([lines1,lines2],['Voltaje en el galvanometro','Fotones detectados'])
		
        # Eventos para detener el proceso cuando se cierre la ventana
		cid = lines1.figure.canvas.mpl_connect('close_event', stopevent)
		cid = lines2.figure.canvas.mpl_connect('close_event', stopevent)
		
        # Plot interactivo
		plt.ion()
		plt.show()

		fig.canvas.draw()

        # Limpiar el buffer de recepcion y la consola
		# os.system('clear')
		ser.reset_input_buffer()
	
        # Mientras la ventana de la figura este abierta
		while not stopsignal:
	
            # Leer 4 bytes del buffer
			b = ser.read(size=4)
		
            # Separarlos y convertirlos en enteros
			b1i = b[0]
			b2i = b[1]
			b3i = b[2]
			b4i = b[3]
            
            # Si el bit mas significativo del primer byte es 1
            # La trama esta sincronizada y los datos se procesaran correctamente
			if b1i >= 128:
			
                # Procesar la trama recibida
				d1 = (b1i & 0x20) >> 5
				d2 = (b3i & 0x20) >> 5

				bi = (((b1i & 0x1F) << 7) + (b2i & 0x7F)) *5/1023
				bj = (((b3i & 0x1F) << 7) + (b4i & 0x7F))#/819

                # Actualizar arreglos
				x = np.delete(x,0)
				x = np.append(x,bi)
	
				y = np.delete(y,0)
				y = np.append(y,bj)

                # Si han pasado al menos 100 ciclos y el buffer esta vacio
                # actualizar los graficos y la consola
				if (i == 0 or tt == True) and not stopsignal:
					tt = True
					if ser.in_waiting == 0:
						now = time.time()
					
						# os.system('clear')
						print('Canal analogico 1: '+"%.4f"%bi+'\tCanal digital 1: '+str(d1)+'\n')
						print('Canal analogico 2: '+"%.4f"%bj+'\tCanal digital 2: '+str(d2))
		
						lines1.set_ydata(x)
						lines2.set_ydata(y)
						fig.canvas.draw()

						plt.pause(0.001)

						tt = False
	
				i = (i+1)%100
			
            # Si la trama no esta sincronizada, limpiar el buffer y volver a intentar
			else:
				print("Bad sync")
				ser.reset_input_buffer()

        # Si se cierra la ventana, cerrar el puerto y limpiar la consola
		ser.close()
		# os.system('clear')
	plt.close()
	stopsignal = False

# Funcion para adquirir y almacenar los datos
def storedata(adqtime):
    
	# Configurar parametros de la comunicacion serial
	ser = serial.Serial(
	    port='COM4',#'/dev/ttyUSB0',#'/dev/ttyACM0',
	    baudrate=115200,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS
	)
	global stopsignal
    
    # Intentar abrir el puerto serial
	try:
		if ser.isOpen():
			ser.close()	
		ser.open()
	except Exception:
		print("Error abriendo el puerto.")
		exit()

    # Si se logra abrir, proceder a graficar en tiempo real
	if ser.isOpen():
		
        # Limpiar el buffer de recepcion y la consola
		# os.system('clear')
		ser.reset_input_buffer()

        # Variable auxiliar para descartar los datos erroneos
        # por mala sincronizacion al inicio de la adquisicion
		security = 0;
		
        # Crear los archivos en los que se almacenaran los datos
		with open("anag1.csv", 'w') as fx, open("anag2.csv", 'w') as fy, open("dig1.csv", 'w') as fd1, open("dig2.csv", 'w') as fd2, open("error_report.txt", 'w') as fe:

            # Adquirir la cantidad de muestras especificada
			for i in range(1000*adqtime+4):
	
                # Leer 4 bytes
				b = ser.read(size=4)
		
                # Separar los bytes y convertirlos a enteros
				b1i = b[0]
				b2i = b[1]
				b3i = b[2]
				b4i = b[3]
                
                # Si el bit mas significativo del primer byte es 1
                # La trama esta sincronizada y los datos se procesaran correctamente
				if b1i >= 128:
			
					d1 = (b1i & 0x20) >> 5
					d2 = (b3i & 0x20) >> 5

					bi = (((b1i & 0x1F) << 7) + (b2i & 0x7F)) *5/1023
					bj = (((b3i & 0x1F) << 7) + (b4i & 0x7F))#/819

					# Ignorar las cuatro primeras adquisiciones
					# Para garantizar que la trama este sincronizada
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

					bi = (((b1i & 0x1F) << 7) + (b2i & 0x7F)) *5/1023
					bj = (((b3i & 0x1F) << 7) + (b4i & 0x7F))#/819
                    
					if(security<4):
						pass
					else:
						fx.write("%f\n"%bi)
						fy.write("%f\n"%bj)
					
						fd1.write("%d\n"%d1)
						fd2.write("%d\n"%d2)

						fe.write("Error en la posicion %d"%i)
						ser.reset_input_buffer()

				security = security+1;

		# Cerrar el puerto al finalizar la adquisicion
		ser.close()
		# os.system('clear')

# Graficar los datos adquiridos
def plotsignal():
	t = np.linspace(0.0, 299.999, 300000) # np.linspace(0.0, 4.999, 5000)
	x = pd.read_csv('anag1.csv', header=None, squeeze = True).values
	y = pd.read_csv('anag2.csv', header=None, squeeze = True).values
	d1 = pd.read_csv('dig1.csv', header=None, squeeze = True).values
	d2 = pd.read_csv('dig2.csv', header=None, squeeze = True).values
	plt.plot(t, x, c='b', alpha = 0.7)
	plt.plot(t, y, c='r', alpha = 0.7)
	plt.plot(t, d1, c='g', alpha = 0.5)
	plt.plot(t, d2, c='y', alpha = 0.5)
	plt.ion()
	plt.show()
	# os.system('clear')

# Graficar la trasformada de Fourier de las senales adquiridas
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
	# os.system('clear')

# Graficar histograma de las senales adquiridas
def plothistogram():
	x = pd.read_csv('anag1.csv', header=None, squeeze = True)
	y = pd.read_csv('anag2.csv', header=None, squeeze = True)
	d1 = pd.read_csv('dig1.csv', header=None, squeeze = True)
	d2 = pd.read_csv('dig2.csv', header=None, squeeze = True)
	x.plot.hist(color='b', alpha=0.7)
	y.plot.hist(color='r', alpha=0.7)
	d1.plot.hist(color='g', alpha=0.5)
	d2.plot.hist(color='y', alpha=0.5)
	plt.ion()
	plt.show()
	# os.system('clear')
	print('Canal analogico 1:')
	print(x.describe())
	print('\nCanal analogico 2:')
	print(y.describe())

# Activar algun modo de envio
def activar_envio(dpar):
	dpar_dict = {'Galv+Sharp': b'\x02', 'Pasos+Sharp': b'\x22', 'Galv+Cnt': b'\x12'}
	
	# Configurar parametros de la comunicacion serial
	ser = serial.Serial(
	    port='COM4',#'/dev/ttyUSB0', #'/dev/ttyACM0',
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
		
        # Enviar orden al microcontrolador
		ser.write(dpar_dict[dpar])
		
		ser.close()
		# os.system('clear')


# Alejar el contador Geiger
# (Funcion despreciada)
def alejar():
	# Configurar parametros de la comunicacion serial
	ser = serial.Serial(
	    port='COM4',#'/dev/ttyUSB0',#'/dev/ttyACM0',
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
		
        # Enviar orden al microcontrolador
		ser.write(b'\x03')
		
		ser.close()
		# os.system('clear')

# Acercar el contador Geiger
# (Funcion despreciada)
def acercar():
	# Configurar parametros de la comunicacion serial
	ser = serial.Serial(
	    port='COM4',#'/dev/ttyUSB0',#'/dev/ttyACM0',
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
		
        # Enviar orden al microcontrolador
		ser.write(b'\x13')
		
		ser.close()
		# os.system('clear')

# Mover el contador Geiger a la posicion indicada
# (Contando los pasos)
def move_Zahlrohr(distn):
    
    # Diccionario de codigos de cada posicion
	dist_dict = {'8.3': b'\x05', '10'  : b'\x15', '11.7': b'\x25', '13.4': b'\x35', '15.1': b'\x45', '16.8': b'\x55',
				 '18.5': b'\x65', '20.2': b'\x75', '21.9': b'\x85', '23.6': b'\x95', '25.3': b'\xa5', '27'  : b'\xb5',
				 '28.7': b'\xc5', '30.4': b'\xd5', '32.1': b'\xe5', '33.8': b'\xf5'}	
	
	# Configurar parametros de la comunicacion serial
	ser = serial.Serial(
	    port='COM4',#'/dev/ttyUSB0',#'/dev/ttyACM0',
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
		
        # Enviar orden al microcontrolador
		ser.write(dist_dict[distn])
		
		ser.close()
		# os.system('clear')
        
# Mover el contador Geiger a la posicion indicada
# (En funcion de la senal del sensor infrarojo)
def move_Zahlrohr_sharp(distn):

    # Diccionario de codigos de cada posicion
	dist_dict = {'8.3': b'\x03', '10'  : b'\x13', '11.7': b'\x23', '13.4': b'\x33', '15.1': b'\x43', '16.8': b'\x53',
				 '18.5': b'\x63', '20.2': b'\x73', '21.9': b'\x83', '23.6': b'\x93', '25.3': b'\xa3', '27'  : b'\xb3',
				 '28.7': b'\xc3', '30.4': b'\xd3', '32.1': b'\xe3', '33.8': b'\xf3'}	
	
	# Configurar parametros de la comunicacion serial
	ser = serial.Serial(
	    port='COM4',#'/dev/ttyUSB0',#'/dev/ttyACM0',
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
		
        # Enviar orden al microcontrolador
		ser.write(dist_dict[distn])
		
		ser.close()
		# os.system('clear')

# Mover la noria y ubicar el obstaculo indicado
def move_noria(obsid):
    # Lista de codigos de cada obstaculo
	obsid_arr = [b'\x04',b'\x14',b'\x24',b'\x34',b'\x44',b'\x54',b'\x64',b'\x74']
	
	# Configurar parametros de la comunicacion serial
	ser = serial.Serial(
	    port='COM4',#'/dev/ttyUSB0',#'/dev/ttyACM0',
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
		
        # Enviar orden al microcontrolador
		ser.write(obsid_arr[obsid])
		
		ser.close()
		# os.system('clear')
