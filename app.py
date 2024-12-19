from base_de_datos import BaseDeDatos
from api import Api
from menu import Menu
import pandas as pd
import os
from datetime import datetime

# Clase App
class App:
    # Constructor
    def __init__(self):
        self.db = BaseDeDatos()
        self.validar_credentials()
        self.api = Api(self.key)

    # Métodos
    # Método que verifica si existe credentials.env
    def validar_credentials(self):
        if os.path.exists("credentials.env"):
            with open("credentials.env", "r") as archivo:
                for linea in archivo:
                    if linea.startswith("apiKey="):
                        self.key = linea.split('=')[1].strip()
                        return True
                return False
        else:
            self.get_credentials()
            return False
        
    # Método que pide al usuario la key de la API y genera el archivo credentials.env
    def get_credentials(self):
        print("No se encuentra configurada la apiKey de polygon.io.")
        self.key = input("Por favor, ingrese su clave de API: ")
        with open("credentials.env", "w") as archivo:
            archivo.write(f"apiKey={self.key}\n")
        print("Archivo credentials.env creado con la clave ingresada.\n")
        os.system("pause")

    # Método main de la app que muestra el menu
    def main(self):
        menu = Menu(self)
        menu.mostrar_menu_principal()

    # Método que consulta los datos necesarios en la API y los guarda en la BD
    def actualizar_datos(self, ticker, fecha_desde, fecha_hasta):
        try:
            self.validar_fechas(fecha_desde, fecha_hasta)
            fechas_faltantes = self.db.consultar_fechas_faltantes(ticker, fecha_desde, fecha_hasta)
            if len(fechas_faltantes) == 0:
                raise ValueError("\n.\n.\nYa existen datos para esas fechas indicadas")
            else:
                rangos_para_api = self.agrupar_fechas(fechas_faltantes)
                print(f"Se buscaran datos para los siguientes periodos para el ticker {ticker}:")
                hay_datos = False
                for inicio,fin in rangos_para_api:
                    print(f'{inicio.strftime("%Y-%m-%d")} - {fin.strftime("%Y-%m-%d")}')
                    fecha_inicio = inicio.strftime("%Y-%m-%d")
                    fecha_fin = fin.strftime("%Y-%m-%d")
                    datos = self.api.consultar_datos(ticker, fecha_inicio, fecha_fin)
                    if datos is not None:
                        if (datos["resultsCount"] == 0):
                            raise ValueError(f"No hay registros para el ticker seleccionado en el rango {fecha_inicio} - {fecha_fin}")
                        else:
                            self.db.insertar_datos(datos, fecha_inicio, fecha_fin)
                            hay_datos = True
                    else:
                        raise ValueError("\n.\n.\nNo se pudo obtener la respuesta de la API.")
                if hay_datos:
                    return True
                else:
                    return False
        except ValueError as e:
            raise     
    
    # Método que consulta el resumen de todos los tickers guardados en la BD
    def visualizar_resumen(self):
        df = self.db.consultar_resumen()
        return df

    # Método que consulta los datos para visualizar un gráfico en la BD para un ticker determinado
    def visualizar_grafico(self, ticker):
        df = self.db.consultar_datos(ticker)
        return df
    
    # Método que valida las fechas ingresadas por el usuario
    def validar_fechas(self, fecha_desde, fecha_hasta):
        try:
            try:
                desde = datetime.strptime(fecha_desde, "%Y-%m-%d")
                hasta = datetime.strptime(fecha_hasta, "%Y-%m-%d")
            except:
                raise ValueError("\n.\n.\nLa fecha ingresada no es correcta.")
            if desde > hasta:
                raise ValueError("\n.\n.\nLa fecha desde no puede ser mayor que la fecha hasta.")
            elif desde > datetime.now() or hasta > datetime.now():
                raise ValueError("\n.\n.\nNo se puede colocar una fecha futura")
        except ValueError as e:
            raise
        
    # Método que genera los rangos necesarios para consultar la API segun una lista de fechas recibida
    def agrupar_fechas(self, fechas):
        rangos = []
        # Ordeno las fechas
        fechas.sort()

        # Inicializo el primer rango (con fecha fin como primera fecha y despues voy cambiando)
        inicio_rango = fechas[0]
        fin_rango = fechas[0]

        # Recorro todas las fechas de la lista en orden
        for i in range(1, len(fechas)):
            if (fechas[i] - fin_rango).days == 1: # Fecha continua
                fin_rango = fechas[i]
            else: # NO es continua -> hay un salto de fecha, entonces termina el rango
                rangos.append((inicio_rango, fin_rango))
                inicio_rango = fechas[i]
                fin_rango = fechas[i]

        # Agrego el ultimo rango
        rangos.append((inicio_rango, fin_rango))

        return rangos

    # Método que consulta la BD para validar si existen datos para un ticker en particular
    def validarTicker(self, ticker):
        return self.db.validar_ticker(ticker)

    