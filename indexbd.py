#https://www.youtube.com/watch?v=W2kAF9pKPPE&t=2733s
#Python Tkinter - Aplicación de Escritorio de Productos con Sqlite3, CRUD

from tkinter import ttk
from tkinter import *

#Libreria para SQLite
import sqlite3
#Libreria para archivos de Excel
import openpyxl

#Abrir archivo de excel
#data_only (solo coge valores, no formulas)
libro = openpyxl.load_workbook("SIMAT.xlsx",data_only=True)
#Indicar con cuál hoja se va a trabajar
hoja = libro.active
#Qué rango voy a trabajar 
celdas = hoja["A1" : "I2835"]

class Estudiantes:
    db_name = 'bdnuevacolombia.db'

    def __init__(self, window):      #Constructor
        self.wind = window          #Propiedad wind que almacena la ventana
        self.wind.title("Modulo Asistencia Votaciones")
        self.wind.geometry("1400x700")

        #Crear un contenedor
        frame = LabelFrame(self.wind, text = 'Registro Estudiantes')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20) 

        #Ingresar identificación estudiante
        Label(frame, text = "Identificación: ").grid(row = 1, column = 0)
        self.identificacion = Entry(frame)
        self.identificacion.focus()     #Posiciona el cursor en esta caja al iniciar la aplicación
        self.identificacion.grid(row = 1, column = 1)

        #Ingresar Apellido1
        Label(frame, text = "Apellido1: ").grid(row = 2, column = 0)
        self.nombre = Entry(frame)
        self.nombre.grid(row = 2, column = 1)

        #Ingresar Apellido2
        Label(frame, text = "Apellido2: ").grid(row = 3, column = 0)
        self.nombre = Entry(frame)
        self.nombre.grid(row = 3, column = 1)

        #Ingresar Nombre1
        Label(frame, text = "Nombre1: ").grid(row = 4, column = 0)
        self.nombre = Entry(frame)
        self.nombre.grid(row = 4, column = 1)

        #Ingresar Nombre2
        Label(frame, text = "Nombre2: ").grid(row = 5, column = 0)
        self.nombre = Entry(frame)
        self.nombre.grid(row = 5, column = 1)

        #Botón Agrear estudiante
        #sticky: Va desde W(Este) hasta E(Oeste) - ocupa todo el ancho
        ttk.Button(frame, text = "Agregar Estudiante", command=self.add_estudiante).grid(row = 6, columnspan = 2, sticky = W + E)

        #Mensaje de salida
        self.message = Label(text = "", fg = "red")
        self.message.grid(row = 7, column = 0, columnspan= 2, sticky=W + E)
                
        #Tabla
        self.tree = ttk.Treeview(height=10, 
                                columns=("#1", "#2", "#3", "#4", "#5", "#6", "#7"))
        self.tree.grid(row = 8, column = 0, columnspan=2)
        self.tree.heading('#0', text="Identificación", anchor= CENTER)
        self.tree.heading('#1', text="Grado", anchor= CENTER)
        self.tree.heading('#2', text="Curso", anchor= CENTER)
        self.tree.heading('#3', text="Apellido1", anchor= CENTER)
        self.tree.heading('#4', text="Apellido2", anchor= CENTER)
        self.tree.heading('#5', text="Nombre1", anchor= CENTER)
        self.tree.heading('#6', text="Nombre2", anchor= CENTER)
        self.tree.heading('#7', text="Asistencia", anchor= CENTER)
        #verscrollbar = ttk.Scrollbar(self.tree, orient=HORIZONTAL, command=self.tree.xview)
        #verscrollbar.pack(side="left", fill="x")
        #self.tree.configure(xscrollcommand=verscrollbar.set)

        #Botones
        ttk.Button(text="ELIMINAR", command = self.borrar_estudiante).grid(row=5, column=0, sticky= W + E)
        #ttk.Button(text="MODIFICAR", command=self.modificar_estudiante).grid(row=5, column=1, sticky= W + E)
        ttk.Button(text="CARGAR LISTA", command=self.seleccionar_curso).grid(row=5, column=1, sticky= W + E)
        #ttk.Button(text="CARGAR LISTA", command=self.leerexcel).grid(row=5, column=1, sticky= W + E)       #Línea para probar el cargue del excel al SQLite
        #Para ´probar la línea anterior la función leerexcel debe tener solo un argumento leerexcel(self)
    
        #Eliminar estudiantes de la tabla en la base de datos
        consulta = "DELETE FROM estudiantes;"
        parametros = ""
        self.ejecute_consulta(consulta, parametros)

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
        registro = self.tree.get_children()     #self.tree (tabla de tkinter) get_children (obtiene todos los elementos de la tabla)
        for elemento in registro:
            self.tree.delete(elemento)
        #self.tree.delete(*self.tree.get_children())
        #Consultando datos en tabla estudiantes
        consulta = "SELECT * FROM estudiantes ORDER BY apellido1 DESC"
        db_filas = self.ejecute_consulta(consulta)
        #Rellenando los datos
        for fila in db_filas:
            #print(fila)
            self.tree.insert('', 0, text= fila[0], value = (fila[1],
                             fila[2], fila[3], fila[4], fila[5],
                             fila[6], fila[7]))                         #Lleva los registros de la bd a la tabla(tree) en pantalla 
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
    
    def seleccionar_curso(self):
        #Crear una ventana encima de la anterior para cargar curso en BD
        self.cargarbd_wind = Toplevel()
        self.scroll = Scrollbar(self.cargarbd_wind, orient=VERTICAL)
        self.cargarbd_wind.title = "Cargar Lista"

        #ListBox
        Label(self.cargarbd_wind, text = "Curso: ").grid(row= 0, column=0)
        self.lista_cursos = Listbox(self.cargarbd_wind,
                                          selectmode=SINGLE, 
                                          yscrollcommand=self.scroll.set)
        self.scroll.configure(command=self.lista_cursos.yview)
        self.lista_cursos.grid(row=0, column=3)
        self.scroll.grid(column=1, row=0, sticky="NS")

        consulta = "SELECT * FROM cursos"
        db_filas = self.ejecute_consulta(consulta)
        #Rellenando los datos
        for fila in db_filas:
            self.lista_cursos.insert(fila[0], fila[1])        

        #Capturar selección del ListBox
        # for item in self.curso_seleccionado.curselection():
        #     self.curso = self.curso_seleccionado.get(item)
        #     print(self.curso)

        #Botón cargar curso
        # Button(self.cargarbd_wind, text = "Cargar Lista", 
        #         command=lambda:self.leerexcel(self.curso_seleccionado)).grid(row = 1, column=0, columnspan = 2, sticky = W + E)

        btn_curso_seleccionado = Button(self.cargarbd_wind, text = "Cargar Lista", 
                 command=self.leerexcel).grid(row = 1, column=0, columnspan = 2, sticky = W + E)

    def leerexcel(self):
        bandera = False
        lista_estud = []
        #For para almacenar datos del archivo en la lista_estud
        for fila in celdas:
            #print([celda.value for celda in fila])      #Esta línea es igual a las dos que siguen
            #for celda in fila:
                #print(celda.value)
            registro_estud = [celda.value for celda in fila]  #comprensión de listas
            lista_estud.append(registro_estud)

        #Verificar si el curso escogido ya está en la BD
        consulta = "SELECT * FROM estudiantes ORDER BY apellido1 DESC"
        db_filas = self.ejecute_consulta(consulta)

        #Captura el curso escogido por el usuario en el listbox(lista_cursos)
        indices = self.lista_cursos.curselection()
        curso = ", ".join(self.lista_cursos.get(i) for i in indices)        #curso tipo string

        if curso == "Prejardín1":
            curso = -201
        elif curso == "Prejardín2":
            curso = -202
        elif curso == "Jardín1":
            curso = -101
        elif curso == "Jardín2":
            curso = -102
        elif curso == "Jardín3":
            curso = -103
        elif curso == "Jardín4":
            curso = -104
        elif curso == "Jardín5":
            curso = -105
        elif curso == "Jardín6":
            curso = -106
        elif curso == "Jardín7":
            curso = -107
        elif curso == "Transición1":
            curso = 1
        elif curso == "Transición2":
            curso = 2
        elif curso == "Transición3":
            curso = 3
        elif curso == "Transición4":
            curso = 4
        elif curso == "Transición5":
            curso = 5
        elif curso == "Transición6":
            curso = 6
        elif curso == "Transición7":
            curso = 7
        else:
            curso = int(curso)

        for estudiante in lista_estud:
            if (estudiante[2] == curso) :
                for fila in db_filas:                   #For para verificar si el estudiante ya esta en la BD
                    if (estudiante[3]==fila[0]):
                        bandera = True
                    else:
                        bandera = False
                #verificar si el estudiante ya fue llevado a la bd (estudiante[3] not in db_filas)
                #por medio del número de identificación
                if bandera == False:
                    consulta = "INSERT INTO estudiantes VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
                    parametros = (estudiante[3],estudiante[1],
                                estudiante[2],estudiante[4],
                                estudiante[5],estudiante[6],
                                estudiante[7],0)
                    self.ejecute_consulta(consulta, parametros)
                    #print (f"El estudiante {estudiante[4]} {estudiante[5]} {estudiante[6]} {estudiante[7]} pertenece al curso {estudiante[2]}")
        self.obtener_estudiantes()

if __name__ == "__main__":   #Comprueba para iniciar la aplicación
    window = Tk()
    aplicacion = Estudiantes(window)
    window.mainloop()




