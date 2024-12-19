import requests

# Clase para interactuar con la API de polygon.io
class Api:
    # Constructor
    def __init__(self, api_key):
        self.api_key = api_key
    
    # Método que consulta la api y devuelve un diccionario con la respuesta
    def consultar_datos(self, ticker, fecha_desde, fecha_hasta):
        try:
            response = requests.get(f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{fecha_desde}/{fecha_hasta}?adjusted=true&sort=asc&apiKey={self.api_key}')
            response.raise_for_status()
            diccionario = dict(response.json())
            return diccionario
        except requests.exceptions.RequestException as e:
            print(f"\nError al consultar la API: {e}")
            return None