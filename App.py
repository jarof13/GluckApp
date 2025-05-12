import  streamlit as st
from    PIL import Image
import  pandas as pd
import  numpy  as np
import  plotly.express as px
from    utils import *
from    sections.estadisticas   import generar_analisis

# Configuración de la página
st.set_page_config(page_title="Análisis de Ventas y Mercadeo Web Cervezas Glurk", layout="wide")

# Título centrado
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        color: #2c3e50;
    }
    </style>
    <div class="title">
        Gluck Reportes Web
    </div>
    """,
    unsafe_allow_html=True
)

# Menú de navegación en la barra lateral
menu = st.sidebar.selectbox(
    "Navega por la app:",
    ("Inicio", "Análisis web y de las ventas"),
    index=0,
)

# Inicializar data_df en session_state si no existe
if "data_df" not in st.session_state:
    st.session_state["data_df"] = None

# Mostrar contenido según la opción seleccionada
if menu == "Inicio":
    st.header("Reportes de las ventas y las campañas web")
    st.subheader("Una vez cargada la data a procesar usa el menú lateral para navegar en las distintas funcionabilidades")
    
    st.header("Carga de Archivo Excel")
    uploaded_file = st.file_uploader("Sube un archivo Excel:", type=["xlsx"])
    
    if uploaded_file:
        try:
            st.session_state["data_df"] = procesar_archivo_excel(uploaded_file)
            st.success("Archivo cargado correctamente.")
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
            st.session_state["data_df"] = None

elif menu == "Análisis web y de las ventas":
    data_df = st.session_state.get("data_df", None)
    if data_df is not None and "sales_data" in data_df:
        # Lectura
        df_sales_data = data_df["sales_data"]
        df_sales_data["Total Revenue"] = df_sales_data["Unit Revenue"] * df_sales_data["Units Sold"]
        df_campaign_data = data_df["campaign_data"]
        df_campaign_data["Conversion_Rate"] = df_campaign_data["Conversions"] / df_campaign_data["Impressions"]
        df_web_analytics = data_df["web_analytics"]

        # 
        generar_analisis(df_sales_data, df_campaign_data, df_web_analytics)
    else:
        st.warning("Primero debes cargar un archivo válido en la sección 'Inicio'.")