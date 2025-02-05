from load_aci import bpm_operativo_df, bpm_personal_df
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
import warnings
warnings.filterwarnings('ignore')

try:
    bpm_operativo_df['FECHA'] = pd.to_datetime(bpm_operativo_df['FECHA'], errors='coerce', format='%d/%m/%Y')
    bpm_operativo_df = bpm_operativo_df.dropna(subset=['FECHA'])
    bpm_operativo_df['PROMEDIOS DIARIOS'] = bpm_operativo_df.drop('FECHA', axis=1).mean(axis=1)
    bpm_operativo_df['EMPAQUE 4'] = bpm_operativo_df['EMPAQUE 4'].combine_first(bpm_operativo_df['Empaque 4'])
    bpm_operativo_df = bpm_operativo_df.drop('Empaque 4', axis=1)
    bpm_operativo_df.columns = bpm_operativo_df.columns.str.upper()
except:
    print(f"Error procesando bpm_operativo_df: {e}")

try:
    bpm_personal_df['FECHA'] = pd.to_datetime(bpm_personal_df['DIA'], errors='coerce', format='%d/%m/%Y')
    bpm_personal_df = bpm_personal_df.drop('DIA', axis=1)
    bpm_personal_df = bpm_personal_df.dropna(subset=['FECHA'])
    bpm_personal_df['PROMEDIOS DIARIOS'] = bpm_personal_df.drop(['FECHA', 'AREA'], axis=1).mean(axis=1)

    bpm_personal_df['INYECCION'] = bpm_personal_df['INYECCION'].combine_first(bpm_personal_df['INYECCION '])
    bpm_personal_df = bpm_personal_df.drop(['INYECCION ', 'AREA'], axis=1)
    bpm_personal_df.columns = bpm_personal_df.columns.str.upper()
except:
    print(f"Error procesando bpm_personal_df: {e}")


filtro_area = [col for col in bpm_operativo_df.columns if col not in ['FECHA', 'PROMEDIOS DIARIOS']]

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
        dcc.DatePickerRange(
            id='filtro_fecha',
            start_date=bpm_operativo_df['FECHA'].min(),
            end_date=bpm_operativo_df['FECHA'].max(),
            style={
                'width': '750px',
                'backgroundColor': '#2A2A2A'
            }
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
        Input('filtro_fecha', 'start_date'),
        Input('filtro_fecha', 'end_date')
        ]
    )
def actualizar_graficos(filtro_area, filtro_fecha_inicio, filtro_fecha_fin):
    start_date = pd.to_datetime(filtro_fecha_inicio)
    end_date = pd.to_datetime(filtro_fecha_fin)
    
    df_operativo_filtrado = bpm_operativo_df[(bpm_operativo_df['FECHA'] >= start_date) & 
                                        (bpm_operativo_df['FECHA'] <= end_date)]
    df_personal_filtrado = bpm_personal_df[(bpm_personal_df['FECHA'] >= start_date) & 
                                        (bpm_personal_df['FECHA'] <= end_date)]
    
    operativas_graf = go.Figure()
    personales_graf = go.Figure()
    
    if not filtro_area:
        operativas_graf.add_trace(
            go.Scatter(
                x=df_operativo_filtrado['FECHA'],
                y=df_operativo_filtrado['PROMEDIOS DIARIOS'],
                mode='lines+markers',
                name='Promedios Diarios'
            )
        )
        operativas_graf.update_layout(
            title='BPM Operativas (Promedios Diarios)',
            xaxis_title='Fecha',
            yaxis_title='Calificación (%)',
            template='plotly_dark'
            )
        personales_graf.update_layout(
            title='BPM Personales (Promedios Diarios)',
            xaxis_title='Fecha',
            yaxis_title='Calificación (%)',
            template='plotly_dark'
            )
        personales_graf.add_trace(
            go.Scatter(
                x=df_personal_filtrado['FECHA'],
                y=df_personal_filtrado['PROMEDIOS DIARIOS'],
                mode='lines+markers',
                name='Promedios Diarios'
            )
        )
    else:
        for area in filtro_area:
            if area in df_operativo_filtrado.columns:
                operativas_graf.add_trace(
                    go.Scatter(
                        x=df_operativo_filtrado['FECHA'],
                        y=df_operativo_filtrado[area],
                        mode='lines+markers',
                        name=area
                    )
                )
            if area in df_personal_filtrado.columns:
                personales_graf.add_trace(
                    go.Scatter(
                        x=df_personal_filtrado['FECHA'],
                        y=df_personal_filtrado[area],
                        mode='lines+markers',
                        name=area
                    )
                )
    
        operativas_graf.update_layout(
            title='BPM Operativas',
            xaxis_title='Fecha',
            yaxis_title='Calificación (%)',
            template='plotly_dark'
        )
        personales_graf.update_layout(
            title='BPM Personales',
            xaxis_title='Fecha',
            yaxis_title='Calificación (%)',
            template='plotly_dark'
        )
    
    return operativas_graf, personales_graf

if __name__ == "__main__":
	bpms.run(debug=True, port='8052')




