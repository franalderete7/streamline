# ui_components.py
import streamlit as st
from typing import Dict, Any

class UIComponents:
    """
    Handles all UI components and interface logic
    """
    
    @staticmethod
    def render_sidebar() -> Dict[str, Any]:
        """
        Render the sidebar with all input parameters
        
        Returns:
            Dict with all input values
        """
        st.sidebar.header("Parámetros del Proyecto")
        
        # Investment parameters
        st.sidebar.subheader("Inversión")
        inversion_inicial = st.sidebar.number_input("Inversión Inicial (USD)", value=850000.0, step=10000.0, min_value=0.0)
        gasto_construccion_mensual = st.sidebar.number_input("Gasto Construcción Mensual (USD)", value=52888.0, step=1000.0, min_value=0.0)
        
        # Sales parameters
        st.sidebar.subheader("Ventas")
        comision_por_venta = st.sidebar.number_input("Comisión por Venta (USD)", value=2000.0, step=100.0, min_value=0.0)
        precio_por_duplex = st.sidebar.number_input("Precio por Dúplex (USD)", value=130000.0, step=1000.0, min_value=0.0)
        num_cuotas = st.sidebar.number_input("Número de Cuotas por Dúplex", value=20, step=1, min_value=1)
        
        # Project structure
        st.sidebar.subheader("Estructura del Proyecto")
        duplex_por_etapa = st.sidebar.number_input("Dúplex por Etapa", value=11, step=1, min_value=1)
        meses_por_etapa = st.sidebar.number_input("Meses por Etapa", value=15, step=1, min_value=1)
        total_etapas = st.sidebar.number_input("Total Etapas", value=3, step=1, min_value=1)
        
        # Financial parameters
        st.sidebar.subheader("Parámetros Financieros")
        tasa_ventas = st.sidebar.number_input("Tasa de Ventas (Dúplex por Mes)", value=1.0, step=0.1, min_value=0.1)
        tea_costo_oportunidad = st.sidebar.number_input("TEA Costo de Oportunidad (%)", value=5.12, step=0.1, min_value=0.0) / 100
        
        # Calculate button
        recalcular = st.sidebar.button("Recalcular Tabla")
        
        return {
            'inversion_inicial': inversion_inicial,
            'gasto_construccion_mensual': gasto_construccion_mensual,
            'comision_por_venta': comision_por_venta,
            'precio_por_duplex': precio_por_duplex,
            'num_cuotas': num_cuotas,
            'duplex_por_etapa': duplex_por_etapa,
            'meses_por_etapa': meses_por_etapa,
            'total_etapas': total_etapas,
            'tasa_ventas': tasa_ventas,
            'tea_costo_oportunidad': tea_costo_oportunidad,
            'recalcular': recalcular
        }
    
    @staticmethod
    def render_data_table(df):
        """
        Render the data table with proper formatting
        
        Args:
            df: DataFrame to display
        """
        st.subheader("Tabla de Flujo de Caja")
        st.dataframe(df.style.format({
            "Gastos Construcción (USD)": "{:,.2f}",
            "Gastos Comisiones (USD)": "{:,.2f}",
            "Ingresos por Cuotas (USD)": "{:,.2f}",
            "Saldo Neto Mensual (USD)": "{:,.2f}",
            "Ingresos Acumulados (USD)": "{:,.2f}",
            "Acumulado (USD)": "{:,.2f}",
            "Capital Invertido (USD)": "{:,.2f}",
            f"Costo de Oportunidad Mensual (USD, TEA {df.columns[-1].split('TEA ')[1].split('%')[0]}% Depósito USD)": "{:,.2f}"
        }), use_container_width=True)
    
    @staticmethod
    def render_financial_summary(metricas: Dict[str, Any], tea_costo_oportunidad: float):
        """
        Render the financial summary section
        
        Args:
            metricas: Financial metrics dictionary
            tea_costo_oportunidad: Opportunity cost rate
        """
        st.subheader("Resumen Financiero", anchor="summary")
        st.markdown("""
        <div class="summary-box">
            <p><b>Ingresos Totales:</b> USD {:,.2f}</p>
            <p><b>Gastos Totales:</b> USD {:,.2f}</p>
            <p><b>Ganancia Neta:</b> USD {:,.2f}</p>
            <p><b>Costo de Oportunidad Total (TEA {:.2f}%):</b> USD {:,.2f}</p>
            <p><b>Mes de Recuperación de Inversión:</b> Mes {}</p>
        </div>
        """.format(
            metricas['total_ingresos'], 
            metricas['total_gastos'], 
            metricas['ganancia_neta'], 
            tea_costo_oportunidad * 100, 
            metricas['costo_oportunidad_total'], 
            metricas['mes_recuperacion']
        ), unsafe_allow_html=True)
    
    @staticmethod
    def render_download_section(df):
        """
        Render the download section
        
        Args:
            df: DataFrame to download
        """
        st.subheader("Descargar Tabla")
        col1, col2 = st.columns(2)
        
        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="Descargar CSV", 
                data=csv, 
                file_name="flujo_de_caja_modificado.csv", 
                mime="text/csv"
            )
        
        with col2:
            from io import BytesIO
            import pandas as pd
            output = BytesIO()
            df.to_excel(output, index=False, engine="openpyxl")
            st.download_button(
                label="Descargar Excel", 
                data=output.getvalue(), 
                file_name="flujo_de_caja_modificado.xlsx", 
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ) 