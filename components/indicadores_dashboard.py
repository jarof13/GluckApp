import streamlit as st
import pandas as pd
from   utils import *

def indicadores_dashboard(df_sales_data, df_campaign_data):


    # Unidades vendidas
    suma_total_sold = df_sales_data['Units Sold'].sum()

    if suma_total_sold % 1 == 0:
        # Es entero, sin decimales
            suma_total_sold_formateado = f"{int(suma_total_sold):,}".replace(",", ".")
    else:
        # Tiene decimales
            suma_total_sold_formateado = f"{suma_total_sold:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # Sección Ventas
    # Agrupar por categoría y sumar las unidades vendidas
    ventas_por_categoria = df_sales_data.groupby("Category")["Units Sold"].sum()

    # Obtener la categoría con más ventas
    categoria_top = ventas_por_categoria.idxmax()
    unidades_top = ventas_por_categoria.max()

    # Agrupar por categoría y sumar total revenue
    revenue_por_categoria = df_sales_data.groupby("Category")["Total Revenue"].sum()

    # Obtener la categoría con más ventas
    rev_top = revenue_por_categoria.idxmax()
    unidades_top_rev = revenue_por_categoria.max()


    unidades_top_formateado = (
        f"{int(unidades_top):,}".replace(",", ".")
        if unidades_top % 1 == 0
        else f"{unidades_top:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    unidades_top_rev_formateado = (
        f"{int(unidades_top_rev):,}".replace(",", ".")
        if unidades_top_rev % 1 == 0
        else f"{unidades_top_rev:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    #Sección Campaña
    # Agrupar por Medium y sumar el gasto (Spend)
    gasto_por_medio = df_campaign_data.groupby("Medium")["Spend"].sum()

    # Obtener el Medium con mayor gasto
    medium_mayor_gasto = gasto_por_medio.idxmax()
    gasto_max = gasto_por_medio.max()

    # Formatear el gasto si lo necesitás
    gasto_max_formateado = (
        f"{int(gasto_max):,}".replace(",", ".")
        if gasto_max % 1 == 0
        else f"{gasto_max:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    #Sección Empresa
    # Calcular la tasa de conversión
    df_campaign_data["Conversion_Rate"] = df_campaign_data["Conversions"] / df_campaign_data["Impressions"]

    # Obtener la mejor campaña
    conversion_por_medium = df_campaign_data.groupby("Medium")["Conversion_Rate"].mean().round(4)
    medium_top = conversion_por_medium.idxmax()
    cr_top     = conversion_por_medium.max()*100



    with st.container():
        col1, col2, col3, col4 = st.columns(4, border=True)
        
        with col1:
            st.subheader("Total de unidades vendidas", divider="gray")
            st.markdown(f"### **{suma_total_sold_formateado}**")
            st.markdown(f"#### Siendo la categoria más vendida **{categoria_top}** con **{unidades_top_formateado}** unidades")
        
        with col2:
            st.subheader("Top Revenue", divider="gray")
            st.markdown(f"### **{rev_top}**")
            st.markdown(f"#### El revenue para dicha categoria fue **${unidades_top_rev_formateado}**.")

        with col3:
            st.subheader("Gastos en Campañas", divider="gray")
            st.markdown(f"### Canal de campaña con mayor inversión **{medium_mayor_gasto}**")
            st.markdown(f"#### Invirtiendo un total de **${gasto_max_formateado}**.")

        with col4:
            st.subheader("Mejor medio publicitario", divider="gray")
            st.markdown(f"### **{medium_top}**")
            st.markdown(f"#### Tasa de coversión: **{cr_top}%**.")