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
        st.sidebar.header("🏗️ Parámetros del Proyecto")
        
        # Land costs
        st.sidebar.subheader("🌍 Costos del Terreno")
        costo_terreno = st.sidebar.number_input("💰 Costo del Terreno (USD)", value=600000.0, step=10000.0, min_value=0.0)
        gastos_compra_terreno = st.sidebar.number_input("📋 Gastos Compra Terreno (USD)", value=20000.0, step=1000.0, min_value=0.0)
        
        # Calculate total land cost
        total_costo_terreno = costo_terreno + gastos_compra_terreno
        st.sidebar.info(f"🏠 **Total Costo del Terreno:** ${total_costo_terreno:,.0f}")
        
        # Pre-construction costs
        st.sidebar.subheader("🔧 Gastos Antes de Comenzar Obra")
        proyecto = st.sidebar.number_input("📊 Proyecto (USD)", value=10000.0, step=1000.0, min_value=0.0)
        cerramiento_mamposteria = st.sidebar.number_input("🧱 Cerramiento Mampostería (USD)", value=60000.0, step=1000.0, min_value=0.0)
        movimiento_suelo = st.sidebar.number_input("🚜 Movimiento de Suelo (USD)", value=80000.0, step=1000.0, min_value=0.0)
        varios = st.sidebar.number_input("🔩 Varios (USD)", value=20000.0, step=1000.0, min_value=0.0)
        
        # Calculate total pre-construction costs
        gastos_varios_antes_obra = proyecto + cerramiento_mamposteria + movimiento_suelo + varios
        st.sidebar.info(f"🔧 **Gastos Varios Antes Comenzar Obra:** ${gastos_varios_antes_obra:,.0f}")
        
        # Calculate total initial investment
        inversion_inicial = total_costo_terreno + gastos_varios_antes_obra
        st.sidebar.success(f"💼 **Inversión Inicial Total:** ${inversion_inicial:,.0f}")
        
        st.sidebar.divider()
        
        # Construction parameters
        st.sidebar.subheader("🏗️ Construcción")
        superficie_promedio_duplex = st.sidebar.number_input("📐 Superficie Promedio Dúplex (M²)", value=90.4, step=0.1, min_value=0.1)
        costo_construccion_por_m2 = st.sidebar.number_input("💰 Costo Construcción por M² (USD)", value=1100.0, step=10.0, min_value=0.0)
        
        st.sidebar.divider()
        
        # Sales parameters
        st.sidebar.subheader("💰 Ventas")
        comision_por_venta = st.sidebar.number_input("🤝 Comisión por Venta (USD)", value=2000.0, step=100.0, min_value=0.0)
        precio_por_duplex = st.sidebar.number_input("🏠 Precio por Dúplex (USD)", value=140000.0, step=1000.0, min_value=0.0)
        
        # Payment structure
        st.sidebar.write("**💳 Estructura de Pago:**")
        porcentaje_down_payment = st.sidebar.number_input("💰 Down Payment (%)", value=40.0, step=1.0, min_value=0.0, max_value=100.0)
        num_cuotas_restantes = st.sidebar.number_input("📅 Cuotas Restantes", value=10, step=1, min_value=1)
        
        # Calculate payment amounts
        down_payment_amount = precio_por_duplex * (porcentaje_down_payment / 100)
        remaining_amount = precio_por_duplex - down_payment_amount
        cuota_restante_mensual = remaining_amount / num_cuotas_restantes if num_cuotas_restantes > 0 else 0
        
        st.sidebar.info(f"💰 **Down Payment:** ${down_payment_amount:,.0f} ({porcentaje_down_payment}%)")
        st.sidebar.info(f"📊 **Monto Restante:** ${remaining_amount:,.0f}")
        st.sidebar.info(f"💳 **Cuota Mensual Restante:** ${cuota_restante_mensual:,.0f}")
        
        # Keep legacy num_cuotas for compatibility (total payment period)
        num_cuotas = num_cuotas_restantes
        
        st.sidebar.divider()
        
        # Project structure
        st.sidebar.subheader("📋 Estructura del Proyecto")
        duplex_por_etapa = st.sidebar.number_input("🏘️ Dúplex por Etapa", value=11, step=1, min_value=1)
        meses_por_etapa = st.sidebar.number_input("⏱️ Meses por Etapa", value=15, step=1, min_value=1)
        total_etapas = st.sidebar.number_input("📊 Total Etapas", value=3, step=1, min_value=1)
        
        # Calculate total duplexes
        total_duplex = duplex_por_etapa * total_etapas
        st.sidebar.info(f"🏠 **Total Dúplex:** {total_duplex} unidades")
        
        # Calculate monthly construction expense based on construction parameters
        total_meses_construccion = meses_por_etapa * total_etapas
        promedio_duplex_por_mes = total_duplex / total_meses_construccion if total_meses_construccion > 0 else 0
        gasto_construccion_mensual = superficie_promedio_duplex * costo_construccion_por_m2 * promedio_duplex_por_mes
        
        st.sidebar.info(f"📊 **Promedio Dúplex/Mes:** {promedio_duplex_por_mes:.2f}")
        st.sidebar.success(f"🔨 **Gasto Construcción Mensual:** ${gasto_construccion_mensual:,.0f}")
        
        st.sidebar.divider()
        
        # Financial parameters
        st.sidebar.subheader("📈 Parámetros Financieros")
        tasa_ventas = st.sidebar.number_input("🎯 Tasa de Ventas (Dúplex por Mes)", value=0.5, step=0.1, min_value=0.1)
        tea_costo_oportunidad = st.sidebar.number_input("💹 TEA Costo de Oportunidad (%)", value=5.12, step=0.1, min_value=0.0) / 100
        
        st.sidebar.divider()
        
        # Calculate button
        recalcular = st.sidebar.button("🔄 Recalcular Tabla", type="primary")
        
        # Summary section
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Resumen Rápido")
        ingreso_potencial = precio_por_duplex * total_duplex
        costo_comisiones_total = comision_por_venta * total_duplex
        st.sidebar.markdown(f"""
        **💰 Inversión Total:** ${inversion_inicial:,.0f}  
        **🌍 Costo Terreno:** ${total_costo_terreno:,.0f}  
        **🔧 Gastos Pre-Obra:** ${gastos_varios_antes_obra:,.0f}  
        **🏠 Total Dúplex:** {total_duplex}  
        **🔨 Gasto Construcción/Mes:** ${gasto_construccion_mensual:,.0f}  
        **🤝 Costo Total Comisiones:** ${costo_comisiones_total:,.0f}  
        **💸 Ingreso Potencial:** ${ingreso_potencial:,.0f}  
        **🎯 Tasa Ventas:** {tasa_ventas}/mes  
        """)
        
        return {
            # Land costs
            'costo_terreno': costo_terreno,
            'gastos_compra_terreno': gastos_compra_terreno,
            'total_costo_terreno': total_costo_terreno,
            
            # Pre-construction costs
            'proyecto': proyecto,
            'cerramiento_mamposteria': cerramiento_mamposteria,
            'movimiento_suelo': movimiento_suelo,
            'varios': varios,
            'gastos_varios_antes_obra': gastos_varios_antes_obra,
            
            # Total investment
            'inversion_inicial': inversion_inicial,
            
            # Construction parameters
            'superficie_promedio_duplex': superficie_promedio_duplex,
            'costo_construccion_por_m2': costo_construccion_por_m2,
            'total_meses_construccion': total_meses_construccion,
            'promedio_duplex_por_mes': promedio_duplex_por_mes,
            'gasto_construccion_mensual': gasto_construccion_mensual,
            
            # Sales and payment structure
            'comision_por_venta': comision_por_venta,
            'precio_por_duplex': precio_por_duplex,
            'porcentaje_down_payment': porcentaje_down_payment,
            'num_cuotas_restantes': num_cuotas_restantes,
            'down_payment_amount': down_payment_amount,
            'remaining_amount': remaining_amount,
            'cuota_restante_mensual': cuota_restante_mensual,
            'num_cuotas': num_cuotas,
            'costo_comisiones_total': costo_comisiones_total,
            
            # Project structure
            'duplex_por_etapa': duplex_por_etapa,
            'meses_por_etapa': meses_por_etapa,
            'total_etapas': total_etapas,
            'total_duplex': total_duplex,
            
            # Financial parameters
            'tasa_ventas': tasa_ventas,
            'tea_costo_oportunidad': tea_costo_oportunidad,
            
            # UI controls
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
        
        # Format columns with proper numeric formatting
        format_dict = {
            "Gastos Construcción (USD)": "{:,.2f}",
            "Gastos Comisiones (USD)": "{:,.2f}",
            "Ingresos por Downpayment - Gastos Comision (USD)": "{:,.2f}",
            "Ingresos Cuotas Restantes (USD)": "{:,.2f}",
            "Ingresos por Down Payment + Cuotas Mensuales (USD)": "{:,.2f}",
            "Ingresos Acumulados (USD)": "{:,.2f}",
            "Acumulado (USD)": "{:,.2f}",
            "Capital Invertido (USD)": "{:,.2f}"
        }
        
        # Add the opportunity cost column with dynamic formatting
        opportunity_cost_col = [col for col in df.columns if "Costo de Oportunidad Mensual" in col]
        if opportunity_cost_col:
            format_dict[opportunity_cost_col[0]] = "{:,.2f}"
        
        st.dataframe(df.style.format(format_dict), use_container_width=True)
    
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
            <p><b>Costo Total Comisiones:</b> USD {:,.2f}</p>
            <p><b>Ganancia Neta:</b> USD {:,.2f}</p>
            <p><b>Costo de Oportunidad Total (TEA {:.2f}%):</b> USD {:,.2f}</p>
            <p><b>Mes de Recuperación de Inversión:</b> Mes {}</p>
        </div>
        """.format(
            metricas['total_ingresos'], 
            metricas['total_gastos'], 
            metricas.get('total_comisiones', 0.0),
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