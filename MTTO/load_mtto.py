import pandas as pd

sheets = {
    'PREVENTIVO 2024': 'A:G',
    'PREVENTIVO 2025': 'A:G'
}
dfs = []
for sheet_name, usecols in sheets.items():
	try:
		dfs.append(
			pd.read_excel(
			r"//192.168.10.2/Compartidos/Mantenimiento (192.168.10.254)/KPI'S.xlsx",
				keep_default_na=True,
				sheet_name=sheet_name,
				usecols=usecols,
    			header=0
				)
			)
	except Exception as e:
		continue

	dfs = pd.concat(dfs, ignore_index=True)

df = dfs
df.columns = df.columns.str.strip()
df = df.dropna(subset=['FECHA'])
df = df.sort_values(by=['FECHA'], ascending=False)
df['TIEMPO_RAW'] = pd.to_timedelta(df['TIEMPO'].astype(str), errors='coerce')
df['TIEMPO_RAW'] = df['TIEMPO_RAW'].fillna(pd.Timedelta(seconds=0))
df['TIEMPO'] = df['TIEMPO_RAW'].apply(lambda x: f"{int(x.total_seconds() // 3600):02}:{int((x.total_seconds() % 3600) // 60):02}")
df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce').dt.strftime('%d/%m/%Y')
df.rename(
    columns={
        'AGUDO1': 'AGUDO 1',
        'AGUDO2': 'AGUDO 2'
    },
    inplace=True
)
df['ESTATUS'] = df['ESTATUS'].replace('FS', 'FUERA DE SERVICIO')
df = df.apply(lambda x: x.str.strip() if x.dtype =='object' else x)
