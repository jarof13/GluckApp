import pandas         as pd
import numpy          as np 
import plotly.express as px
import streamlit      as st



def procesar_archivo_excel(uploaded_file:str) -> pd.DataFrame:
    """
    Lee el archivo Excel y crea dataframes accesibles para cada pestaña.

    Args:
        uploaded_file: Archivo Excel subido por el usuario.

    Returns:
        dict: Un diccionario con las hojas del archivo Excel, donde las claves son los nombres
              de las hojas (en minúsculas y sin espacios) y los valores son los DataFrames correspondientes.
    """
    try:
        # Cargar todas las hojas del archivo Excel
        sheets = pd.read_excel(uploaded_file, sheet_name=None)
        
        dataframes = {}

        for sheet_name, df in sheets.items():
            table_name = sheet_name.lower().replace(" ", "_")
            dataframes[table_name] = df  
        
        return dataframes
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return None
    

def render_custom_metric(titulo, valor, emoji=""):
    st.markdown(f"""
        <div style="
            padding: 1rem;
            border: 1px solid #ddd;
            border-radius: 10px;
            background-color: #f9f9f9;
            margin-bottom: 1rem;
            text-align: center;
        ">
            <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;">{emoji} {titulo}</div>
            <div style="font-size: 1.5rem; color: #333;">{valor}</div>
        </div>
    """, unsafe_allow_html=True)