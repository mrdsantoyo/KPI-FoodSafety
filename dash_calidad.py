import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import warnings
warnings.filterwarnings('ignore')
from ACI.load_aci import bpm_operativo_df, bpm_personal_df


filtro_area = [col for col in bpm_operativo_df.columns if col not in ['FECHA', 'PROMEDIOS DIARIOS']]


print(filtro_area)
# def actualizar_graficos(filtro_area, start_date, end_date):
#     return bpmoperativas(filtro_area, start_date, end_date), bpmpersonales(filtro_area, start_date, end_date)

# if __name__ == "__main__":
#     bpms.run(debug=True, port=8052)

