import sqlite3, requests
import matplotlib.pyplot as plt, pandas as pd, numpy as np
from datetime import datetime, timedelta

def crearBD(): 
    # Creamos la conexion a la Base de Datos
    conn = sqlite3.connect("TPFINAL.db")

    # Creamos el curso para interactuar con los datos
    cursor = conn.cursor()

    # Ejecutar comandos de SQL
    cursor.execute(f'''
        CREATE TABLE if not exists ticker (
        ticker_id INTEGER PRIMARY KEY autoincrement,
        ticker TEXT NOT NULL,
        fecha_desde DATETIME NOT NULL,
        fecha_hasta DATETIME NOT NULL
    );
    ''')
    cursor.execute(f'''
        CREATE TABLE if not exists precios (
        id INTEGER PRIMARY KEY autoincrement,
        ticker_id INTEGER NOT NULL,
        fecha DATETIME NOT NULL,
        close REAL NOT NULL,
        high REAL NOT NULL,
        low REAL NOT NULL,
        number INTEGER NOT NULL,
        open REAL NOT NULL,
        volumen REAL NOT NULL,
        volumen_weighted REAL NOT NULL,
        FOREIGN KEY(ticker_id) REFERENCES ticker(ticker_id)
    );
    ''')
    conn.commit()    
    
def consultarRangos(ticker,fecha_desde,fecha_hasta):
    conn = sqlite3.connect("TPFINAL.db")
    cursor = conn.cursor()
    res = cursor.execute(f'''
        select fecha_desde, fecha_hasta from ticker where ticker = ? order by 1 asc;
        ''',[ticker])

    rangos_existentes = cursor.fetchall()
    fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
    fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d')
    fechas_faltantes = []
    fecha_actual = fecha_desde
    while fecha_actual <= fecha_hasta:
        en_rango = False
        for fecha_desde_db, fecha_hasta_db in rangos_existentes:
            fecha_desde_db = datetime.strptime(fecha_desde_db, '%Y-%m-%d')
            fecha_hasta_db = datetime.strptime(fecha_hasta_db, '%Y-%m-%d')
            if fecha_desde_db <= fecha_actual <= fecha_hasta_db:
                en_rango = True
                fecha_actual = fecha_hasta_db + timedelta(days=1)
                break
        if not en_rango:
            fechas_faltantes.append(fecha_actual)
            fecha_actual += timedelta(days=1)

    return fechas_faltantes 
    
def agrupar_fechas(fechas):
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

def consultar_api(ticker, inicio, fin,key):
    r = requests.get(f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{inicio}/{fin}?adjusted=true&sort=asc&apiKey={key}')
    diccionario = dict(r.json())
    return diccionario

def insertardatos(diccionario, fecha_desde, fecha_hasta):
    # Creamos la conexion a la Base de Datos
    conn = sqlite3.connect("TPFINAL.db")
    cursor = conn.cursor()
    cursor.execute(f'''
        INSERT INTO ticker (ticker, fecha_desde, fecha_hasta)
        VALUES ('{diccionario["ticker"]}', '{fecha_desde}', '{fecha_hasta}');
        ''')
    id = cursor.lastrowid
    conn.commit()
    
    for item in diccionario["results"]:
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO precios (ticker_id, fecha, close, high, low, number, open, volumen, volumen_weighted)
            VALUES ({id}, '{item["t"]}', '{item["c"]}', '{item["h"]}', '{item["l"]}', '{item["n"]}', '{item["o"]}', '{item["v"]}', '{item["vw"]}');
            ''')
        conn.commit()
        
def visualizarResumen():
    conn = sqlite3.connect("TPFINAL.db")
    df = pd.read_sql_query("SELECT ticker, fecha_desde, fecha_hasta FROM ticker order by ticker asc, fecha_desde asc", conn)
    print("Los tickers guardados en la base de datos son:\n")
    print(df)
    
def visualizarGrafico(ticker):
    conn = sqlite3.connect("TPFINAL.db")
    df2 = pd.read_sql_query('''SELECT date(fecha/1000,'unixepoch') as Fecha, close, high, low, number, open, volumen, volumen_weighted
                            FROM precios p
                            INNER JOIN ticker t ON p.ticker_id = t.ticker_id
                            where t.ticker = ?''', conn,params=[ticker])
    x1 = df2["Fecha"]
    y1 = df2["close"]
 
    x2 = df2["Fecha"]
    y2 = df2["high"]
   
    x3 = df2["Fecha"]
    y3 = df2["low"]
   
    x4 = df2["Fecha"]
    y4 = df2["open"]
 
    fig, ax = plt.subplots()
    ax.plot(x1, y1, marker = "o", label = "close")
    ax.plot(x2, y2, marker = "o", label = "high")
    ax.plot(x3, y3, marker = "o", label = "low")
    ax.plot(x4, y4, marker = "o", label = "open")
    ax.legend()
    plt.show()