import requests, sqlite3, os
import matplotlib.pyplot as plt, pandas as pd, numpy as np
from datetime import datetime, timedelta
from utils import *

with open ("credentials.env","r") as archivo:
    for linea in archivo:
        if (linea.startswith("apiKey=")):
            key = linea.split('=')[1].strip()
            
crearBD()
while True:
    clear = lambda: os.system('cls')
    clear()
    print("------------------------------------")
    print("MENU PRINCIPAL")
    print("")
    print("Opción 1: Actualización de datos")
    print("Opción 2: Visualización de datos")
    print("Opción 3: Salir")    
    print("------------------------------------")
    opcion = input("Seleccione la opción que desea elegir: ")
    if (opcion == "1"):
        clear()
        ticker = input("Ingrese el ticker que desea visualizar: ")
        fecha_desde = input("Ingrese la fecha desde que desea visualizar los datos(yyyy-mm-dd): ")
        fecha_hasta = input("Ingrese la fecha hasta que desea visualizar los datos(yyyy-mm-dd): ")
        fechas_faltantes = consultarRangos(ticker,fecha_desde,fecha_hasta)
        if (len(fechas_faltantes) == 0):
            print("Ya existen datos para esas fechas indicadas")
        else:
            rangos_para_api = agrupar_fechas(fechas_faltantes)
            print(f"Se buscaran datos para los siguientes periodos para el ticker {ticker}:")
            hay_datos = False
            for inicio,fin in rangos_para_api:
                print(f'{inicio.strftime("%Y-%m-%d")} - {fin.strftime("%Y-%m-%d")}')
                fecha_inicio = inicio.strftime("%Y-%m-%d")
                fecha_fin = fin.strftime("%Y-%m-%d")
                # Acá deberíamos llamar a la API y traernos la info para cada rango, así lo guardamos en la bd
                datos = consultar_api(ticker,fecha_inicio,fecha_fin,key)
                print(".")
                print(".")
                print(".")
                if (datos["resultsCount"] == 0):
                    print(f"No hay registros para el ticker seleccionado en el rango {fecha_inicio} - {fecha_fin}")
                else:
                    hay_datos = True
                    insertardatos(datos,fecha_inicio,fecha_fin)
            if(hay_datos):
                print("Datos insertados correctamente")
        os.system("pause")
    elif (opcion == "2"):
        clear()
        print("------------------------------------")
        print("MENU VISUALIZACIÓN DE GRÁFICOS")
        print("")
        print("Opción 1: Resumen de datos guardados")
        print("Opción 2: Visualización de gráficos")
        print("Opción 3: Volver")
        print("------------------------------------")
        opcion2 = input("Ingrese la opción que desea visualizar: ")
        if (opcion2 == "1"):
            clear()
            visualizarResumen()
            os.system("pause")
        elif (opcion2 == "2"):
            clear()
            ticker = input("Ingrese el ticker que desea visualizar: ")
            visualizarGrafico(ticker)
            os.system("pause")
        elif (opcion2 == "3"):
            pass   
        else:
            print("Opcion Incorrecta")
            os.system("pause")
    elif (opcion == "3"):
        break    
    else:
        print("Opcion Incorrecta")
        os.system("pause")