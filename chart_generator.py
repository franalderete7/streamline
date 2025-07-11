# chart_generator.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class ChartGenerator:
    """
    Handles all chart generation for the cash flow application
    """
    
    @staticmethod
    def create_cash_flow_chart(df: pd.DataFrame, tea_costo_oportunidad: float) -> go.Figure:
        """
        Create the main cash flow chart showing accumulated expenses, income, and difference
        
        Args:
            df: Cash flow DataFrame
            tea_costo_oportunidad: Opportunity cost rate
            
        Returns:
            go.Figure: Plotly figure object
        """
        # Calculate accumulated values
        df_chart = df.copy()
        
        # Calculate accumulated expenses (construction + commissions)
        df_chart['Gasto Acumulado por Mes (USD)'] = (
            df_chart['Gastos Construcción (USD)'] + df_chart['Gastos Comisiones (USD)']
        ).cumsum()
        
        # Calculate accumulated income
        df_chart['Ingreso Acumulado por Mes (USD)'] = (
            df_chart['Ingresos por Down Payment + Cuotas Mensuales (USD)']
        ).cumsum()
        
        # Calculate difference (Income - Expenses)
        df_chart['Diferencia Entre Ingresos y Gastos (USD)'] = (
            df_chart['Ingreso Acumulado por Mes (USD)'] - df_chart['Gasto Acumulado por Mes (USD)']
        )
        
        # Create the line chart with the three traces
        fig = px.line(df_chart, x="Mes", 
                      y=["Gasto Acumulado por Mes (USD)", 
                         "Ingreso Acumulado por Mes (USD)", 
                         "Diferencia Entre Ingresos y Gastos (USD)"],
                      title="Evolución de Ingresos y Gastos Acumulados",
                      labels={"value": "USD", "variable": "Métricas"})
        
        # Improve chart styling with dark theme and increased scale
        fig.update_layout(
            legend_title_text="",
            template="plotly_dark",  # Changed to dark template
            title_font_size=24,  # Increased title font size
            title_font_color="#e0e0e0",  # Light color for dark background
            font=dict(size=14, color="#e0e0e0"),  # Increased font size
            plot_bgcolor='#2d2d2d',  # Dark background
            paper_bgcolor='#2d2d2d',  # Dark background
            margin=dict(l=80, r=80, t=120, b=80),  # Increased margins for better spacing
            hovermode='x unified',
            hoverlabel=dict(
                bgcolor="#1a1a1a", 
                font_size=14,  # Increased hover font size
                font_family="Arial",
                font_color="#e0e0e0"
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=0.98,  # Positioned closer to the chart
                xanchor="center",
                x=0.5,  # Centered horizontally
                bgcolor='rgba(45, 45, 45, 0.8)',  # Semi-transparent dark background
                bordercolor='#555555',
                borderwidth=1,
                font=dict(size=13, color="#e0e0e0"),  # Increased legend font size
                itemsizing='constant',
                itemwidth=40,  # Increased item width
                itemclick=False,  # Disable click to hide/show
                itemdoubleclick=False
            ),
            # Increased chart size for better visibility
            width=1200,  # Increased width
            height=700   # Increased height
        )
        
        # Update line colors and styles
        colors = ['#e74c3c', '#4CAF50', '#3498db']  # Red for expenses, Green for income, Blue for difference
        
        # Update all traces with common styling
        fig.update_traces(
            line=dict(width=4),  # Increased line width for better visibility
            hovertemplate='<b>%{fullData.name}</b><br>Mes: %{x}<br>USD: $%{y:,.0f}<extra></extra>'
        )
        
        # Update individual trace colors using update_traces with selector
        trace_names = ["Gasto Acumulado por Mes (USD)", "Ingreso Acumulado por Mes (USD)", "Diferencia Entre Ingresos y Gastos (USD)"]
        for i, (name, color) in enumerate(zip(trace_names, colors)):
            fig.update_traces(
                line_color=color,
                selector=dict(name=name)
            )
        
        # Update axes for dark theme
        fig.update_xaxes(
            gridcolor='#444444',
            zerolinecolor='#444444',
            showgrid=True,
            color='#e0e0e0'
        )
        
        fig.update_yaxes(
            gridcolor='#444444',
            zerolinecolor='#444444',
            showgrid=True,
            color='#e0e0e0'
        )
        
        return fig
    
    @staticmethod
    def create_summary_chart(df: pd.DataFrame) -> go.Figure:
        """
        Create a summary chart showing key metrics with dark theme
        
        Args:
            df: Cash flow DataFrame
            
        Returns:
            go.Figure: Plotly figure object
        """
        # Calculate summary metrics
        total_ingresos = df['Ingresos por Down Payment + Cuotas Mensuales (USD)'].sum()
        total_gastos_construccion = df['Gastos Construcción (USD)'].sum()
        total_gastos_comisiones = df['Gastos Comisiones (USD)'].sum()
        
        # Create bar chart
        categories = ['Ingresos', 'Gastos Construcción', 'Gastos Comisiones']
        values = [total_ingresos, total_gastos_construccion, total_gastos_comisiones]
        colors = ['#4CAF50', '#e74c3c', '#f39c12']
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=values,
                marker_color=colors,
                text=[f'${v:,.0f}' for v in values],
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>Valor: $%{y:,.0f}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title="Resumen Financiero del Proyecto",
            title_font_size=22,  # Increased title font size
            title_font_color="#e0e0e0",
            xaxis_title="Categorías",
            yaxis_title="USD",
            template="plotly_dark",
            plot_bgcolor='#2d2d2d',
            paper_bgcolor='#2d2d2d',
            margin=dict(l=80, r=80, t=100, b=80),  # Increased margins
            showlegend=False,
            font=dict(color="#e0e0e0", size=14),  # Increased font size
            # Increased chart size for better visibility
            width=1200,  # Increased width
            height=600   # Increased height
        )
        
        # Update axes for dark theme
        fig.update_xaxes(
            gridcolor='#444444',
            zerolinecolor='#444444',
            color='#e0e0e0'
        )
        
        fig.update_yaxes(
            gridcolor='#444444',
            zerolinecolor='#444444',
            color='#e0e0e0'
        )
        
        return fig 