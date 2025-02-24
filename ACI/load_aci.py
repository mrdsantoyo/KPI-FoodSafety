import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

##### LIBERACIÓN de PT ######   regresa DF "dfs"
dfs = []
sheets = {
    "CHICHARRÓN PRENSADO": "A,C:F,L:Q,S,T,X:AF",
    "PELLET": "A,C:F,L:Q,S,T,X:AJ",
    "PORCIONADOS": "A,C:E,K:O,Q,R,V:AA",
    "EMBUTIDOS": "A,C:E,K:Q,S,T,X:AB",
    "MANTECA": "A,C:E,J:Q,S,T,X:AF",
    "AHUMADOS": "A,C:F,L,N:Q,S,T,X:AC",
    "CARNE PARA HAMBURGUESA Y MOLIDA": "A,C:E,K:O,Q,R,V:Z",
    "ARRACHERA": "A,C:E,K:P,R,S,W:AB",
    "COCIDOS Y ESTERILIZADOS": "A,C:D,F,G,M:Q,S,T,X:AE"
}

for sheet_name, usecols in sheets.items():
    try:
        df = pd.read_excel(
            "//192.168.10.2/Compartidos/Calidad Compartida (192.168.10.254)/8. BITACORA DE LIBERACIÓN DE PT Y MP/D-FTO-ACI-083 Bitácora de liberación de PT 2025.xlsx",
            sheet_name=sheet_name,
            skiprows=8,
            usecols=usecols
        )
        dfs.append(df)
    except Exception as e:
        print(f"Error cargando {sheet_name}: {e}")

##### BPM's OPERATIVO ######
bpm_operativo_list = []
sheets = {
    "ENERO": "A:O",
    "FEBRERO": "A:J",
    "MARZO": "A:k",
    "ABRIL": "A:K",
    "MAYO": "A:L",
    "JUNIO": "A:K",
    "JULIO": "A:K",
    "AGOSTO": "A:K",
    "SEPTIEMBRE": "A:K"
}

bpm_operativo_df = pd.DataFrame()

try:
    xls = pd.ExcelFile("\\192.168.10.2\Compartidos\Calidad Compartida (192.168.10.254)\5. KPI´s calidad\2025\Bitacora de BPM's 2025.xlsx") 
    for sheet_name, usecols in sheets.items():
        if sheet_name in xls.sheet_names:
            try:
                temp_df = pd.read_excel(xls, sheet_name=sheet_name, usecols=usecols, skiprows=24)
                temp_df['MES'] = sheet_name  # Agregar el nombre del mes para identificación
                bpm_operativo_df = pd.concat([bpm_operativo_df, temp_df], ignore_index=True)
            except Exception as e:
                print(f"⚠️ Error procesando BPM operativo en {sheet_name}: {e}")
        else:
            print(f"❌ Hoja {sheet_name} no encontrada, se omite.")
except Exception as e:
    print(f"🚨 Error general al cargar BPM operativo: {e}")



bpm_operativo_df = pd.concat(bpm_operativo_list, ignore_index=True) if bpm_operativo_list else pd.DataFrame()

##### BPM's PERSONAL ######
bpm_personal_list = []
sheets = {
    "ENERO": "A:O",
    "FEBRERO": "A:J",
    "MARZO": "A:k",
    "ABRIL": "A:K",
    "MAYO": "A:L",
    "JUNIO": "A:K",
    "JULIO": "A:K",
    "AGOSTO": "A:K",
    "SEPTIEMBRE": "A:K"
}
bpm_personal_df = pd.DataFrame()

try:
    for sheet_name, usecols in sheets.items():
        if sheet_name in xls.sheet_names:
            try:
                temp_df = pd.read_excel(xls, sheet_name=sheet_name, usecols=usecols, skiprows=24)
                temp_df['MES'] = sheet_name  # Agregar el nombre del mes para identificación
                bpm_personal_df = pd.concat([bpm_personal_df, temp_df], ignore_index=True)
            except Exception as e:
                print(f"⚠️ Error procesando BPM personal en {sheet_name}: {e}")
        else:
            print(f"❌ Hoja {sheet_name} no encontrada, se omite.")
except Exception as e:
    print(f"🚨 Error general al cargar BPM personal: {e}")

print(f"✅ BPM Operativo cargado con {bpm_operativo_df.shape[0]} filas y {bpm_operativo_df.shape[1]} columnas.")
print(f"✅ BPM Personal cargado con {bpm_personal_df.shape[0]} filas y {bpm_personal_df.shape[1]} columnas.")
