from tkinter import *

OPTIONS = [
8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28
] #etc

master = Tk()

variable = StringVar(master)
variable.set(OPTIONS[0]) # default value

w = OptionMenu(master, variable, *OPTIONS)
w.pack()

mainloop()