import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from MTTO.load_mtto import df
import warnings
warnings.filterwarnings('ignore')
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import styles

# 1. Elimina filas sin FECHA y columnas innecesarias
df = df.dropna(subset=['FECHA'])
df = df.drop(columns=['TIEMPO_RAW', 'SEMANA', 'TIEMPO'])

# 2. Convierte FECHA a tipo datetime
df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y')

# 3. Ordena todo el DataFrame por FECHA
df = df.sort_values(by='FECHA', ascending=True)

# 4. Normaliza ESTATUS
df['ESTATUS'] = df['ESTATUS'].astype(str).str.strip().str.upper()

# 5. Crea una copia para trabajar
df1 = df.copy()

# 6. Extrae el número de mes y reemplázalo por su nombre
df1['MES'] = df1['FECHA'].dt.month
df1['MES'].replace(
    {
        1: 'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre'
    },
    inplace=True
)

# 7. Convierte la columna MES en categórico ordenado
orden_meses = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]
df1['MES'] = pd.Categorical(df1['MES'], categories=orden_meses, ordered=True)

def actualizar_graficos(filtro_equipo, filtro_tecnico, filtro_area):
    # 8. Aplica los filtros sobre la copia ordenada y categorizada
    df_filtrado = df1.copy()
    
    if filtro_equipo:
        df_filtrado = df_filtrado[df_filtrado['EQUIPO'].str.upper().isin(filtro_equipo)]
    if filtro_area:
        df_filtrado = df_filtrado[df_filtrado['ÁREA'].str.upper().isin(filtro_area)]
    if filtro_tecnico:
        df_filtrado = df_filtrado[df_filtrado['TÉCNICO'].str.upper().isin(filtro_tecnico)]
    
    # 9. Calcula la eficiencia por mes
    total_mes = df_filtrado.groupby('MES')['ESTATUS'].count()
    realizados_mes = df_filtrado[df_filtrado['ESTATUS'] == 'REALIZADO'].groupby('MES')['ESTATUS'].count()
    eficiencia = (realizados_mes / total_mes).fillna(0) * 100
    eficiencia = eficiencia.reset_index(name='PorcentajeRealizados')
    
    # 10. Crea el gráfico
    graf_eficiencia = go.Figure()
    graf_eficiencia.add_trace(
        go.Scatter(
            x=eficiencia['MES'],  # la columna categórica ordenada
            y=eficiencia['PorcentajeRealizados'],
            mode='lines+markers',
            hoverlabel=dict(namelength=0),
            name='Eficiencia %'
        )
    )
    graf_eficiencia.update_layout(
        title='Eficiencia de Mantenimientos Mensuales',
        xaxis_title='Mes',
        yaxis_title='Porcentaje (%)',
        template='plotly_dark'
    )
    
    return graf_eficiencia

# Ahora, cuando llames a actualizar_graficos, verás los meses en orden cronológico.
