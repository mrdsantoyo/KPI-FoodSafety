from load_aci import bpm_operativo_df, bpm_personal_df
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output

# Procesar bpm_operativo_df
try:
    bpm_operativo_df['EMPAQUE 4'] = bpm_operativo_df['EMPAQUE 4'].combine_first(bpm_operativo_df.get('Empaque 4'))
    bpm_operativo_df = bpm_operativo_df.drop(columns=['Empaque 4'], errors='ignore')
    bpm_operativo_df.iloc[1:] = bpm_operativo_df.iloc[1:].apply(pd.to_numeric, errors='coerce')
    bpm_operativo_df['FECHA'] = pd.to_datetime(bpm_operativo_df['FECHA'], format='%d/%m', errors='coerce').dt.strftime('%d/%m')
    reorder = ['FECHA', 'AHUMADOS', 'ALMACEN', 'COCIDOS Y ESTERILIZADOS', 'CORTE', 'DESHUESE',
               'ENVASADO', 'EMPAQUE 1', 'EMPAQUE 2', 'EMPAQUE 3', 'FRITA',
               'HABILITAMIENTO', 'INYECCION', 'MANTENIMIENTO', 'CONDIMENTOS',
               'MARINADOS', 'PELLET', 'SANIDAD', 'EMPAQUE 4']
    bpm_operativo_df = bpm_operativo_df.reindex(columns=reorder).dropna(subset=['FECHA'])
    bpm_operativo_df['PROMEDIOS DIARIOS'] = bpm_operativo_df.iloc[:, 1:].mean(axis=1)
except Exception as e:
    print(f"Error procesando bpm_operativo_df: {e}")

# Procesar bpm_personal_df
try:
    bpm_personal_df.iloc[:, 1:] = bpm_personal_df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
    bpm_personal_df['FECHA'] = pd.to_datetime(bpm_personal_df['FECHA'], format='%d/%m', errors='coerce').dt.strftime('%d/%m')
    bpm_personal_df['PROMEDIOS DIARIOS'] = bpm_personal_df.iloc[:, 1:].mean(axis=1)
except Exception as e:
    print(f"Error procesando bpm_personal_df: {e}")

# Inicializar opciones para el dropdown
filtro_area = [col for col in bpm_operativo_df.columns if col not in ['FECHA', 'PROMEDIOS DIARIOS']]

# Crear la app Dash
bpms = Dash(__name__)
bpms.layout = html.Div(
    children=[
        dcc.Dropdown(
            id='filtro_area',
            options=[{'label': col, 'value': col} for col in filtro_area],
            placeholder='Selecciona un área',
            multi=True,
            style={
                'width': '750px',
                'backgroundColor': '#2A2A2A'
            }
        ),
        dcc.Interval(
            id='intervalo',
            interval=3600 * 1000,
            n_intervals=0
        ),
        dcc.Graph(
            id='operativas_graf',
            style={
                'width': '750px',
                'height': '300px',
                'backgroundColor': '#2A2A2A'
            }
        ),
        dcc.Graph(
            id='personales_graf',
            style={
                'width': '750px',
                'height': '300px',
                'backgroundColor': '#2A2A2A'
            }
        )
    ]
)
@bpms.callback(
    [
        Output('operativas_graf', 'figure'),
        Output('personales_graf', 'figure')
    ],
    [
        Input('filtro_area', 'value'),
        Input('intervalo', 'n_intervals')
    ]
)
def graficos(filtro_area, n_intervals):
    # Gráfico para operativas_graf
    operativas_graf = go.Figure()
    if not filtro_area:
        operativas_graf.add_trace(
            go.Scatter(
                x=bpm_operativo_df['FECHA'],
                y=bpm_operativo_df['PROMEDIOS DIARIOS'],
                mode='lines+markers',
                name='Promedios Diarios'
            )
        )
    else:
        for area in filtro_area:
            operativas_graf.add_trace(
                go.Scatter(
                    x=bpm_operativo_df['FECHA'],
                    y=bpm_operativo_df[area],
                    mode='lines+markers',
                    name=area
                )
            )
    operativas_graf.update_layout(
        title="Gráfico de BPM's operativas por área",
        template='plotly_dark',
        xaxis=dict(title="Fecha", showgrid=True, autorange=True),
        yaxis=dict(title="Promedio", showgrid=True, autorange=True),
        showlegend=True
    )

    # Gráfico para personales_graf
    personales_graf = go.Figure()
    if not filtro_area:
        personales_graf.add_trace(
            go.Scatter(
                x=bpm_personal_df['FECHA'],
                y=bpm_personal_df['PROMEDIOS DIARIOS'],
                mode='lines+markers',
                name='Promedios Diarios'
            )
        )
    else:
        for area in filtro_area:
            if area in bpm_personal_df.columns:
                personales_graf.add_trace(
                    go.Scatter(
                        x=bpm_personal_df['FECHA'],
                        y=bpm_personal_df[area],
                        mode='lines+markers',
                        name=area
                    )
                )
    personales_graf.update_layout(
        title="Gráfico de BPM's personales por área",
        template='plotly_dark',
        xaxis=dict(title="Fecha", showgrid=True, autorange=True),
        yaxis=dict(title="Promedio", showgrid=True, autorange=True),
        showlegend=True
    )

    return operativas_graf, personales_graf

if __name__ == "__main__":
    bpms.run(debug=True, port='8052')
