from load_mtto import df
import pandas as pd
from dash import Dash, html, dash_table
import warnings

warnings.filterwarnings("ignore")

df = df.dropna(subset=['FECHA'])
df= df.drop(columns=['TIEMPO_RAW', 'SEMANA', 'TIEMPO'])
df['FECHA'] = pd.to_datetime(df['FECHA']).dt.strftime('%d/%m/%Y')
df['ESTATUS'] = df['ESTATUS'].astype(str).str.strip().str.upper()
df1 = df[df['ESTATUS'] != 'REALIZADO']
df1 = df1.sort_values(by='FECHA', ascending=False)

app = Dash(__name__)
app.layout = html.Div(
	children=[
		html.H2(
			children='Reporte de mantenimientos reprogramados',
			style={
				'fontFamily': 'Arial, sans-serif',
				'color': 'black',
				'fontSize': '24px',
				'fontWeight': 'bold',
				'textAlign': 'center',
				'paddingTop': '20px'
			}
		),
		dash_table.DataTable(
			id='tabla-mttos',
			columns=[{"name": i, "id": i} for i in df1.columns],
			data=df1.to_dict('records'),
			filter_action="native",  # Agrega barra de búsqueda
			style_table={
				'width': '750px',  # 🔹 Ajusta el ancho de la tabla
				'margin': '0 auto',  # 🔹 Centra la tabla horizontalmente
				'height': '600px',  # 🔹 Ajusta la altura máxima
				'overflowY': 'auto',  # 🔹 Agrega scroll vertical
				# 'backgroundColor': '#2b2b2b'
			},
			style_cell={
				'minWidth': '100px', 
				'maxWidth': '200px', 
				'width': 'auto',
				'whiteSpace': 'normal',
				'textAlign': 'center',
				'fontFamily': 'Arial, sans-serif',
				'fontSize': '14px',
				'backgroundColor': '#2b2b2b'
			},
			style_header={
				'backgroundColor': 'black',
				'color': 'white',
				'fontWeight': 'bold',
				'textAlign': 'center',
				'backgroundColor': '#2b2b2b'
			},
			style_data_conditional=[
				{  
					'if': {'filter_query': "{ESTATUS} = 'FUERA DE SERVICIO'"},
					'backgroundColor': 'yellow',#'#ff9e1c',
					'color': 'black'
				},
				{
					'if': {'filter_query': "{ESTATUS} = 'REPROGRAMADO'"},
					'backgroundColor': 'red',#'#9d2626',
					'color': 'white'
				},
				{
					'if': {'filter_query': "{ESTATUS} = 'CANCELADO'"},
					'backgroundColor': 'gray',
					'color': 'white'
				},
				{
					'if':{'filter_query':"{ESTATUS} = 'PROGRAMADO'"},
					'backgroundColor': 'white',
					'color': 'black',
					'fontWeight':'bold'
				}
			]
		)
	],
	style={
		'width': '750px',  
		'margin': '0 auto' 
	}
)

if __name__ == '__main__':
	app.run(debug=True, port='8055')
