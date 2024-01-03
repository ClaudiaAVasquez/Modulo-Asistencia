#https://www.youtube.com/watch?v=1xjgY5Wpwto
#Leer archivos de Excel con Python (CLASE COMPLETA)
#Libreria para leer archivos de Excel
import openpyxl

#Librerias para enviar correos electrónicos
import smtplib, ssl
import getpass

#Abrir archivo de excel
#data_only (solo coge valores, no formulas)
libro = openpyxl.load_workbook("SIMAT.xlsx",data_only=True)
#Indicar con cuál hoja se va a trabajar
hoja = libro.active
#Qué rango voy a trabajar 
celdas = hoja["A1" : "AQ5"]

def leer_archivo():
    lista_estud = []

    #For para almacenar datos del archivo en la lista_estud
    for fila in celdas:
        #print([celda.value for celda in fila])      #Esta línea es igual a las dos que siguen
        #for celda in fila:
        #print(celda.value)
        registro_estud = [celda.value for celda in fila]  #comprensión de listas
        lista_estud.append(registro_estud)

    for estudiante in lista_estud:
        print (f"El estudiante {estudiante[25]} {estudiante[26]} {estudiante[27]} {estudiante[28]} pertenece al curso {estudiante[14]}")

def enviar_correo():
    #Solicita usuario y contraseña para correo
    username = input("Ingrese su nombre de usuario: ")
    password = getpass.getpass("Ingrese su password: ")

    #Crea la conexión para el correo electrónico
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(username, password)
        print("Inició sesión en Gmail")

        for estudiante in lista_estud:
            destinatario = estudiante[43]
            mensaje = ("Prueba para enviar mensajes de correo desde Python")
            server.sendmail(username, destinatario, mensaje)
            print("Mensaje enviado")
            
def main():
    leer_archivo()

main()

    


