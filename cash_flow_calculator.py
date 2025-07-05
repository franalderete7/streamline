# cash_flow_calculator.py
import pandas as pd
import numpy as np
from typing import Dict, Any

class CashFlowCalculator:
    """
    Handles all cash flow calculations for real estate projects
    """
    
    @staticmethod
    def generar_flujo_caja(inversion_inicial: float, gasto_construccion_mensual: float, 
                          comision_por_venta: float, precio_por_duplex: float,
                          num_cuotas: int, duplex_por_etapa: int, meses_por_etapa: int, 
                          total_etapas: int, tasa_ventas: float, tea_costo_oportunidad: float) -> pd.DataFrame:
        """
        Generate cash flow calculations for real estate project
        
        Args:
            inversion_inicial: Initial investment amount
            gasto_construccion_mensual: Monthly construction expenses
            comision_por_venta: Commission per sale
            precio_por_duplex: Price per duplex
            num_cuotas: Number of installments
            duplex_por_etapa: Duplexes per stage
            meses_por_etapa: Months per stage
            total_etapas: Total stages
            tasa_ventas: Sales rate
            tea_costo_oportunidad: Opportunity cost rate
            
        Returns:
            pd.DataFrame: Cash flow data
        """
        # Calcular parámetros derivados
        total_duplex = duplex_por_etapa * total_etapas
        total_meses_construccion = meses_por_etapa * total_etapas
        total_meses = total_meses_construccion + num_cuotas  # Incluye período de cobro de cuotas
        cuota_mensual = precio_por_duplex / num_cuotas if num_cuotas > 0 else 0
        tasa_mensual = (1 + tea_costo_oportunidad) ** (1/12) - 1 if tea_costo_oportunidad > 0 else 0

        # Crear DataFrame
        df = pd.DataFrame({
            "Mes": range(total_meses + 1),
            "Etapa de Construcción": [""] * (total_meses + 1),
            "Gastos Construcción (USD)": [0.0] * (total_meses + 1),
            "Gastos Comisiones (USD)": [0.0] * (total_meses + 1),
            "Ingresos por Cuotas (USD)": [0.0] * (total_meses + 1),
            "Dúplex Vendidos": [0] * (total_meses + 1),
            "Cuotas Activas": [0] * (total_meses + 1),
            "Saldo Neto Mensual (USD)": [0.0] * (total_meses + 1),
            "Ingresos Acumulados (USD)": [0.0] * (total_meses + 1),
            "Acumulado (USD)": [0.0] * (total_meses + 1),
            "Capital Invertido (USD)": [0.0] * (total_meses + 1),
            "Costo de Oportunidad Mensual (USD, TEA {:.2f}% Depósito USD)".format(tea_costo_oportunidad * 100): [0.0] * (total_meses + 1)
        })

        # Mes 0: Inversión inicial
        df.loc[0, "Etapa de Construcción"] = "Inicial"
        df.loc[0, "Gastos Construcción (USD)"] = inversion_inicial
        df.loc[0, "Saldo Neto Mensual (USD)"] = -inversion_inicial
        df.loc[0, "Acumulado (USD)"] = -inversion_inicial
        df.loc[0, "Capital Invertido (USD)"] = inversion_inicial
        df.loc[0, "Costo de Oportunidad Mensual (USD, TEA {:.2f}% Depósito USD)".format(tea_costo_oportunidad * 100)] = inversion_inicial * tasa_mensual

        # Calcular ventas y cuotas
        duplex_vendidos = 0
        cuotas_por_duplex = {}
        for mes in range(1, total_meses + 1):
            # Asignar etapa
            if mes <= total_meses_construccion:
                etapa_num = (mes - 1) // meses_por_etapa + 1
                df.loc[mes, "Etapa de Construcción"] = f"Etapa {etapa_num}" if etapa_num <= total_etapas else "Post-Construcción"
            else:
                df.loc[mes, "Etapa de Construcción"] = "Post-Construcción"

            # Gastos de construcción
            if mes <= total_meses_construccion:
                df.loc[mes, "Gastos Construcción (USD)"] = gasto_construccion_mensual

            # Ventas de dúplex
            if duplex_vendidos < total_duplex and mes <= total_meses_construccion:
                duplex_vendidos += tasa_ventas
                df.loc[mes, "Dúplex Vendidos"] = int(duplex_vendidos)
                if duplex_vendidos - int(duplex_vendidos) < tasa_ventas:
                    df.loc[mes, "Gastos Comisiones (USD)"] = comision_por_venta
                    cuotas_por_duplex[mes] = num_cuotas

            # Cuotas activas
            cuotas_activas = 0
            for inicio, cuotas_restantes in list(cuotas_por_duplex.items()):
                if mes >= inicio and cuotas_restantes > 0:
                    cuotas_activas += 1
                    cuotas_por_duplex[inicio] -= 1
            df.loc[mes, "Cuotas Activas"] = cuotas_activas
            df.loc[mes, "Ingresos por Cuotas (USD)"] = cuotas_activas * cuota_mensual

            # Saldo neto mensual
            df.loc[mes, "Saldo Neto Mensual (USD)"] = df.loc[mes, "Ingresos por Cuotas (USD)"] - \
                                                      df.loc[mes, "Gastos Construcción (USD)"] - \
                                                      df.loc[mes, "Gastos Comisiones (USD)"]

            # Ingresos acumulados y acumulado
            df.loc[mes, "Ingresos Acumulados (USD)"] = df.loc[:mes, "Ingresos por Cuotas (USD)"].sum()
            df.loc[mes, "Acumulado (USD)"] = df.loc[:mes, "Saldo Neto Mensual (USD)"].sum()

            # Capital invertido y costo de oportunidad
            df.loc[mes, "Capital Invertido (USD)"] = -df.loc[mes, "Acumulado (USD)"] if df.loc[mes, "Acumulado (USD)"] < 0 else 0
            df.loc[mes, "Costo de Oportunidad Mensual (USD, TEA {:.2f}% Depósito USD)".format(tea_costo_oportunidad * 100)] = \
                df.loc[mes, "Capital Invertido (USD)"] * tasa_mensual

        return df
    
    @staticmethod
    def calcular_metricas_financieras(df: pd.DataFrame, tea_costo_oportunidad: float) -> Dict[str, Any]:
        """
        Calculate key financial metrics from cash flow data
        
        Args:
            df: Cash flow DataFrame
            tea_costo_oportunidad: Opportunity cost rate
            
        Returns:
            Dict with financial metrics
        """
        # Calcular métricas
        total_ingresos = df["Ingresos por Cuotas (USD)"].sum()
        total_gastos = df["Gastos Construcción (USD)"].sum() + df["Gastos Comisiones (USD)"].sum()
        ganancia_neta = total_ingresos - total_gastos
        costo_oportunidad_total = df[f"Costo de Oportunidad Mensual (USD, TEA {tea_costo_oportunidad * 100:.2f}% Depósito USD)"].sum()
        mes_recuperacion = df[df["Acumulado (USD)"] > 0]["Mes"].iloc[0] if not df[df["Acumulado (USD)"] > 0].empty else "No alcanzado"
        
        return {
            'total_ingresos': total_ingresos,
            'total_gastos': total_gastos,
            'ganancia_neta': ganancia_neta,
            'costo_oportunidad_total': costo_oportunidad_total,
            'mes_recuperacion': mes_recuperacion
        } 