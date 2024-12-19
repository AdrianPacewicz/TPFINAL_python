import matplotlib.pyplot as plt, pandas as pd, os

# Clase Menu
class Menu:
    def __init__(self, app):
        self.app = app
    
    def mostrar_menu_principal(self):
        # menu
        while True:
            self.clear()
            print("------------------------------------")
            print("MENU PRINCIPAL")
            print("")
            print("Opción 1: Actualización de datos")
            print("Opción 2: Visualización de datos")
            print("Opción 3: Salir")
            print("------------------------------------")
            opcion = input("Seleccione la opción que desea elegir: ")
            # Actualización de datos
            if (opcion == "1"):
                self.clear()
                ticker = input("Ingrese el ticker que desea visualizar: ")
                fecha_desde = input("Ingrese la fecha desde que desea visualizar los datos(yyyy-mm-dd): ")
                fecha_hasta = input("Ingrese la fecha hasta que desea visualizar los datos(yyyy-mm-dd): ")
                try:
                    if(self.app.actualizar_datos(ticker,fecha_desde,fecha_hasta)):
                        print("\n.\n.\n.\nDatos insertados correctamente.")
                        os.system("pause")
                except ValueError as e:
                    print(e)
                    os.system("pause")
            elif (opcion == "2"):
                self.mostrar_menu_visualizacion()
            elif (opcion == "3"):
                break
            else:
                print("Opcion Incorrecta")
                os.system("pause")


    def mostrar_menu_visualizacion(self):
        self.clear()
        print("------------------------------------")
        print("MENU VISUALIZACIÓN DE GRÁFICOS")
        print("")
        print("Opción 1: Resumen de datos guardados")
        print("Opción 2: Visualización de gráficos")
        print("Opción 3: Volver")
        print("------------------------------------")
        opcion = input("Ingrese la opción que desea visualizar: ")
        # Resumen de datos
        if (opcion == "1"):
            self.clear()
            print("Los tickers guardados en la base de datos son:\n")
            print(self.app.visualizar_resumen())
            os.system("pause")
        # Gráficos
        elif (opcion == "2"):
            self.clear()
            ticker = input("Ingrese el ticker que desea visualizar: ")
            if(self.app.validarTicker(ticker)):
                df = self.app.visualizar_grafico(ticker)
                self.graficar(df)
                os.system("pause")
            else:
                print(".\n.\n.\nNo hay registros para el ticker seleccionado")
                os.system("pause")
        # Volver
        elif (opcion == "3"):
            pass   
        else:
            print("Opcion Incorrecta")
            os.system("pause")

    def graficar(self, df):
        x1 = df["fecha"]
        y1 = df["close"]
    
        x2 = df["fecha"]
        y2 = df["high"]
    
        x3 = df["fecha"]
        y3 = df["low"]
    
        x4 = df["fecha"]
        y4 = df["open"]
    
        fig, ax = plt.subplots()
        ax.plot(x1, y1, marker = "o", label = "close")
        ax.plot(x2, y2, marker = "o", label = "high")
        ax.plot(x3, y3, marker = "o", label = "low")
        ax.plot(x4, y4, marker = "o", label = "open")
        ax.legend()
        plt.show()

    def clear(self):
        os.system('cls')
