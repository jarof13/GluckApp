import streamlit as st
from components.indicadores_dashboard import indicadores_dashboard
from components.graficos_dashboard    import graficas_ventas
from components.graficos_dashboard    import analisis_canal
from components.graficos_dashboard    import analisis_web


def generar_analisis(df_sales_data, df_campaign_data, df_web_analytics):

    # Indicadores
    st.title("Indicadores Clave")
    indicadores_dashboard(df_sales_data, df_campaign_data)
    st.markdown("<br>", unsafe_allow_html=True)

    # Graficos
    st.title("Análisis de las Ventas dado el Canal")
    canal = graficas_ventas(df_sales_data)

    # Analisis por canal
    analisis_canal(df_sales_data, canal)

    st.title("Relación y análisis entre Métricas de Campañas")
    st.subheader("Hipótesis sobre las Campañas")
    st.markdown("""
        1. **Saturación del Canal y Fatiga de Campañas**: Si el **CTR (Click-Through Rate)** disminuye mientras el **CPM (Costo por Mil Impresiones)** se mantiene constante o aumenta, podría estar ocurriendo una saturación del canal, lo que indica que el público objetivo ha perdido interés en los anuncios. Esto sugiere la necesidad de optimizar la segmentación o de probar otros canales.
        
        2. **Eficiencia del Gasto en Campañas (Spend vs Conversions)**: Si la **inversión (Spend)** está fuertemente correlacionada con las **conversiones**, se podría interpretar que las campañas están siendo eficientes y escalables. Sin embargo, una relación débil sugiere que el aumento de la inversión no está generando más conversiones, lo que podría ser indicativo de una estrategia de targeting o mensaje publicitario inadecuado.
        
        3. **Impacto del Budget en la Eficiencia de Campañas**: Si encontramos una baja correlación entre **Spend** y **CTR**, podría ser una señal de que la inversión no se está utilizando de manera eficiente, y que el presupuesto está siendo mal distribuido o no está siendo invertido en las campañas con mayor potencial de generar interacciones.
    """, unsafe_allow_html=True)

    # Analisis web
    analisis_web(df_campaign_data, df_web_analytics)