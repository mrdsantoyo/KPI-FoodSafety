import pandas as pd

sheets = {
    'PREVENTIVO 2024': 'A:G',
    'PREVENTIVO 2025': 'A:G'
}

dfs = []
workbook = r"C:/Users/daniel.santoyo/KPI-EDA/Excel/KPI'S.xlsx"
# workbook = r"//192.168.10.2/Compartidos/Mantenimiento (192.168.10.254)/KPI'S.xlsx"
for sheet_name, usecols in sheets.items():
    try:
        df_temp = pd.read_excel(
            io=workbook,
            sheet_name=sheet_name,
            usecols=usecols,
            header=0,
            keep_default_na=True
        )
        dfs.append(df_temp)
    except Exception as e:
        print(f"Error en hoja {sheet_name}: {e}")
        continue

dfs = pd.concat(dfs, ignore_index=True)
df = dfs.loc[:, ~dfs.columns.duplicated()]

# Limpia los nombres de columnas y elimina duplicados resultantes
df.columns = df.columns.str.strip()
df = df.loc[:, ~df.columns.duplicated()]

df = df.dropna(subset=['FECHA'])
df = df.sort_values(by=['FECHA'], ascending=False)

def convertir_timedelta(val):
    try:
        if isinstance(val, pd.Timedelta):
            return val
        td = pd.to_timedelta(str(val), errors='coerce')
        return td if pd.notnull(td) else pd.Timedelta(seconds=0)
    except Exception:
        return pd.Timedelta(seconds=0)

df['TIEMPO_RAW'] = df['TIEMPO'].apply(convertir_timedelta)
df['TIEMPO'] = df['TIEMPO_RAW'].apply(
    lambda x: f"{int(x.total_seconds() // 3600):02}:{int((x.total_seconds() % 3600) // 60):02}"
)

df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce').dt.strftime('%d/%m/%Y')

df.rename(
    columns={
        'AGUDO1': 'AGUDO 1',
        'AGUDO2': 'AGUDO 2'
    },
    inplace=True
)

df['ESTATUS'] = df['ESTATUS'].replace('FS', 'FUERA DE SERVICIO')
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)


