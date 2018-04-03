import os
import demoscope3
from tkinter import *

master = Tk()
Nbuttons = 10

def buttonfunction(index):
	for i in range(Nbuttons):
		buttons[i].config(state="disabled")
	if index == 0:
		demoscope3.scope()
	elif index == 1:
		demoscope3.storedata(5)
	elif index == 2:
		demoscope3.plotsignal()
	elif index == 3:
		demoscope3.plotfourier()
	elif index == 4:
		demoscope3.plothistogram()
	elif index == 5:
		demoscope3.activar_envio()
	elif index == 6:
		demoscope3.alejar()
	elif index == 7:
		demoscope3.acercar()
	elif index == 8:
		demoscope3.move_noria(input('Obstaculo -> '))
	elif index == 9:
		os.system('clear')
		exit()
	for i in range(Nbuttons):
		buttons[i].config(state="active")
	

button_names = ['Plotear en tiempo real', 'Adquirir y almacenar', 'Graficar senal adquirida', 'Transformada de Fourier',
		'Histograma', 'Activar envio', 'Alejar', 'Acercar', 'Mover noria', 'Salir']

buttons = []

for index in range(Nbuttons): 
    n=button_names[index]

    button = Button(master, bg="White", text=n, relief=GROOVE,
                    command=lambda index=index, n=n: buttonfunction(index))

    # Add the button to the window
    button.grid(padx=2, pady=2, row=index, column=0)

    # Add a reference to the button to 'buttons'
    buttons.append(button)

mainloop()
