import os
import demoscope3
from tkinter import *
from tkinter import ttk, Canvas

master = Tk()
master.title("Laboratorio remoto- LFN USB")
master.geometry('700x700')

top_frame = Frame(master, bg='white', width = 700, height=700, padx=10, pady=10)
#top_frame.grid(column=0, row=0)
top_frame.pack(side= TOP, fill=BOTH)
lbl = Label(top_frame, text="Laboratorio remoto - Espectrometría gamma", font=("Times New Roman", 20),bg='white')
lbl.pack(side=TOP, padx=10, pady=10)
#left_frame = Frame(master, bg='white', width = 300)
#left_frame.grid(column=0, row=5)
#left_frame.pack(side= LEFT, fill=BOTH)
#right_frame = Frame(master, bg='white', width = 300)
#right_frame.grid(column=10, row=5)
#right_frame.pack(side= RIGHT, fill=BOTH)
#center_frame=Frame(master, bg='white', width=500, height=1000)
#center_frame.pack(side=TOP, fill=X)

#Para probar que los indices de los obstáculos sean los correctos
def cambiar_obstaculo():
    demoscope3.move_noria(obstaculo.get())
def def_distancia():
	demoscope3.move_Zahlrohr_sharp(distancia.get())
	#print(distancia.get())
#Lista de obstáculos de la noria
obstaculo = IntVar()
lbl_obs=Label(top_frame, text="Seleccione el atenuador que desea\n interponer entre la muestra y el detector",
			font=("Times New Roman", 12),bg='white', padx=10,pady=10)
lbl_obs=lbl_obs.pack(side= TOP, fill=Y)
#lbl_obs.grid(pady=20,column=0, row=2)
# left_canvas=Canvas(left_frame)
# left_canvas.create_line(15, 25, 200, 25)
# left_canvas.grid(column=0, row=2)
obs0 = Radiobutton(top_frame,text='Sin atenuador', value=0, variable=obstaculo, bg='white',font=("Times New Roman", 12))
obs1 = Radiobutton(top_frame,text='Al 2.550cm', value=1, variable=obstaculo,bg='white',font=("Times New Roman", 12)) 
obs2 = Radiobutton(top_frame,text='Pb 0.080cm', value=2, variable=obstaculo,bg='white',font=("Times New Roman", 12))
obs4 = Radiobutton(top_frame,text='Al 0.935cm', value=4, variable=obstaculo,bg='white',font=("Times New Roman", 12))
obs5 = Radiobutton(top_frame,text='Pb 0.320cm', value=5, variable=obstaculo,bg='white',font=("Times New Roman", 12))
obs6 = Radiobutton(top_frame,text='Al 0.450cm ', value=6, variable=obstaculo,bg='white',font=("Times New Roman", 12))
obs7 = Radiobutton(top_frame,text='Pb 0.160cm', value=7, variable=obstaculo,bg='white',font=("Times New Roman", 12))
btn = Button(top_frame, text="Cambiar obstáculo", command=cambiar_obstaculo, font=("Times New Roman", 12))
obs0.pack(side= TOP, fill=Y)
obs1.pack(side= TOP, fill=Y)
obs2.pack(side= TOP, fill=Y)
obs4.pack(side= TOP, fill=Y)
obs5.pack(side= TOP, fill=Y)
obs6.pack(side= TOP, fill=Y)
obs7.pack(side= TOP, fill=Y)
btn.pack(side= TOP, fill=Y, pady=10)
# obs0.grid(padx=2, pady=2, column=0, row=4)
# obs1.grid(padx=2, pady=2, column=0, row=5)
# obs2.grid(padx=2, pady=2, column=0, row=6)
# obs4.grid(padx=2, pady=2, column=0, row=7)
# obs5.grid(padx=2, pady=2, column=0, row=8)
# obs6.grid(padx=2, pady=2, column=0, row=9)
# obs7.grid(padx=2, pady=2, column=0, row=10) 
# btn.grid(padx=2, pady=2, column=0, row=12)

#Lista de distancias
distancia=StringVar()
lbl_distancia=Label(top_frame, text="Defina la distancia en cm\nentre el detector y la muestra",
			font=("Times New Roman", 12),bg='white')
lbl_distancia.pack(side= TOP, fill=Y)
dist_array=['8.3','10','11.7','13.4','15.1','16.8','18.5','20.2','21.9','23.6','25.3','27','28.7','30.4','32.1','33.8']
#lbl_distancia.grid(column=0, row=15, pady=20)
dist_menu=OptionMenu(top_frame, distancia, *dist_array) 
distancia.set('8.3')
dist_menu.pack(side=TOP, fill=Y, pady=10)
# distancia = Spinbox(top_frame, from_=0, to=5, width=5)
# distancia.pack(side= TOP, fill=Y,pady=10)
#distancia.grid(pady=10,column=0,row=20)
#lbl_cm=Label(left_frame, text="cm",font=("Times New Roman", 12),bg='white')
#lbl_cm.grid(column=1,row=20)
btn = Button(top_frame, text="Seleccionar", command=def_distancia, font=("Times New Roman", 12))
btn.pack(side= TOP, fill=Y,pady=10)
#btn.grid(padx=2, pady=2, column=0, row=22)

Nbuttons = 6

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
		os.system('clear')
		exit()
	for i in range(Nbuttons):
		buttons[i].config(state="active")
	

button_names = ['Plotear en tiempo real', 'Adquirir y almacenar', 'Graficar senal adquirida', 'Transformada de Fourier',
		'Histograma', 'Salir']

buttons = []

for index in range(Nbuttons): 
    n=button_names[index]

    button = Button(top_frame, bg="White", text=n, relief=GROOVE, command=lambda index=index, n=n: buttonfunction(index),font=("Times New Roman", 12))

    # Add the button to the window
    button.pack(side=TOP, fill=Y)

    # Add a reference to the button to 'buttons'
    buttons.append(button)

mainloop()
