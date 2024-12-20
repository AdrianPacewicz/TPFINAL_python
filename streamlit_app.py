import streamlit as st
from base_de_datos import BaseDeDatos
from api import Api
from app import App
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

class StreamlitApp:
    def __init__(self, app):
        self.app = app

    def run(self):
        self.app.validar_credentials(st)
        self.app.api = Api(self.app.key)
        st.title("TP Final - ITBA - Curso Python")

        col1, col2, col3 = st.columns(3)

        # Sección para actualizar datos
        with col1:
            st.header("Actualización de datos")
            ticker = st.text_input("Ingrese el ticker", value="AAPL")
            fecha_desde = st.date_input("Fecha desde")
            fecha_hasta = st.date_input("Fecha hasta")

            if st.button("Actualizar datos"):
                try:
                    if self.app.actualizar_datos(ticker, fecha_desde.strftime("%Y-%m-%d"), fecha_hasta.strftime("%Y-%m-%d")):
                        st.success("Datos insertados correctamente.")
                    else:
                        st.error("No se encontraron datos para el ticker y las fechas seleccionadas.")
                except ValueError as e:
                    st.error(str(e))

        # Sección para visualizar el resumen
        with col2:
            st.header("Resumen de datos guardados")
            resumen_df = self.app.visualizar_resumen()
            st.dataframe(resumen_df,use_container_width=True,hide_index=True)

        # Sección para visualizar el gráfico
        with col3:
            st.header("Visualización de gráficos")
            ticker_grafico = st.selectbox("Seleccione el ticker para el gráfico", resumen_df["ticker"].unique())
            tipo_grafico = st.radio("Seleccione el tipo de gráfico", ["Comparativo", "Barras"])

            if st.button("Generar gráfico"):
                df = self.app.visualizar_grafico(ticker_grafico)

                if tipo_grafico == "Comparativo":
                    fig, ax = plt.subplots()
                    ax.plot(df["fecha"], df["close"], label="Close", color='blue', markersize=5, marker='.')
                    ax.plot(df["fecha"], df["high"], label="High", color='green', markersize=5, marker='.')
                    ax.plot(df["fecha"], df["low"], label="Low", color='red', markersize=5, marker='.')
                    ax.plot(df["fecha"], df["open"], label="Open", color='yellow', markersize=5, marker='.')
                    ax.set_xlabel('Fecha')
                    ax.set_ylabel('Valor')
                    ax.grid(True)
                    ax.set_title('Gráfico Comparativo')
                    ax.legend()
                    st.pyplot(fig)  # Mostrar el gráfico con Streamlit

                elif tipo_grafico == "Barras":
                    fig, axs = plt.subplots(2, 2)
                    axs[0, 0].bar(df["fecha"], df["close"], label="Close", color='blue')
                    axs[0, 0].set_title("Close")
                    axs[0, 1].bar(df["fecha"], df["high"], label="High", color='green')
                    axs[0, 1].set_title("High")
                    axs[1, 0].bar(df["fecha"], df["low"], label="Low", color='red')
                    axs[1, 0].set_title("Low")
                    axs[1, 1].bar(df["fecha"], df["open"], label="Open", color='yellow')
                    axs[1, 1].set_title("Open")
                    st.pyplot(fig)  # Mostrar el gráfico con Streamlit