import requests
import sqlite3
import pandas
import os
from datetime import datetime, timedelta
from utils import *

with open ("credentials.env","r") as archivo:
    for linea in archivo:
        if (linea.startswith("apiKey=")):
            key = linea.split('=')[1].strip()
            
crearBD()

print("Opción 1: Actualización de datos")
print("Opción 2: Visualización de datos")
opcion = input("Seleccione la opción que desea elegir: ")
clear = lambda: os.system('cls')
clear()
if (opcion == "1"):
    ticker = input("Ingrese el ticker que desea visualizar: ")
    fecha_desde = input("Ingrese la fecha desde que desea visualizar los datos(yyyy-mm-dd): ")
    fecha_hasta = input("Ingrese la fecha hasta que desea visualizar los datos(yyyy-mm-dd): ")
    fechas_faltantes = consultarRangos(ticker,fecha_desde,fecha_hasta)
    rangos_para_api = agrupar_fechas(fechas_faltantes)
    for inicio,fin in rangos_para_api:
        print(f'{inicio.strftime("%Y-%m-%d")} - {fin.strftime("%Y-%m-%d")}')
        fecha_inicio = inicio.strftime("%Y-%m-%d")
        fecha_fin = fin.strftime("%Y-%m-%d")
        # Acá deberíamos llamar a la API y traernos la info para cada rango, así lo guardamos en la bd
        datos = consultar_api(ticker,fecha_inicio,fecha_fin,key)
        insertardatos(datos,fecha_inicio,fecha_fin)
    print("Datos insertados correctamente")
        
