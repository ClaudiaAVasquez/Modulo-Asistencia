#https://www.youtube.com/watch?v=W2kAF9pKPPE&t=2733s
#Python Tkinter - Aplicación de Escritorio de Productos con Sqlite3, CRUD

from tkinter import ttk
from tkinter import *

import sqlite3

class Estudiantes:
    db_name = 'bdestudiantes.db'

    def __init__(self, window):      #Constructor
        self.wind = window          #Propiedad wind que almacena la ventana
        self.wind.title("Aplicación Estudiantes")

        #Crear un contenedor
        frame = LabelFrame(self.wind, text = 'Registro Estudiantes')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        #Ingresar identificación estudiante
        Label(frame, text = "Identificación: ").grid(row = 1, column = 0)
        self.identificacion = Entry(frame)
        self.identificacion.focus()     #Posiciona el cursor en esta caja al iniciar la aplicación
        self.identificacion.grid(row = 1, column = 1)

        #Ingresar Nombre
        Label(frame, text = "Nombre").grid(row = 2, column = 0)
        self.nombre = Entry(frame)
        self.nombre.grid(row = 2, column = 1)

        #Botón Agrear estudiante
        #sticky: Va desde W(Este) hasta E(Oeste) - ocupa todo el ancho
        ttk.Button(frame, text = "Guardar Estudiante", command=self.add_estudiante).grid(row = 3, columnspan = 2, sticky = W + E)

        #Mensaje de salida
        self.message = Label(text = "", fg = "red")
        self.message.grid(row = 3, column = 0, columnspan= 2, sticky=W + E)
                
        #Tabla
        self.tree = ttk.Treeview(height=10, columns=2)      #height (filas en la tabla) columns(campos en la tabla)
        self.tree.grid(row = 4, column = 0, columnspan=2)
        self.tree.heading('#0', text="Identificación", anchor= CENTER)
        self.tree.heading('#1', text="Nombre", anchor= CENTER)

        #Botones
        ttk.Button(text="ELIMINAR", command = self.borrar_estudiante).grid(row=5, column=0, sticky= W + E)
        ttk.Button(text="MODIFICAR", command=self.modificar_estudiante).grid(row=5, column=1, sticky= W + E)

        #Mostrar estudiantes en la tabla
        self.obtener_estudiantes()

    def ejecute_consulta(self, consulta, parametros = ()):   #función para hacer consulta a la BD - parametros es una tupla vacia
        with sqlite3.connect(self.db_name) as conn:          #Método para conexión a la BD, conn guarda la conexión
            posicion = conn.cursor()                         #Me permite saber en qué registro está ubicada
            resultado = posicion.execute(consulta, parametros)
            conn.commit()
        return resultado
    
    def obtener_estudiantes(self):  #Función para leer registros
        #Limpiando la tabla estudiantes
        registro = self.tree.get_children()     #self.tree (tabla) get_children (obtiene todos los elementos de la tabla)
        for elemento in registro:
            self.tree.delete(elemento)
        #Consultando datos en tabla estudiantes
        consulta = "SELECT * FROM estudiantes ORDER BY identificacion DESC"
        db_filas = self.ejecute_consulta(consulta)
        #Rellenando los datos
        for fila in db_filas:
            #print(fila)
            self.tree.insert('', 0, text= fila[0], value = fila[1])
            #print(fila)
    
    def validacion_estudiante(self):
        return len(self.identificacion.get()) != 0 and len(self.nombre.get()) != 0     #.get captura lo que el usr ingresa

    def add_estudiante(self):
        if self.validacion_estudiante():
            consulta = 'INSERT INTO estudiantes VALUES(?, ?)'
            parametros =  (self.identificacion.get(), self.nombre.get())
            self.ejecute_consulta(consulta, parametros)
            print("Datos guardados")
            self.message["text"] = "El Estudiante {} ha sido agregado exitosamente".format(self.nombre.get())
            self.identificacion.delete(0, END)
            self.nombre.delete(0, END)
            #print(self.identificacion.get())
            #print(self.nombre.get())
        else:
            print('Identificación y/o nombre requerido')
            self.message["text"] = "La identificación y el nombre son requeridos"
        self.obtener_estudiantes()

    def borrar_estudiante(self):
        #Limpiar mensaje en pantalla
        self.message["text"] = ""
        try:
            #Capturar el texto=identificación del registro seleccionado
            #ejemplo registro seleccionado -->
            #{'text': '1111', 'image': '', 'values': ['zzzzzz'], 'open': 0, 'tags': ''}
            self.tree.item(self.tree.selection())["text"][0]
        except IndexError as error:
            self.message["text"] = "Selecciona primero el estudiante"
            return
        self.message["text"] = ""
        identificacion = self.tree.item(self.tree.selection())["text"]
        consulta = "DELETE FROM estudiantes WHERE identificacion = ?"
        self.ejecute_consulta(consulta, (identificacion, ))
        self.message["text"] = "El estudiante {} ha sido eliminado exitosamente".format(identificacion)
        #Actualizar tabla
        self.obtener_estudiantes()
    
    def modificar_estudiante(self):
        self.message["text"] = ""
        try:
            #Capturar el texto=identificación del registro seleccionado
            #ejemplo registro seleccionado -->
            #{'text': '1111', 'image': '', 'values': ['zzzzzz'], 'open': 0, 'tags': ''}
            self.tree.item(self.tree.selection())["text"][0]
        except IndexError as error:
            self.message["text"] = "Selecciona primero el estudiante"
            return
        old_identificacion = self.tree.item(self.tree.selection())["text"]
        old_nombre = self.tree.item(self.tree.selection())["values"][0]
        
        #Crear una ventana encima de la anterior para modificar registro
        self.mod_wind = Toplevel()
        self.mod_wind.title = "Modificar Estudiante"

        #old_identificacion
        Label(self.mod_wind, text = "Identificación: ").grid(row= 0, column=1)
        Entry(self.mod_wind, textvariable=StringVar(self.mod_wind, value = 
        old_identificacion), state="readonly").grid(row = 0, column=2)
      
        #Nueva identificacion
        Label(self.mod_wind, text="New ident.: ").grid(row = 1, column = 1)
        self.New_identificacion = Entry(self.mod_wind)
        self.New_identificacion.grid(row = 1, column=2)

        #old_nombre
        Label(self.mod_wind, text="Nombre: ").grid(row=2, column=1)
        Entry(self.mod_wind, textvariable=StringVar(self.mod_wind, value=
        old_nombre), state = "readonly").grid(row=2, column=2)

        #Nuevo_nombre
        Label(self.mod_wind, text="Nuevo Nombre: ").grid(row=3, column=1)
        self.Nuevo_nombre = Entry(self.mod_wind)
        self.Nuevo_nombre.grid(row=3, column=2)

        Button(self.mod_wind, text= "ACTUALIZAR", command=lambda:self.mod_registro(self.New_identificacion.get(), 
        old_identificacion, self.Nuevo_nombre.get(), old_nombre)).grid(row=4, column=2, sticky=W)

    def mod_registro(self, New_identificacion, old_identificacion, Nuevo_nombre, old_nombre):
        consulta = "UPDATE estudiantes SET identificacion = ?, nombre = ? WHERE identificacion = ? AND nombre = ?"
        parametros = (New_identificacion, Nuevo_nombre, old_identificacion, old_nombre)
        self.ejecute_consulta(consulta, parametros)
        self.mod_wind.destroy()          #Cuando el usr de clic sobre ACTUALIZAR se cierra la ventana de modificación
        self.message["text"]= "El Estudiante {} ha sido actulizado exitosamente".format(New_identificacion)
        self.obtener_estudiantes()

if __name__ == "__main__":   #Comprueba para iniciar la aplicación
    window = Tk()
    aplicacion = Estudiantes(window)
    window.mainloop()
