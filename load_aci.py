##CARGA EL DOCUMENTO y regresa dfs, bpm_operativo_df, bpm_personal_df  (DATA FRAMES)
import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
##### LIBERACIÓN de PT ######   regresa DF "dfs"
dfs = []
sheets = {"CHICHARRÓN PRENSADO": "A,C:F,L:Q,S,T,X:AF",
          "PELLET": "A,C:F,L:Q,S,T,X:AJ",
          "PORCIONADOS": "A,C:E,K:O,Q,R,V:AA",
          "EMBUTIDOS": "A,C:E,K:Q,S,T,X:AB",
          "MANTECA": "A,C:E,J:Q,S,T,X:AF",
          "AHUMADOS": "A,C:F,L,N:Q,S,T,X:AC",
          "CARNE PARA HAMBURGUESA Y MOLIDA": "A,C:E,K:O,Q,R,V:Z",
          "ARRACHERA": "A,C:E,K:P,R,S,W:AB",
          "COCIDOS Y ESTERILIZADOS": "A,C:D,F,G,M:Q,S,T,X:AE"}

for sheet_name, usecols in sheets.items():
    try:
        dfs.append(
            pd.read_excel(
                "//192.168.10.2/Compartidos/Calidad Compartida (192.168.10.254)/8. BITACORA DE LIBERACIÓN DE PT Y MP/D-FTO-ACI-083 Bitácora de liberación de PT 2025.xlsx",  #remoto
                # "Excel/Bitácora de liberación de PT.xlsx",   #Local
                keep_default_na=True,
                sheet_name=sheet_name,
                skiprows=8,   #remoto, quitar para local.
                usecols=usecols
                )
            )

    except Exception as e:
        continue

#### BPM's OPERATIVAS #####   regresa DF "bpm_operativo_df"
bpm_operativo = []
fechas = []
ruta_bpm_local="Excel/Bitacora de BPM's 2024.xlsx"
sheets = {
    "ENERO": "A:J",
    "FEBRERO": "A:J",
    "MARZO": "A:K",
    "ABRIL": "A:K",
    "MAYO": "A:K",
    "JUNIO": "A:K",
    "JULIO": "A:K",
    "AGOSTO": "A:K",
    "SEPTIEMBRE": "A:K",
    "OCTUBRE": "A:K",
    "NOVIEMBRE": "A:K",
    "DICIEMBRE": "A:K"
}
for sheet, usecols in sheets.items():
    try:
        temp_df = pd.read_excel(
            "//192.168.10.2/Compartidos/Calidad Compartida (192.168.10.254)/5. KPI´s calidad/2025/Bitacora de BPM'S 2025.xlsx",
            # ruta_bpm_local,  #Local
            sheet_name=sheet,
            usecols=usecols,
            skiprows=[0, 2],
            nrows=18
        )
        fechas.extend(temp_df.columns[1:])
    except Exception as e:
        continue    
    
    temp_df = temp_df.T
    temp_df.columns = temp_df.iloc[0]  # Asignar encabezados desde la primera fila
    temp_df = temp_df[1:]  # Eliminar la fila de encabezados original
    bpm_operativo.append(temp_df)

bpm_operativo_df = pd.concat(bpm_operativo, ignore_index=True)
fechas_df = pd.DataFrame({'FECHA': fechas})

if len(bpm_operativo_df) == len(fechas_df):
    bpm_operativo_df['FECHA'] = fechas_df['FECHA'].values
else:
    raise ValueError("Los DataFrames no tienen el mismo número de filas. Verifica los datos.")

#### BPM's PERSONAL ######   regresa DF "bpm_personal_df"
bpm_personal = []
personal_df_list = []
for sheet, usecol in sheets.items():
    try:
        temp_df = pd.read_excel(
            "//192.168.10.2/Compartidos/Calidad Compartida (192.168.10.254)/5. KPI´s calidad/2025/Bitacora de BPM'S 2025.xlsx",            
            # ruta_bpm_local,  # Ruta local
            sheet_name=sheet,
            usecols=usecol,
            skiprows=list(range(24))  # Saltar filas irrelevantes
        )
        if temp_df.empty:
            print(f"La hoja {sheet} está vacía.")
            continue

        temp_df = temp_df.drop(index=0, errors='ignore')
        temp_df = temp_df.T

        temp_df.columns = temp_df.iloc[0]
        temp_df = temp_df[1:]  # Eliminar la fila usada como encabezado
        temp_df.columns = temp_df.columns.str.upper()

        temp_df.index = pd.to_datetime(temp_df.index, errors='coerce')
        temp_df['FECHA'] = temp_df.index

        columnas = ['FECHA'] + [col for col in temp_df.columns if col != 'FECHA']
        temp_df = temp_df[columnas]

        personal_df_list.append(temp_df)
        
    except Exception as e:
        continue

bpm_personal_df = pd.concat(personal_df_list, ignore_index=True)

