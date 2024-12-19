import matplotlib.pyplot as plt, pandas as pd, os

# Clase Menu
class Menu:
    # Constructor
    def __init__(self, app):
        self.app = app
    
    # Método que muestra el menú principal de la aplicación
    def mostrar_menu_principal(self):
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
                self.app.db.desconectar()
                break
            else:
                print("Opcion Incorrecta")
                os.system("pause")

    # Método que muestra el menú de visualización de la aplicación
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
            opcion3 = input("\n1- Gráfico Comparativo \n2- Gráfico de Barras \nIngrese el tipo de gráfico que sea visualizar: ")
            if(self.app.validarTicker(ticker)):
                df = self.app.visualizar_grafico(ticker)
                self.graficar(df,opcion3)
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

    # Método que dado un dataframe y una opción grafica lo solicitado
    def graficar(self, df, opcion):
        x1 = df["fecha"]
        y1 = df["close"]
    
        x2 = df["fecha"]
        y2 = df["high"]
    
        x3 = df["fecha"]
        y3 = df["low"]
    
        x4 = df["fecha"]
        y4 = df["open"]

        if(opcion == "1"):
            fig, ax = plt.subplots()
            ax.plot(x1, y1, label = "Close", color='blue', markersize = 5, marker = '.')
            ax.plot(x2, y2, label = "High", color='green', markersize = 5, marker = '.')
            ax.plot(x3, y3, label = "Low", color='red', markersize = 5, marker = '.')
            ax.plot(x4, y4, label = "Open", color='yellow', markersize = 5, marker = '.')
            ax.set_xlabel('Fecha')
            ax.set_ylabel('Valor')
            ax.grid(True)
            ax.set_title('Gráfico')
            ax.legend()
            plt.show()
        elif (opcion == "2"):
            fig, axs = plt.subplots(2,2)
            axs[0,0].bar(x1,y1, label = "Close", color='blue')
            axs[0,0].set_title("Close")
            axs[0,1].bar(x2,y2, label = "High", color='green') 
            axs[0,1].set_title("High")
            axs[1,0].bar(x3,y3, label = "Low", color='red')
            axs[1,0].set_title("Low")
            axs[1,1].bar(x4,y4, label = "Open", color='yellow') 
            axs[1,1].set_title("Open")
            plt.show()
        else:
            print("Opcion Incorrecta")

    # Método que limpia la terminal
    def clear(self):
        os.system('cls')
