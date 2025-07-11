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
        Create the main cash flow chart with dark theme
        
        Args:
            df: Cash flow DataFrame
            tea_costo_oportunidad: Opportunity cost rate
            
        Returns:
            go.Figure: Plotly figure object
        """
        # Create the main line chart
        fig = px.line(df, x="Mes", 
                      y=["Ingresos por Down Payment + Cuotas Mensuales (USD)", "Ingresos por Downpayment - Gastos Comision (USD)", "Gastos Construcción (USD)", 
                         "Acumulado (USD)", f"Costo de Oportunidad Mensual (USD, TEA {tea_costo_oportunidad * 100:.2f}% Depósito USD)"],
                      title="Evolución del Flujo de Caja",
                      labels={"value": "USD", "variable": "Métricas"})
        
        # Improve chart styling with dark theme
        fig.update_layout(
            legend_title_text="",
            template="plotly_dark",  # Changed to dark template
            title_font_size=20,
            title_font_color="#e0e0e0",  # Light color for dark background
            font=dict(size=12, color="#e0e0e0"),  # Light text color
            plot_bgcolor='#2d2d2d',  # Dark background
            paper_bgcolor='#2d2d2d',  # Dark background
            margin=dict(l=50, r=50, t=100, b=50),  # Increased top margin for legend
            hovermode='x unified',
            hoverlabel=dict(
                bgcolor="#1a1a1a", 
                font_size=12, 
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
                font=dict(size=11, color="#e0e0e0"),
                itemsizing='constant',
                itemwidth=30,
                itemclick=False,  # Disable click to hide/show
                itemdoubleclick=False
            )
        )
        
        # Update line colors and styles
        fig.update_traces(
            line=dict(width=3),
            hovertemplate='<b>%{fullData.name}</b><br>Mes: %{x}<br>USD: $%{y:,.0f}<extra></extra>'
        )
        
        # Customize colors for dark theme
        colors = ['#4CAF50', '#2ecc71', '#e74c3c', '#f39c12', '#3498db', '#9b59b6']
        for i in range(len(fig.data)):
            fig.data[i].line.color = colors[i % len(colors)]
        
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
            title_font_size=18,
            title_font_color="#e0e0e0",
            xaxis_title="Categorías",
            yaxis_title="USD",
            template="plotly_dark",
            plot_bgcolor='#2d2d2d',
            paper_bgcolor='#2d2d2d',
            margin=dict(l=50, r=50, t=80, b=50),
            showlegend=False,
            font=dict(color="#e0e0e0")
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