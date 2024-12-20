from app import App
from api import Api

# Main de la aplicacion
if __name__ == "__main__":
    app = App()
    app.validar_credentials(streamlit=None)
    app.api = Api(app.key)
    app.main()