import os
import demoscope3
from tkinter import *
from tkinter import ttk, Canvas

master = Tk()
master.title("Laboratorio remoto- LFN USB")
master.geometry('1000x1000')

top_frame = Frame(master, bg='white', width = 1000, height=300, padx=10, pady=10)
top_frame.pack(side= TOP, fill=X)
lbl = Label(top_frame, text="Laboratorio remoto - Espectrometría gamma", font=("Times New Roman", 20),bg='white')
lbl.pack(side=TOP, padx=10, pady=10)
left_frame = Frame(master, bg='white', width = 250,padx=10, pady=10)
left_frame.pack(side= LEFT, fill=Y)
right_frame = Frame(master, bg='white', width = 250,padx=10, pady=10)
right_frame.pack(side= RIGHT, fill=Y)
center_frame=Frame(master, bg='white', width=500, height=1000)
center_frame.pack(side=TOP, fill=X)

#Para probar que los indices de los obstáculos sean los correctos
def cambiar_obstaculo():
    demoscope3.move_noria(obstaculo.get())
def def_distancia():
	print(distancia.get())
#Lista de obstáculos de la noria
obstaculo = IntVar()
lbl_obs=Label(left_frame, text="Seleccione el atenuador que desea\n interponer entre la muestra y el detector",
			font=("Times New Roman", 12),bg='white', padx=10)
lbl_obs.grid(pady=20,column=0, row=2)
# left_canvas=Canvas(left_frame)
# left_canvas.create_line(15, 25, 200, 25)
# left_canvas.grid(column=0, row=2)
obs0 = Radiobutton(left_frame,text='Sin atenuador', value=0, variable=obstaculo, bg='white',font=("Times New Roman", 12))
obs1 = Radiobutton(left_frame,text='Al 2.550cm', value=1, variable=obstaculo,bg='white',font=("Times New Roman", 12)) 
obs2 = Radiobutton(left_frame,text='Pb 0.080cm', value=2, variable=obstaculo,bg='white',font=("Times New Roman", 12))
obs4 = Radiobutton(left_frame,text='Al 0.935cm', value=4, variable=obstaculo,bg='white',font=("Times New Roman", 12))
obs5 = Radiobutton(left_frame,text='Pb 0.320cm', value=5, variable=obstaculo,bg='white',font=("Times New Roman", 12))
obs6 = Radiobutton(left_frame,text='Al 0.450cm ', value=6, variable=obstaculo,bg='white',font=("Times New Roman", 12))
obs7 = Radiobutton(left_frame,text='Pb 0.160cm', value=7, variable=obstaculo,bg='white',font=("Times New Roman", 12))
btn = Button(left_frame, text="Cambiar obstáculo", command=cambiar_obstaculo, font=("Times New Roman", 12))
obs0.grid(padx=2, pady=2, column=0, row=4)
obs1.grid(padx=2, pady=2, column=0, row=5)
obs2.grid(padx=2, pady=2, column=0, row=6)
obs4.grid(padx=2, pady=2, column=0, row=7)
obs5.grid(padx=2, pady=2, column=0, row=8)
obs6.grid(padx=2, pady=2, column=0, row=9)
obs7.grid(padx=2, pady=2, column=0, row=10) 
btn.grid(padx=2, pady=2, column=0, row=12)

#Lista de distancias
lbl_distancia=Label(left_frame, text="Defina la distancia en cm\nentre el detector y la muestra",
			font=("Times New Roman", 12),bg='white')
lbl_distancia.grid(column=0, row=15, pady=20)
distancia = Spinbox(left_frame, from_=8, to=28, width=5)
distancia.grid(pady=10,column=0,row=20)
#lbl_cm=Label(left_frame, text="cm",font=("Times New Roman", 12),bg='white')
#lbl_cm.grid(column=1,row=20)
btn = Button(left_frame, text="Seleccionar", command=def_distancia, font=("Times New Roman", 12))
btn.grid(padx=2, pady=2, column=0, row=22)

Nbuttons = 12

def buttonfunction(index):
	for i in range(Nbuttons):
		buttons[i].config(state="disabled")
	if index == 0:
		demoscope3.scope()
	elif index == 1:
		demoscope3.storedata(300)
	elif index == 2:
		demoscope3.plotsignal()
	elif index == 3:
		demoscope3.plotfourier()
	elif index == 4:
		demoscope3.plothistogram()
	elif index == 5:
		demoscope3.activar_envio('Galv+Sharp')
	elif index == 6:
		demoscope3.activar_envio('Pasos+Sharp')
	elif index == 7:
		demoscope3.activar_envio('Galv+Cnt')
	elif index == 8:
		demoscope3.alejar()
	elif index == 9:
		demoscope3.acercar()
	elif index == 10:
		demoscope3.move_noria(input('Obstaculo -> '))
	elif index == 11:
		os.system('clear')
		exit()
	for i in range(Nbuttons):
		buttons[i].config(state="active")
	

button_names = ['Plotear en tiempo real', 'Adquirir y almacenar', 'Graficar senal adquirida', 'Transformada de Fourier',
		'Histograma', 'Galv+Sharp', 'Pasos+Sharp', 'Galv+Cnt', 'Alejar', 'Acercar', 'Mover noria', 'Salir']

buttons = []

for index in range(Nbuttons): 
    n=button_names[index]

    button = Button(right_frame, bg="White", text=n, relief=GROOVE, command=lambda index=index, n=n: buttonfunction(index))

    # Add the button to the window
    button.grid(padx=2, pady=2, row=index, column=0)

    # Add a reference to the button to 'buttons'
    buttons.append(button)

mainloop()
