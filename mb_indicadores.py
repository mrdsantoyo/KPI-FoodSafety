import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import warnings
from load_aci import dfs


warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

dfs = pd.concat(dfs, ignore_index=True)

# Procesamiento de datos para Mesofílicos
dfs.columns = dfs.columns.str.strip().str.replace('\n', ' ')
df_mesofilicos = dfs.loc[:, ['Folio', 'Producto', 'Fecha de siembra', 'Mesofilicos <10,000 UFC/g', 'Cta. Total Mesofilicos  <10,000 UFC/g']].copy()

df_mesofilicos.rename(
    columns={
        'Mesofilicos <10,000 UFC/g': 'Mesofilicos_1',
        'Cta. Total Mesofilicos  <10,000 UFC/g': 'Mesofilicos_2'
    },
    inplace=True
)

df_mesofilicos['Mesofilicos (UFC/g)'] = df_mesofilicos['Mesofilicos_1'].combine_first(df_mesofilicos['Mesofilicos_2'])
df_mesofilicos['Mesofilicos (UFC/g)'] = df_mesofilicos['Mesofilicos (UFC/g)'].replace('INC', 55500)
df_mesofilicos['Mesofilicos (UFC/g)'] = pd.to_numeric(df_mesofilicos['Mesofilicos (UFC/g)'], errors='coerce').fillna(0)
df_mesofilicos['Fecha de siembra'] = pd.to_datetime(df_mesofilicos['Fecha de siembra'], errors='coerce')

df_mesofilicos['Producto'] = df_mesofilicos['Producto'].apply(lambda x: x.split('/')[-1] if isinstance(x, str) else x)

# Procesamiento de datos para Coliformes
df_coliformes = dfs.loc[:, ['Folio', 'Producto', 'Fecha de siembra', 'Cta. Total Coliformes  <10 UFC/g', 'Coliformes  <10 UFC/g',
                            'Cta. Total Coliformes  <5000 UFC/g', 'Cta. Total Coliformes  <5,000 UFC/g', 'Mesofilicos <10,000 UFC/g', 'Cta. Total Mesofilicos  <10,000 UFC/g']].copy()

df_coliformes.rename(
    columns={
        'Cta. Total Coliformes  <10 UFC/g': 'coliformes_1',
        'Coliformes  <10 UFC/g': 'coliformes_2',
        'Cta. Total Coliformes  <5000 UFC/g': 'coliformes_3',
        'Cta. Total Coliformes  <5,000 UFC/g': 'coliformes_4',
        'Mesofilicos <10,000 UFC/g': 'Mesofilicos_1',
        'Cta. Total Mesofilicos  <10,000 UFC/g': 'Mesofilicos_2'
    },
    inplace=True
)

df_coliformes['Coliformes (<10 UFC/g)'] = df_coliformes['coliformes_1'].combine_first(df_coliformes['coliformes_2'])
df_coliformes['Coliformes (<10 UFC/g)'] = df_coliformes['Coliformes (<10 UFC/g)'].replace('INC', 2100)
df_coliformes['Coliformes (<10 UFC/g)'] = pd.to_numeric(df_coliformes['Coliformes (<10 UFC/g)'], errors='coerce').fillna(0)


df_coliformes["Coliformes (<5'000 UFC/g)"] = df_coliformes['coliformes_3'].combine_first(df_coliformes['coliformes_4'])
df_coliformes["Coliformes (<5'000 UFC/g)"] = df_coliformes["Coliformes (<5'000 UFC/g)"].replace('INC', 100000)
df_coliformes["Coliformes (<5'000 UFC/g)"] = pd.to_numeric(df_coliformes["Coliformes (<5'000 UFC/g)"], errors='coerce').fillna(0)

df_coliformes['Mesofilicos (UFC/g)'] = df_coliformes['Mesofilicos_1'].combine_first(df_coliformes['Mesofilicos_2'])
df_coliformes['Mesofilicos (UFC/g)'] = df_coliformes['Mesofilicos (UFC/g)'].replace('INC', 55500)
df_coliformes['Mesofilicos (UFC/g)'] = pd.to_numeric(df_coliformes['Mesofilicos (UFC/g)'], errors='coerce').fillna(0)

productos_unicos = df_mesofilicos['Producto'].dropna().unique()
# productos_unicos = [producto for producto in productos_unicos if producto is not None]

filtro = [{'label': producto, 'value': producto} for producto in productos_unicos if producto is not None]

# indicadores_mb Dash
indicadores_mb = Dash(__name__)

indicadores_mb.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=3600*1000,
        n_intervals=0
    ),
    dcc.Dropdown(
        id='producto-filter',
        options=filtro,
        # value=None,
        placeholder="Selecciona un producto",
        multi=True,
        style={'width': '750px',
               'backgroundColor': '#1A1A1A'
               },
    ),
    dcc.Graph(
        id='mesofilicos-graf',
        style={'width': '750px', 'height': '300px'}
    ),
    dcc.Graph(
        id='coliformes-10-graf',
        style={'width': '750px', 'height': '300px'}
    ),
    dcc.Graph(
        id='coliformes-5-graf',
        style={'width': '750px', 'height': '300px'}
    )
])

@indicadores_mb.callback(
    [Output('mesofilicos-graf', 'figure'),
     Output('coliformes-10-graf', 'figure'),
     Output('coliformes-5-graf', 'figure')],
    [Input('interval-component', 'n_intervals'),
     Input('producto-filter', 'value')]
)

def graficos(n_intervals, producto_filter):
    # Filtrar los productos seleccionados
    if producto_filter:
        df_mesofilicos_filtrado = df_mesofilicos[df_mesofilicos['Producto'].isin(producto_filter)]
        df_coliformes_filtrado = df_coliformes[df_coliformes['Producto'].isin(producto_filter)]
    else:
        df_mesofilicos_filtrado = df_mesofilicos.sort_values(by=['Mesofilicos (UFC/g)'], ascending=True).head()
        df_coliformes_filtrado = df_coliformes.sort_values(by=['Mesofilicos (UFC/g)'], ascending=True).head()

    # Gráfico de Mesofílicos
    mesofilicos_fig = go.Figure()
    if producto_filter is None:
        mesofilicos_fig.add_annotation(
            text="Selecciona un producto para filtrar",
            font=dict(size=14),
            showarrow=False,
            yref='paper'
            )
        mesofilicos_fig.update_yaxes(range=[0,10000])

    for producto in df_mesofilicos_filtrado['Producto'].unique():
        df_producto = df_mesofilicos_filtrado[df_mesofilicos_filtrado['Producto'] == producto]
        df_agrupado = df_producto.groupby('Fecha de siembra', as_index=False)['Mesofilicos (UFC/g)'].mean()
        mesofilicos_fig.add_trace(
            go.Scatter(
                x=df_agrupado['Fecha de siembra'],
                y=df_agrupado['Mesofilicos (UFC/g)'],
                mode='markers',
                name=producto
            )
        )
        mesofilicos_fig.add_trace(
            go.Scatter(
                x=['2024-01-01', '2024-12-31'],
                y=[10000, 10000],
                mode='lines',
                name="Límite 10,000 UFC/g",
                hoverinfo='name',
                line=dict(color='red', dash='dash')
            )
        )

    mesofilicos_fig.update_layout(
        title='Tendencia de Mesofílicos (<10,000 UFC/g)',
        xaxis_title='Fecha',
        yaxis_title='Mesofílicos (UFC/g)',
        template='plotly_dark',
        showlegend=False
    )

    # Gráfico de Coliformes (<10 UFC/g)
    coliformes_10_fig = go.Figure()
    if producto_filter is None:
        coliformes_10_fig.add_annotation(
            text="Selecciona un producto para filtrar",
            font=dict(size=14),
            showarrow=False,
            yref='paper'
            )
        coliformes_10_fig.update_yaxes(range=[0,10])

    for producto in df_coliformes_filtrado['Producto'].unique():
        df_producto = df_coliformes_filtrado[df_coliformes_filtrado['Producto'] == producto]
        df_agrupado_10 = df_producto.groupby('Fecha de siembra', as_index=False)['Coliformes (<10 UFC/g)'].mean()
        coliformes_10_fig.add_trace(
            go.Scatter(
                x=df_agrupado_10['Fecha de siembra'],
                y=df_agrupado_10['Coliformes (<10 UFC/g)'],
                mode='markers',
                name=producto
            )
        )
        coliformes_10_fig.add_trace(
            go.Scatter(
                x=['2024-01-01', '2024-12-31'],     
                y=[10, 10],
                mode='lines',
                name='Límite 10 UFC/g',
                hoverinfo='name',                
                line=dict(color='red', dash='dash')
            )
        )

    coliformes_10_fig.update_layout(
        title='Tendencia de Coliformes para productos cocidos (<10 UFC/g)',
        xaxis_title='Fecha',
        yaxis_title='Coliformes (<10 UFC/g)',
        template='plotly_dark',
        showlegend=False
    )

    # Gráfico de Coliformes (<5,000 UFC/g)
    coliformes_5_fig = go.Figure()
    if producto_filter is None:
        coliformes_5_fig.add_annotation(
            text="Selecciona un producto para filtrar",
            font=dict(size=14),
            showarrow=False,
            yref='paper'
            )
        coliformes_5_fig.update_yaxes(range=[0,5000])

    for producto in df_coliformes_filtrado['Producto'].unique():
        df_producto = df_coliformes_filtrado[df_coliformes_filtrado['Producto'] == producto]
        df_agrupado_5 = df_producto.groupby('Fecha de siembra', as_index=False)["Coliformes (<5'000 UFC/g)"].mean()
        coliformes_5_fig.add_trace(
            go.Scatter(
                x=df_agrupado_5['Fecha de siembra'],
                y=df_agrupado_5["Coliformes (<5'000 UFC/g)"],
                mode='markers',
                name=producto
            )
        )
    coliformes_5_fig.add_trace(
        go.Scatter(
            x=['2024-01-01', '2024-12-31'],
            y=[5000, 5000],
            mode='lines',
            name='Límite 5000 UFC/g',
            hoverinfo='name',
            line=dict(color='red', dash='dash')
        )
    )

    coliformes_5_fig.update_layout(
        title='Tendencia de Coliformes para productos crudos (<5,000 UFC/g)',
        xaxis_title='Fecha',
        yaxis_title='Coliformes (<5,000 UFC/g)',
        template='plotly_dark',
        showlegend=False
    )

    # Actualizar rangos de fechas en los ejes X
    mesofilicos_fig.update_xaxes(range=['2024-01-01', '2024-12-31'])
    coliformes_10_fig.update_xaxes(range=['2024-01-01', '2024-12-31'])
    coliformes_5_fig.update_xaxes(range=['2024-01-01', '2024-12-31']) 
    
    return mesofilicos_fig, coliformes_10_fig, coliformes_5_fig


if __name__ == '__main__':
    indicadores_mb.run(debug=True, port='8051')