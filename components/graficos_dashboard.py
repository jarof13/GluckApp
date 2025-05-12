import streamlit      as st
import pandas         as pd
import plotly.express as px
import seaborn        as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from   datetime import datetime, timedelta
from   utils import *


def graficas_ventas(df_sales_data):
    st.subheader("Visualización de Ventas")

    category_colors = {
    "Home": "#1f77b4",
    "Beauty": "#ff7f0e",
    "Apparel": "#2ca02c",
    "Sports": "#d62728",
    "Electronics": "#9467bd"
}

  # Filtro de canal único
    canales_disponibles = df_sales_data['Channel'].unique().tolist()
    st.markdown("##### Selecciona un canal a visualizar:")
    canal_seleccionado = st.radio("", canales_disponibles, horizontal=True)


    # -------- Gráfico 1: Unidades vendidas por categoría y canal a lo largo del tiempo --------
    agg_units = df_sales_data.groupby(['Date', 'Category', 'Channel']).agg(
        Units=('Units Sold', 'sum')
    ).reset_index()

    df_filtrado = agg_units[agg_units["Channel"] == canal_seleccionado]

    fig = px.line(
        df_filtrado,
        x='Date',
        y='Units',
        color='Category',
        title=f"Unidades vendidas por Categoría - Canal: {canal_seleccionado}",
        color_discrete_map=category_colors,
        markers=True
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        legend_title="Categoría",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.1,
            xanchor="left",
            x=0.5,
            title=None
        ),
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------- Gráfico 2: Revenue total por categoría y canal --------
    agg_revenue = df_sales_data.groupby(["Channel", "Category"]).agg(
        Revenue=("Total Revenue", "sum")
    ).reset_index()
    
    agg_revenue = agg_revenue.sort_values(by=["Channel", "Revenue"], 
                            ascending=[True, True]) 

    df_filtrado = agg_revenue[agg_revenue["Channel"] == canal_seleccionado]

    fig = px.bar(
        df_filtrado,
        x="Channel",
        y="Revenue",
        color="Category",
        title=f"Revenue Total por Categoría - Canal: {canal_seleccionado}",
        barmode="group",
        color_discrete_map=category_colors
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        legend_title="",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    return canal_seleccionado


def analisis_canal(df_sales_data, canal_seleccionado):
    st.subheader("Análisis Detallado por Canal")

    df_filtrado = df_sales_data[df_sales_data["Channel"] == canal_seleccionado]

    resumen = df_filtrado.groupby("Category").agg(
        Total_Unidades=('Units Sold', 'sum'),
        Total_Revenue=('Total Revenue', 'sum'),
        Ultima_Fecha=('Date', 'max'),
        Promedio_Unidades_Diarias=('Units Sold', 'mean')
    ).reset_index()

    resumen.columns = [
            "Categoría", 
            "Total Unidades", 
            "Total Revenue", 
            "Ultima Fecha", 
            "Promedio Unidades Diarias"
        ]
    
    # Formatear números con punto como separador de miles y coma como separador decimal
    resumen["Total Unidades"] = resumen["Total Unidades"].astype(int).map(lambda x: f"{x:,}".replace(",", "."))
    resumen["Total Revenue"] = resumen["Total Revenue"].map(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    resumen["Promedio Unidades Diarias"] = resumen["Promedio Unidades Diarias"].map(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    resumen["Ultima Fecha"] = pd.to_datetime(resumen["Ultima Fecha"]).dt.strftime("%d/%m/%Y")

    st.markdown("##### Métricas por Categoría")
    st.dataframe(resumen.sort_values("Total Unidades", ascending=False), use_container_width=True, hide_index=True)

    # Agrupar por mes y categoría
    df_filtrado["Mes"] = df_filtrado["Date"].dt.to_period("M")
    ventas_mensuales = df_filtrado.groupby(["Mes", "Category"])["Units Sold"].sum().reset_index()

    # Convertir a datetime para ordenar
    ventas_mensuales["Mes"] = ventas_mensuales["Mes"].dt.to_timestamp()

    # Obtener meses ordenados
    meses_ordenados = ventas_mensuales["Mes"].sort_values().unique()

    # Definir primeros y últimos 3 meses del dataset
    primeros_3 = meses_ordenados[:3]
    ultimos_3 = meses_ordenados[-3:]

    # Calcular promedios de ventas para cada grupo de meses
    ventas_inicio = ventas_mensuales[ventas_mensuales["Mes"].isin(primeros_3)].groupby("Category")["Units Sold"].mean()
    ventas_final = ventas_mensuales[ventas_mensuales["Mes"].isin(ultimos_3)].groupby("Category")["Units Sold"].mean()

    # Calcular variación porcentual
    variacion_total = ((ventas_final - ventas_inicio) / ventas_inicio.replace(0, pd.NA)) * 100

    # Categoría con mayor caída
    categoria_mayor_caida = variacion_total.idxmin()
    valor_mayor_caida = variacion_total.min()


    # Categoría con la última venta más antigua
    ultima_fecha_cat = df_filtrado.groupby("Category")["Date"].max()
    categoria_inactiva = ultima_fecha_cat.idxmin()
    fecha_inactiva = ultima_fecha_cat.min().strftime("%d/%m/%Y")

    # Categoría con mayor crecimiento
    categoria_crecimiento = variacion_total.idxmax()
    valor_crecimiento = variacion_total.max()

    # Frecuencia de compra promedio
    frecuencia_prom = df_filtrado.sort_values("Date")["Date"].diff().dt.days.dropna().mean()

    # Mostrar métricas
    st.markdown("##### Métricas Clave (Análisis Temporal y Tendencias)")

    st.markdown("""
                    <style>
                        .metric-container {
                            padding: 1rem;
                            border: 1px solid #ddd;
                            border-radius: 10px;
                            background-color: #f9f9f9;
                            margin-bottom: 1rem;
                        }
                        .metric-title {
                            font-size: 1.2rem;
                            font-weight: bold;
                            margin-bottom: 0.5rem;
                        }
                    </style>
                """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        render_custom_metric("Mayor caída en ventas", f"{categoria_mayor_caida} ({valor_mayor_caida:.1f}%)", "📉")
        render_custom_metric("Última venta antigua", f"{categoria_inactiva} ({fecha_inactiva})", "📅")

    with col2:
        render_custom_metric("Mayor crecimiento", f"{categoria_crecimiento} (+{valor_crecimiento:.1f}%)", "📈")
        render_custom_metric("Frecuencia de venta", f"{frecuencia_prom:.1f} días", "🔁")


def analisis_web(df_campaign_data, df_web_analytics):


    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Relación entre CTR y Costo por Mil (CPM) según Medio Publicitario")
        fig_ctr_cpm = px.scatter(
            df_campaign_data,
            x="CPM",
            y="CTR",
            color="Medium",
            hover_data=["Campaign ID"],
            labels={"CPM": "Costo por Mil Impresiones (CPM)", "CTR": "Ratio de Clicks (CTR)"},
            template="simple_white"
        )
        fig_ctr_cpm.update_traces(marker=dict(size=8, opacity=0.6))
        fig_ctr_cpm.update_layout(height=400, 
                                  legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.1,
                                        xanchor="left",
                                        x=0.5,
                                        title=None
                                    ),
                                xaxis_title_font=dict(size=18),
                                yaxis_title_font=dict(size=18))
        st.plotly_chart(fig_ctr_cpm, use_container_width=True)

    with col2:
        st.markdown("#### Eficiencia del Gasto Publicitario: Inversión vs Conversiones por Medio")
        fig_spend_conv = px.scatter(
            df_campaign_data,
            x="Spend",
            y="Conversions",
            color="Medium",
            hover_data=["Campaign ID"],
            labels={"Spend": "Gasto", "Conversions": "Conversiones"},
            template="simple_white"
        )
        fig_spend_conv.update_traces(marker=dict(size=8, opacity=0.6))
        fig_spend_conv.update_layout(height=400, 
                                     legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.1,
                                        xanchor="left",
                                        x=0.5,
                                        title=None
                                    ),
                                     xaxis_title_font=dict(size=18),
                                     yaxis_title_font=dict(size=18))
        st.plotly_chart(fig_spend_conv, use_container_width=True)


    st.subheader("Matriz de Correlación")

    # Filtro para el 'Medium' utilizando radio button
    medios_disponibles = df_campaign_data['Medium'].unique().tolist()
    medios_disponibles = ['All'] + medios_disponibles  
    st.markdown("##### Selecciona un Medio de Publicidad a analizar:")
    medio_seleccionado = st.radio("", 
                                  medios_disponibles, horizontal=True)

    # Filtrar el DataFrame según el medio seleccionado
    if medio_seleccionado != 'All':
        df_filtrado = df_campaign_data[df_campaign_data['Medium'] == medio_seleccionado]
    else:
        df_filtrado = df_campaign_data

    # Calcular la correlación entre las variables de interés
    variables_de_interes = ['CTR', 'CPM', 'Spend', 'Conversions']
    correlation_matrix = df_filtrado[variables_de_interes].corr().round(3)

    # Crear heatmap con texto y estilos
    fig = px.imshow(
        correlation_matrix,
        text_auto=".3f",
        color_continuous_scale='RdBu',
        aspect="auto",
        zmin=-1, zmax=1,
    )

    # Aumentar el tamaño de las etiquetas
    fig.update_layout(
        font=dict(size=16),  # tamaño de los textos
        xaxis=dict(tickfont=dict(size=16), title=""),
        yaxis=dict(tickfont=dict(size=16), title=""),
        margin=dict(t=30, l=30, r=30, b=30)
    )

    # Mostrar en Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("##### Análisis de Correlaciones Significativas")

    # Estilo visual para las métricas personalizadas
    st.markdown("""
        <style>
            .metric-container {
                padding: 1rem;
                border: 1px solid #ddd;
                border-radius: 10px;
                background-color: #f9f9f9;
                margin-bottom: 1rem;
            }
            .metric-title {
                font-size: 1.2rem;
                font-weight: bold;
                margin-bottom: 0.5rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # Extraer correlaciones específicas
    cor_ctrcpm = correlation_matrix.loc["CTR", "CPM"]
    cor_spconv = correlation_matrix.loc["Spend", "Conversions"]

    col1, col2 = st.columns(2)

    with col1:
        render_custom_metric(
            "Relación CTR y CPM",
            f"Coeficiente de correlación: {cor_ctrcpm:.3f}. "
            + ("Esto sugiere que cuando el costo por visibilidad aumenta, la tasa de clics tiende a disminuir, lo que podría indicar menor eficiencia publicitaria."
               if cor_ctrcpm < 0 else "Indica que a mayor inversión en visibilidad (CPM), también se observa una mayor tasa de clics, posiblemente reflejando mejor segmentación o contenido."),
            "📊"
        )

    with col2:
        render_custom_metric(
            "Relación Spend y Conversions",
            f"Coeficiente de correlación: {cor_spconv:.3f}. "
            + ("Esto sugiere que al aumentar la inversión, también se incrementan las conversiones, lo cual es señal de una campaña efectiva y escalable." 
               if cor_spconv > 0.5 else "Esto indica que el aumento de inversión no garantiza más conversiones, lo que podría reflejar problemas en el targeting o en el mensaje de la campaña."),
            "💸"
        )
    
    st.markdown("##### Medios según la Calidad de sus Correlaciones")

    st.markdown("""
                        <style>
                            .expander .streamlit-expanderHeader {
                                font-size: 4.5rem !important;  /* Título del expander */
                                font-weight: bold;
                            }
                            .expander .streamlit-expanderContent {
                                font-size: 4.5rem !important;  /* Texto dentro del expander */
                            }
                        </style>
                    """, unsafe_allow_html=True)


    # Recalcular correlaciones por medio
    buenos_medios = []
    malos_medios = []

    for medio in df_campaign_data['Medium'].unique():
        df_m = df_campaign_data[df_campaign_data['Medium'] == medio]
        corr_m = df_m[variables_de_interes].corr()
        
        cor_ctrcpm = corr_m.loc["CTR", "CPM"]
        cor_spconv = corr_m.loc["Spend", "Conversions"]
        
        if cor_ctrcpm > 0.05 and cor_spconv > 0.5:
            buenos_medios.append((medio, cor_ctrcpm, cor_spconv))
        else:
            malos_medios.append((medio, cor_ctrcpm, cor_spconv))

    # Mostrar en dos columnas
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("📈 Medios con Buen Desempeño"):
            st.markdown("""
                <div class="metric-container">
                    <div class="metric-title">📈 Medios con Buen Desempeño</div>
            """, unsafe_allow_html=True)

            if buenos_medios:
                for medio, c1, c2 in buenos_medios:
                    render_custom_metric(
                        f"{medio}  CTR vs CPM: {c1:.3f}, Spend vs Conversions: {c2:.3f}",
                        f"Recomendación: Considera incrementar inversión en este medio o duplicar campañas similares, ya que muestra señales claras de eficiencia y retorno.",
                        "📈"
                    )
            else:
                render_custom_metric("No se identificaron medios con buen desempeño en ambas métricas clave.", "", "⚠️")

            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        with st.expander("📈 Medios con Buen Desempeño"):
            st.markdown("""
                <div class="metric-container">
                    <div class="metric-title">⚠️ Medios con mal desempeño</div>
            """, unsafe_allow_html=True)

            if malos_medios:
                for medio, c1, c2 in malos_medios:
                    render_custom_metric(
                        f"{medio}  CTR vs CPM: {c1:.3f}, Spend vs Conversions: {c2:.3f}",
                        f"Sugerencia: Revisa la segmentación, creatividad o el objetivo de conversión. Podría no estar llegando al público correcto o no estar alineado con su intención.",
                        "⚠️"
                    )
            else:
                render_custom_metric("Todos los medios presentan métricas aceptables.", "", "✔️")

            st.markdown("</div>", unsafe_allow_html=True)

