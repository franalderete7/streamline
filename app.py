# app.py - Main Streamlit Application
import streamlit as st
import pandas as pd

# Import modular components
from styles import get_css_styles
from cash_flow_calculator import CashFlowCalculator
from chart_generator import ChartGenerator
from ui_components import UIComponents

# Page configuration
st.set_page_config(page_title="Flujo de Caja Inmobiliario", layout="wide")

# Apply custom styles with dark theme using the correct method
st.markdown(f"<style>{get_css_styles()}</style>", unsafe_allow_html=True)

# Main title
st.title("Flujo de Caja - Proyecto Inmobiliario")

# Render sidebar and get input parameters
inputs = UIComponents.render_sidebar()

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = CashFlowCalculator.generar_flujo_caja(
        inputs['inversion_inicial'], 
        inputs['gasto_construccion_mensual'], 
        inputs['comision_por_venta'], 
        inputs['precio_por_duplex'],
        inputs['num_cuotas'], 
        inputs['duplex_por_etapa'], 
        inputs['meses_por_etapa'],
        inputs['total_etapas'], 
        inputs['tasa_ventas'], 
        inputs['tea_costo_oportunidad']
    )

# Recalculate when button is clicked
if inputs['recalcular']:
    st.session_state.df = CashFlowCalculator.generar_flujo_caja(
        inputs['inversion_inicial'], 
        inputs['gasto_construccion_mensual'], 
        inputs['comision_por_venta'], 
        inputs['precio_por_duplex'],
        inputs['num_cuotas'], 
        inputs['duplex_por_etapa'], 
        inputs['meses_por_etapa'],
        inputs['total_etapas'], 
        inputs['tasa_ventas'], 
        inputs['tea_costo_oportunidad']
    )

# Get current DataFrame
df = st.session_state.df

# Calculate financial metrics
metricas = CashFlowCalculator.calcular_metricas_financieras(df, inputs['tea_costo_oportunidad'])

# Render data table
UIComponents.render_data_table(df)

# Render financial summary
UIComponents.render_financial_summary(metricas, inputs['tea_costo_oportunidad'])

# Render chart
st.subheader("Gráfico de Flujo de Caja")
fig = ChartGenerator.create_cash_flow_chart(df, inputs['tea_costo_oportunidad'])
st.plotly_chart(fig, use_container_width=True)

# Render download section
UIComponents.render_download_section(df)