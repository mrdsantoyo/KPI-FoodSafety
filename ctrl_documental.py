import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
import warnings
from pandas.errors import SettingWithCopyWarning

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=SettingWithCopyWarning)

df1 = []

sheets = {
    'Dirección General (A)': 'I:M',
    'I+D (A)': 'I:M',
    'SGIA (A)': 'I:M',
    'GOP (A) ': 'I:M',
    'ACI (A) ': 'I:M',
    'Almacen (A)  ': 'I:M',
    'Mantenimiento (A)  ': 'I:M',
    'TIC (A) ': 'I:M',
    'Producción (A)': 'I:M',
    'GCH': 'I:M',
    'Mercadotecnia (A)': 'I:M',
    'SMO (A) ': 'I:M',
    'Seguridad Patrimonial (A) ': 'I:M',
    'Sanidad (A)': 'I:M',
    'Contabilidad (A)': 'I:M',
    'Fiscal (A)': 'I:M',
    'Costos (A)': 'I:M',
    'Tesorería (A)': 'I:M',
    'Cuentas por Cobrar (A)': 'I:M',
    'Ventas (A) ': 'I:M',
    'Seguridad e Higiene (A)': 'I:M',
    'Compras (A)': 'I:M',
    'Control Vehicular (A) ': 'I:M',
    'Gerencia de Administración (A)': 'I:M',
    'Área Jurídica (A)': 'I:M',
    'Cultura Organizacional (A) ': 'I:M'
}

for sheet_name, usecols in sheets.items():
    df = pd.read_excel(
        'C:/Users/daniel.santoyo/KPI-EDA/Excel/Control de actualización de vigencia por documento D.xlsm',
        # "//192.168.10.2/Compartidos/SGI/Documentación/INDICADORES DE RECARGA/Control de actualización de vigencia por documento D.xlsm",
        sheet_name=sheet_name,
        usecols=usecols,
        skiprows=2,
        nrows=1
    )
    df['Departamento'] = sheet_name
    df1.append(df)
df1 = pd.concat(df1)
df1.rename(
    columns={x: x.replace('(A)', '').strip().capitalize() for x in df1.columns},
    inplace=True
)

df1 = df1.reset_index(drop=True).copy()

df1['Publicado'] = df1['Listos para publicar'].combine_first(df1['Publicados'])
df1['Publicado'] = df1['Publicado'].combine_first(df1['Publicado'])

dfs = df1[['Departamento', 'Publicado', 'En flujo', 'Ausencia', 'Vigencia v.', 'Rechazados']]
dfs['Departamento'] = dfs['Departamento'].str.replace(r'(A)', '').str.strip()

documentos = Dash(__name__)

documentos.layout = html.Div(
    children=[
        dcc.Dropdown(
            id='filtro-departamento',
            options=[{'label': i.upper(), 'value': i.upper()} for i in dfs['Departamento'].unique()],
            value=[],
            multi=True,
            placeholder="Selecciona un departamento",
            style={'width': '500px',
                'backgroundColor': '#2A2A2A'
                }
        ),
        dcc.Graph(
            id='control-documentos',
            style={
                'width': '500px',
                'height': '500px'
            }
        )
    ]
)
@documentos.callback(
    Output('control-documentos', 'figure'),
    Input('filtro-departamento', 'value')
)
def update_graph(filtro_departamento):
    # Filtrar los datos por departamento si hay filtro seleccionado
    if filtro_departamento:
        df_filtrado = dfs[dfs['Departamento'].isin(filtro_departamento)]
    else:
        df_filtrado = dfs

    # Sumar los valores por estado documental
    total = df_filtrado[['Publicado', 'En flujo', 'Ausencia', 'Vigencia v.', 'Rechazados']].sum()

    labels = total.index.tolist()
    values = total.values.tolist()

    # Crear el gráfico de pastel
    control_documental = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                textinfo='label+percent',
                insidetextorientation='radial',
                pull=[0.05] * len(labels)
            )
        ]
    )

    control_documental.update_layout(
        title='Control Documental',
        template='plotly_dark'
    )

    return control_documental

if __name__ == '__main__':
    documentos.run(debug=True, port='8053')
