from app import App
from streamlit_app import StreamlitApp

# Main de la aplicacion
if __name__ == "__main__":
    app = App()
    streamlit_app = StreamlitApp(app)
    streamlit_app.run()