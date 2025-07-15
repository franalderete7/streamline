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
                          total_etapas: int, tasa_ventas: float, tea_costo_oportunidad: float,
                          porcentaje_down_payment: float = 40.0, num_cuotas_restantes: int = 10,
                          down_payment_amount: float = 0.0, cuota_restante_mensual: float = 0.0) -> pd.DataFrame:
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
            tasa_ventas: Sales rate (duplexes per month)
            tea_costo_oportunidad: Opportunity cost rate
            
        Returns:
            pd.DataFrame: Cash flow data
        """
        # Calcular parámetros derivados
        total_duplex = duplex_por_etapa * total_etapas
        total_meses_construccion = meses_por_etapa * total_etapas
        
        # Calculate payment structure if not provided
        if down_payment_amount == 0.0:
            down_payment_amount = precio_por_duplex * (porcentaje_down_payment / 100)
        if cuota_restante_mensual == 0.0:
            remaining_amount = precio_por_duplex - down_payment_amount
            cuota_restante_mensual = remaining_amount / num_cuotas_restantes if num_cuotas_restantes > 0 else 0
        
        # Calculate realistic timeline to ensure ALL payments are collected
        # Estimate when the last duplex will be sold based on non-overlapping etapa sales
        
        # Etapa 1: starts month 1, sells 11 duplexes at 0.5/month = ~22 months to complete
        # Etapa 2: starts max(month 16, when etapa 1 finishes), sells 11 duplexes
        # Etapa 3: starts max(month 31, when etapa 2 finishes), sells 11 duplexes
        
        # Conservative estimate: account for sales rate and etapa dependencies
        etapa_1_completion = max(1, int(duplex_por_etapa / max(tasa_ventas, 0.1)))
        etapa_2_start = max(meses_por_etapa + 1, etapa_1_completion + 1)  # Month 16 or when etapa 1 finishes
        etapa_2_completion = etapa_2_start + int(duplex_por_etapa / max(tasa_ventas, 0.1))
        etapa_3_start = max(meses_por_etapa * 2 + 1, etapa_2_completion + 1)  # Month 31 or when etapa 2 finishes
        etapa_3_completion = etapa_3_start + int(duplex_por_etapa / max(tasa_ventas, 0.1))
        
        # Last sale month is when etapa 3 completes
        estimated_last_sale_month = etapa_3_completion
        
        # Ensure timeline extends enough to collect ALL payments from the last sale
        minimum_total_months = estimated_last_sale_month + num_cuotas_restantes
        
        # Use the larger of the original calculation or our new minimum
        extra_meses = max(0, int(total_duplex / max(tasa_ventas, 0.1)) - total_meses_construccion)
        original_total_meses = total_meses_construccion + num_cuotas_restantes + extra_meses
        total_meses = max(original_total_meses, minimum_total_months)
        tasa_mensual = (1 + tea_costo_oportunidad) ** (1/12) - 1 if tea_costo_oportunidad > 0 else 0

        # Crear DataFrame
        df = pd.DataFrame({
            "Mes": range(total_meses + 1),
            "Etapa de Construcción": [""] * (total_meses + 1),
            "Gastos Construcción (USD)": [0.0] * (total_meses + 1),
            "Gastos Comisiones (USD)": [0.0] * (total_meses + 1),
            "Ingresos por Downpayment - Gastos Comision (USD)": [0.0] * (total_meses + 1),
            "Ingresos Cuotas Restantes (USD)": [0.0] * (total_meses + 1),
            "Ingresos por Down Payment + Cuotas Mensuales (USD)": [0.0] * (total_meses + 1),
            "Dúplex Vendidos": [0] * (total_meses + 1),
            "Cuotas Activas": [0] * (total_meses + 1),
            "Ingresos Acumulados (USD)": [0.0] * (total_meses + 1),
            "Acumulado (USD)": [0.0] * (total_meses + 1),
            "Capital Invertido (USD)": [0.0] * (total_meses + 1),
            "Costo de Oportunidad Mensual (USD, TEA {:.2f}% Depósito USD)".format(tea_costo_oportunidad * 100): [0.0] * (total_meses + 1)
        })

        # Mes 0: Inversión inicial
        df.loc[0, "Etapa de Construcción"] = "Inicial"
        df.loc[0, "Gastos Construcción (USD)"] = inversion_inicial
        df.loc[0, "Acumulado (USD)"] = -inversion_inicial
        df.loc[0, "Capital Invertido (USD)"] = inversion_inicial
        df.loc[0, "Costo de Oportunidad Mensual (USD, TEA {:.2f}% Depósito USD)".format(tea_costo_oportunidad * 100)] = inversion_inicial * tasa_mensual

        # Calcular ventas y cuotas - NON-OVERLAPPING ETAPA SALES
        duplex_vendidos_acumulados = 0
        fraccion_acumulada = 0.0  # Accumulate fractions until we have whole duplexes
        cuotas_por_duplex = {}  # {mes_inicio: cuotas_restantes}
        
        # Track sales by etapa
        duplex_vendidos_por_etapa = [0] * total_etapas  # Track sold duplexes per etapa
        etapa_actual_venta = 0  # Current etapa being sold (0-indexed)
        
        # Calculate when each etapa can start selling
        # Etapa 1: starts month 1 (construction starts)
        # Etapa 2: starts max(month 16, month when etapa 1 is sold out)
        # Etapa 3: starts max(month 31, month when etapa 2 is sold out)
        etapa_inicio_venta = {}  # Will be populated as we go
        
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

            # Determine which etapa we can sell from this month
            # Calculate when each etapa's sales can start
            if etapa_actual_venta == 0:
                # Etapa 1 can start selling from month 1
                if 1 not in etapa_inicio_venta:
                    etapa_inicio_venta[1] = 1
            elif etapa_actual_venta == 1:
                # Etapa 2 can start selling when:
                # 1. Etapa 2 construction starts (month 16) AND
                # 2. Etapa 1 is sold out
                etapa_2_construccion_inicio = meses_por_etapa + 1  # Month 16
                if duplex_vendidos_por_etapa[0] >= duplex_por_etapa and mes >= etapa_2_construccion_inicio:
                    if 2 not in etapa_inicio_venta:
                        etapa_inicio_venta[2] = mes
            elif etapa_actual_venta == 2:
                # Etapa 3 can start selling when:
                # 1. Etapa 3 construction starts (month 31) AND
                # 2. Etapa 2 is sold out
                etapa_3_construccion_inicio = meses_por_etapa * 2 + 1  # Month 31
                if duplex_vendidos_por_etapa[1] >= duplex_por_etapa and mes >= etapa_3_construccion_inicio:
                    if 3 not in etapa_inicio_venta:
                        etapa_inicio_venta[3] = mes

            # Ventas de dúplex - NON-OVERLAPPING ETAPA SALES
            duplex_vendidos_mes = 0
            
            # Check if we can sell from current etapa
            can_sell_this_month = False
            if etapa_actual_venta < total_etapas:
                etapa_numero = etapa_actual_venta + 1
                if etapa_numero in etapa_inicio_venta and mes >= etapa_inicio_venta[etapa_numero]:
                    # We can sell from this etapa if it's not sold out
                    if duplex_vendidos_por_etapa[etapa_actual_venta] < duplex_por_etapa:
                        can_sell_this_month = True
                    else:
                        # Current etapa is sold out, move to next etapa
                        etapa_actual_venta += 1
                        can_sell_this_month = False  # Check next etapa next month
            
            if can_sell_this_month and duplex_vendidos_acumulados < total_duplex:
                # Calculate available duplexes from current etapa
                duplex_disponibles_etapa = duplex_por_etapa - duplex_vendidos_por_etapa[etapa_actual_venta]
                
                # Use consistent sales rate throughout the project
                tasa_mes = min(tasa_ventas, duplex_disponibles_etapa)
                
                if tasa_mes > 0:
                    # If it's the very first month of sales and the rate is fractional,
                    # give it a one-time boost to ensure a sale happens.
                    # Otherwise, just accumulate the sales rate.
                    if mes == 1 and tasa_ventas < 1.0:
                        fraccion_acumulada = 1.0
                    else:
                        fraccion_acumulada += tasa_mes

                    # Sell complete duplexes only
                    duplex_completos = int(fraccion_acumulada)
                    fraccion_acumulada -= duplex_completos
                    
                    # Don't exceed available duplexes from current etapa
                    duplex_completos = min(duplex_completos, duplex_disponibles_etapa)
                    
                    if duplex_completos > 0:
                        duplex_vendidos_mes = duplex_completos
                        duplex_vendidos_acumulados += duplex_completos
                        duplex_vendidos_por_etapa[etapa_actual_venta] += duplex_completos
                        
                        df.loc[mes, "Dúplex Vendidos"] = duplex_completos
                        df.loc[mes, "Gastos Comisiones (USD)"] = duplex_completos * comision_por_venta
                        
                        # Generate down payment income minus commission immediately
                        down_payment_income = duplex_completos * down_payment_amount
                        commission_expense = duplex_completos * comision_por_venta
                        df.loc[mes, "Ingresos por Downpayment - Gastos Comision (USD)"] = down_payment_income - commission_expense
                        df.loc[mes, "Gastos Comisiones (USD)"] = commission_expense  # Keep for reference/tracking
                        
                        # Generate remaining cuotas for each complete duplex sold - START NEXT MONTH
                        for i in range(duplex_completos):
                            duplex_id = f"{mes}_{i}"
                            cuotas_por_duplex[duplex_id] = {
                                'cuotas_restantes': num_cuotas_restantes,
                                'mes_venta': mes
                            }

            # Calcular cuotas activas e ingresos restantes - START FROM NEXT MONTH AFTER SALE
            cuotas_activas = 0
            cuotas_por_duplex_actualizadas = {}
            
            for duplex_id, duplex_info in cuotas_por_duplex.items():
                mes_venta = duplex_info['mes_venta']
                cuotas_restantes = duplex_info['cuotas_restantes']
                
                # First cuota starts the month AFTER the sale
                if mes > mes_venta and cuotas_restantes > 0:
                    cuotas_activas += 1
                    cuotas_restantes -= 1
                    if cuotas_restantes > 0:
                        cuotas_por_duplex_actualizadas[duplex_id] = {
                            'cuotas_restantes': cuotas_restantes,
                            'mes_venta': mes_venta
                        }
                elif cuotas_restantes > 0:
                    # Keep the duplex in the list but don't collect cuota this month
                    cuotas_por_duplex_actualizadas[duplex_id] = duplex_info
            
            cuotas_por_duplex = cuotas_por_duplex_actualizadas
            df.loc[mes, "Cuotas Activas"] = cuotas_activas
            
            # Calculate income from remaining cuotas
            ingresos_cuotas_restantes = cuotas_activas * cuota_restante_mensual
            df.loc[mes, "Ingresos Cuotas Restantes (USD)"] = ingresos_cuotas_restantes
            
            # Total income is down payment (net of commission) + remaining cuotas
            total_income = df.loc[mes, "Ingresos por Downpayment - Gastos Comision (USD)"] + ingresos_cuotas_restantes
            df.loc[mes, "Ingresos por Down Payment + Cuotas Mensuales (USD)"] = total_income

            # Ingresos acumulados y acumulado (commission already subtracted in down payment column)
            df.loc[mes, "Ingresos Acumulados (USD)"] = df.loc[:mes, "Ingresos por Down Payment + Cuotas Mensuales (USD)"].sum()
            
            # Calculate net flow for this month (commission already subtracted in down payment column)
            saldo_neto_mensual = df.loc[mes, "Ingresos por Down Payment + Cuotas Mensuales (USD)"] - \
                                df.loc[mes, "Gastos Construcción (USD)"]
            
            # Update accumulated balance
            df.loc[mes, "Acumulado (USD)"] = df.loc[mes-1, "Acumulado (USD)"] + saldo_neto_mensual

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
        # Calcular métricas (commission already netted in down payment column)
        total_ingresos = df["Ingresos por Down Payment + Cuotas Mensuales (USD)"].sum()
        total_gastos = df["Gastos Construcción (USD)"].sum()  # Commission already subtracted from income
        total_comisiones = df["Gastos Comisiones (USD)"].sum()  # Track commission separately for display
        ganancia_neta = total_ingresos - total_gastos
        costo_oportunidad_total = df[f"Costo de Oportunidad Mensual (USD, TEA {tea_costo_oportunidad * 100:.2f}% Depósito USD)"].sum()
        positive_months = df[df["Acumulado (USD)"] > 0]
        if len(positive_months) > 0:
            mes_recuperacion = positive_months["Mes"].tolist()[0]
        else:
            mes_recuperacion = "No alcanzado"
        
        return {
            'total_ingresos': total_ingresos,
            'total_gastos': total_gastos,
            'total_comisiones': total_comisiones,
            'ganancia_neta': ganancia_neta,
            'costo_oportunidad_total': costo_oportunidad_total,
            'mes_recuperacion': mes_recuperacion
        } 