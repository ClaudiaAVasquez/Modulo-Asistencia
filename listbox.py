from tkinter import ttk
from tkinter import *
from tkinter import messagebox

def obtener_seleccion():
    indices = curso_seleccionado.curselection()
    messagebox.showinfo(
        title="items seleccionados",
        message=", ".join(curso_seleccionado.get(i) for i in indices)
    )

win=Tk()
win.title("Modulo Asistencia Votaciones")

curso_seleccionado = Listbox(win,selectmode=SINGLE)

curso_seleccionado.insert(0,"H")
curso_seleccionado.insert(1,"o")
curso_seleccionado.insert(2,"l")
curso_seleccionado.insert(3,"a")
curso_seleccionado.pack()

btn_obtener_seleccion = Button(win, text = "Seleccionar",command=obtener_seleccion)
btn_obtener_seleccion.pack()
win.mainloop()

