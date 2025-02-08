import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from load_mtto import df

mtto = Dash()
mtto.layout = html.Div(
    children=[
        dcc.Dropdown(
            id='filtro_equipo',
            options=[{'label': x.upper(), 'value': x.upper()} for x in df['EQUIPO'].dropna().unique()],
            multi=True,
            placeholder='Selecciona un equipo',
            style={
                'width': '500px',
                'backgroundColor': '#1b1b1b'
            }
        ),
        dcc.Dropdown(
            id='filtro_tecnico',
            options=[{'label': x.upper(), 'value': x.upper()} for x in df['TÉCNICO'].dropna().unique()],
            multi=True,
            placeholder='Selecciona un técnico',
            style={
                'width': '500px',
                'backgroundColor': '#1b1b1b'
            }
        ),
        dcc.Graph(
            id='realizados',
            style={
                'width': '500px',
                'height': '500px',
                'backgroundColor': '#1b1b1b'
            }
        )
    ]
)
@mtto.callback(
    Output('realizados', 'figure'),
    [
        Input('filtro_equipo', 'value'),
        Input('filtro_tecnico', 'value')
        ]
)
def update_graphs(filtro_equipo, filtro_tecnico):
    # Filtrar según el equipo seleccionado
    df_filtrado = df.copy()
    if filtro_equipo:
        df_filtrado = df_filtrado[df_filtrado['EQUIPO'].str.upper().isin(filtro_equipo)]
    if filtro_tecnico:
        df_filtrado = df_filtrado[df_filtrado['TÉCNICO'].str.upper().isin(filtro_tecnico)]

    # Contar los valores de ESTATUS
    estatus_counts = df_filtrado['ESTATUS'].value_counts()

    graf_realizados = go.Figure(
        data=[
            go.Pie(
                labels=estatus_counts.index,
                values=estatus_counts.values,
                hoverinfo='label+value+percent',
                pull=[0.1 if i == 0 else 0 for i in range(len(estatus_counts))]
            )
        ]
    )
    graf_realizados.update_layout(
        title='Porcentaje de Mantenimientos Preventivos Realizados',
        template='plotly_dark',
        showlegend=True
    )

    return graf_realizados

if __name__ == '__main__':
    mtto.run(debug=True, port='8054')
