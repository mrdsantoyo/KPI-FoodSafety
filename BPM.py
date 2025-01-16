import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from load_aci import bpm_operativo_df, bpm_personal_df
from pandas.errors import SettingWithCopyWarning
import warnings

# Ignorar advertencias
warnings.filterwarnings('ignore', category=SettingWithCopyWarning)

# Limpieza y preparación de df_operativo
df_operativo = bpm_operativo_df.copy()

# Combinar columnas 'Empaque 4' y 'EMPAQUE 4'
if 'Empaque 4' in df_operativo.columns:
    df_operativo['EMPAQUE 4'] = df_operativo['EMPAQUE 4'].combine_first(df_operativo['Empaque 4'])
    df_operativo = df_operativo.drop(columns=['Empaque 4'])

# Convertir la columna 'FECHA' a formato datetime
df_operativo['FECHA'] = pd.to_datetime(df_operativo['FECHA'], format='%d/%m/%Y', errors='coerce')

# Calcular promedios diarios
df_operativo['PROMEDIOS DIARIOS'] = df_operativo.iloc[:, 1:].apply(pd.to_numeric, errors='coerce').mean()

filtro_area = [
    'AHUMADOS', 'ALMACEN', 'COCIDOS Y ESTERILIZADOS', 'CORTE', 'DESHUESE',
    'ENVASADO', 'EMPAQUE 1', 'EMPAQUE 2', 'EMPAQUE 3', 'FRITA',
    'HABILITAMIENTO', 'INYECCION', 'MANTENIMIENTO', 'CONDIMENTOS',
    'MARINADOS', 'PELLET', 'SANIDAD', 'EMPAQUE 4'
]

# Limpieza y preparación de df_personal
df_personal = bpm_personal_df.copy()
df_personal['FECHA'] = pd.to_datetime(df_personal['FECHA'], format='%d/%m/%Y', errors='coerce')
df_personal['PROMEDIOS DIARIOS'] = df_personal.iloc[:,0].apply(pd.to_numeric, errors='coerce').mean()

# Dash App
bpms = Dash(__name__)

bpms.layout = html.Div(
    children=[
        dcc.Dropdown(
            id='filtro_area',
            options=[{'label': col, 'value': col} for col in filtro_area],
            value=None,  # Selección inicial (ninguna área seleccionada)
            placeholder="Selecciona un área",
            multi=True,
            style={
                'width': '750px',
                'backgroundColor': '#1A1A1A'
            }
        ),
        dcc.Interval(
            id='interval',
            interval=3600 * 1000,  # Actualización cada hora
            n_intervals=0
        ),
        dcc.Graph(
            id='operativas',
            style={
                'width': '750px',
                'height': '300px',
                'backgroundColor': '#2A2A2A'
            }
        ),
        dcc.Graph(
            id='personal',
            style={
                'width': '750px',
                'height': '300px',
                'backgroundColor': '#2A2A2A'
            }
        ),
    ]
)

# Callback para actualizar las gráficas
@bpms.callback(
    [Output('operativas', 'figure'),
     Output('personal', 'figure')],
    [Input('filtro_area', 'value'),
     Input('interval', 'n_intervals')]
)

def update_graphs(selected_areas, n_intervals):
    # Gráfica operativa
    fig_operativo = go.Figure()
    if not selected_areas:
        fig_operativo.add_trace(
            go.Scatter(
                x=df_operativo['FECHA'],
                y=df_operativo['PROMEDIOS DIARIOS'],
                mode='markers',
                name='Promedios Diarios'
            )
        )
    else:
        for area in selected_areas:
            if area in filtro_area:
                fig_operativo.add_trace(
                    go.Scatter(
                        x=df_operativo['FECHA'],
                        y=df_operativo[area],
                        mode='markers',
                        name=area
                    )
                )
    fig_operativo.update_layout(
        title="BPM's Operativas por Área",
        xaxis_title='Fecha',
        yaxis_title='Valor',
        template='plotly_dark',
        xaxis=dict(
            tickformat='%d/%m'
        ),
        showlegend=True
    )

    # Gráfica personal
    fig_personal = go.Figure()
    if not selected_areas:
        fig_personal.add_trace(
            go.Scatter(
                x=df_personal['FECHA'],
                y=df_personal['PROMEDIOS DIARIOS'],
                mode='markers',
                name='Promedios Diarios'
            )
        )
    else:
        for area in selected_areas:
            if area in filtro_area:
                fig_personal.add_trace(
                    go.Scatter(
                        x=df_personal['FECHA'],
                        y=df_personal[area],
                        mode='markers',
                        name=area
                    )
                )
    fig_personal.update_layout(
        title="BPM's Personales por Área",
        xaxis_title='Fecha',
        yaxis_title='Valor',
        template='plotly_dark',
        xaxis=dict(
            tickformat='%d/%m'
        ),
        showlegend=True
    )

    return fig_operativo, fig_personal


if __name__ == "__main__":
    bpms.run(debug=True, port='8052')
