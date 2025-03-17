import pandas as pd
import warnings
warnings.filterwarnings('ignore')

#####Control Documental - Estatus
def load_control_documental():
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
    # workbook="C:/Users/daniel.santoyo/KPI-EDA/Excel/Control de actualización de vigencia por documento D.xlsm"
    workbook="//192.168.10.2/Compartidos/SGI/Documentación/INDICADORES DE RECARGA/Control de actualización de vigencia por documento D.xlsm"
    for sheet_name, usecols in sheets.items():
        df = pd.read_excel(
            workbook,
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
    df_documentos = df1[['Departamento', 'Publicado', 'En flujo', 'Ausencia', 'Vigencia v.', 'Rechazados']].copy()
    df_documentos['Departamento'] = df_documentos['Departamento'].str.replace(r'(A)', '', regex=True).str.strip()
    df_documentos = df_documentos.fillna(0)     # ['Departamento', 'Publicado', 'En flujo', 'Ausencia', 'Vigencia v.', 'Rechazados']
    return df_documentos

###### TIF 
def load_tif():
    # workbook="Excel/Seguimiento TIF.xlsx"
    workbook="//192.168.10.2/Compartidos/SGI/GAP/Seguimiento Indicador TIF/Seguimiento TIF.xlsx"
    df = pd.read_excel(
        workbook,
        skiprows=2
        )
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    df['Fecha de cierre'] = pd.to_datetime(df['Fecha de cierre'], errors='coerce')
    df['Fecha compromiso'] = pd.to_datetime(df['Fecha compromiso'], errors='coerce')
    df['Días transcurridos'] = (pd.Timestamp.today() - df['Fecha']).dt.days
    df['Días propuestos'] = (df['Fecha compromiso']-df['Fecha']).dt.days
    df['Días propuestos'] = df['Días propuestos'].fillna(0)
    df['Retraso'] = df['Días transcurridos'] - df['Días propuestos']
    df['Mes'] = df['Fecha'].dt.month
    df['Mes'] = df['Mes'].map(
        {
            1:'Enero',
            2:'Febrero',
            3:'Marzo',
            4:'Abril',
            5:'Mayo',
            6:'Junio',
            7:'Julio',
            8:'Agosto',
            9:'Septiembre',
            10:'Octubre',
            11:'Noviembre',
            12:'Diciembre'
            }
        )
    return df

### Desviaciones pendientes x Mes
def desviaciones_x_mes():
    df1 = load_tif()
    df1 = df1.sort_values('Fecha', ascending=True)
    df1 = df1[df1['Estatus']=='CERRADA']
    df1 = df1.groupby('Mes')['Estatus'].count()

    df2 = load_tif()
    df2 = df2.sort_values('Fecha', ascending=True)
    df2 = df2[df2['Estatus']!='CERRADA']
    df2 = df2.groupby('Mes')['Estatus'].count()
    df3 = pd.concat([df1,df2], axis=1)
    df3.columns = ['Cerradas', 'Abiertas']
    df3['Cerradas'] = df3['Cerradas'].fillna(0)
    df3['%'] = ((df3['Cerradas'] / (df3['Cerradas']+df3['Abiertas']))*100).round(2)

    # df3
    return df3