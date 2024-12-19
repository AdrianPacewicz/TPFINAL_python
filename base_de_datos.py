import sqlite3, pandas as pd
from datetime import datetime, timedelta

# Clase encargada de interactuar con la base de datos sqlite
class BaseDeDatos:
    # Constructor
    def __init__(self, nombre_bd="TPFINAL.db"):
        self.nombre_bd = nombre_bd
        self.conexion = None
        self.cursor = None
        self.conectar()

    # Metodos
    # Conectar a la BD
    def conectar(self):
        self.conexion = sqlite3.connect(self.nombre_bd)
        self.cursor = self.conexion.cursor()
        self.crear_tablas()

    # Desconectar la BD
    def desconectar(self):
        if self.conexion:
            self.conexion.close()
    
    # Método que crea las tablas en caso de que no existan
    def crear_tablas(self):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS ticker (
            ticker_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            fecha_desde DATETIME NOT NULL,
            fecha_hasta DATETIME NOT NULL
        );
        ''')

        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS precios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        self.conexion.commit()

    # Método que consultar las fechas sin info para un ticker dentro de un rango determinado y devuelve una lista de las mismas
    def consultar_fechas_faltantes(self,ticker,fecha_desde,fecha_hasta):
        self.cursor.execute(f'''
            SELECT 
                fecha_desde,
                fecha_hasta
            FROM ticker
            WHERE
                ticker = ?
            ORDER BY fecha_desde;
            ''',[ticker])
        rangos_existentes = self.cursor.fetchall()
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

    # Método para insertar nueva info en la BD
    def insertar_datos(self, datos, fecha_desde, fecha_hasta):
        self.cursor.execute(f'''
            INSERT INTO ticker (ticker, fecha_desde, fecha_hasta) VALUES
            ('{datos["ticker"]}', '{fecha_desde}', '{fecha_hasta}');
            ''')
        id = self.cursor.lastrowid
        self.conexion.commit()
        for item in datos["results"]:
            self.cursor.execute(f'''
                INSERT INTO precios (ticker_id, fecha, close, high, low, number, open, volumen, volumen_weighted) VALUES
                ({id}, '{item["t"]}', '{item["c"]}', '{item["h"]}', '{item["l"]}', '{item["n"]}', '{item["o"]}', '{item["v"]}', '{item["vw"]}');
                ''')
            self.conexion.commit()

    # Método para consultar los tickers guardados hasta el momento y sus rangos
    def consultar_resumen(self):
        df = pd.read_sql_query('''
            SELECT
                ticker,
                fecha_desde,
                fecha_hasta
            FROM ticker
            ORDER BY ticker, fecha_desde;
            ''', self.conexion)
        return df

    # Método para consultar los datos de un ticker y poder gráficar
    def consultar_datos(self, ticker):
        df_datos = pd.read_sql_query('''
            SELECT
                date(fecha/1000,'unixepoch') as fecha,
                close,
                high,
                low,
                number,
                open,
                volumen,
                volumen_weighted
            FROM precios p
            INNER JOIN ticker t ON p.ticker_id = t.ticker_id
            WHERE t.ticker = ?;
            ''', self.conexion, params=[ticker])
        
        df_datos['fecha'] = pd.to_datetime(df_datos['fecha'])
        
        resultados = self.cursor.execute(f'''
            SELECT
                MIN(fecha_desde),
                MAX(fecha_hasta)
            FROM ticker 
            WHERE ticker = ?;
            ''',[ticker])
        
        for row in resultados:
            min_fecha = row[0]
            max_fecha = row[1]
            cantidad_dias = (datetime.strptime(max_fecha,"%Y-%m-%d") - datetime.strptime(min_fecha,"%Y-%m-%d")).days + 1
            fechas = pd.date_range(min_fecha, periods=cantidad_dias)
            df_fechas = pd.DataFrame(fechas, columns=['fecha'], index=fechas)

        df = df_fechas.join(df_datos.set_index('fecha'), on='fecha')
        return df

    # Método que valida si existen datos de un ticker
    def validar_ticker(self, ticker):
        resultados = self.cursor.execute(f'''
            SELECT COUNT(*) AS Cantidad
            FROM ticker 
            WHERE ticker = ?;
            ''',[ticker])
        
        for row in resultados:
            if row[0] == 0:
                return False
            else:
                return True