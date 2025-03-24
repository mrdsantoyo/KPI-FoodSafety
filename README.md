# KPI-FoodSafety

## Descripción del Proyecto

El objetivo de este proyecto es desarrollar dashboards interactivos para facilitar el monitoreo y análisis de indicadores clave de desempeño (KPIs) relacionados con la inocuidad alimentaria en procesos industriales. Utiliza Python con Dash Plotly, pandas y numpy para gestionar, analizar y visualizar información clave de manera dinámica y clara.

## Generación de Dashboards de Inocuidad (Food Safety) para industria.

🗃️ Los archivos load_XXXXXX.py corresponden a archivos Excel (.xls, .xlsx, .xlsm) ubicados en un servidor local, donde cada archivo de excel fue creado por usuarios básicos sin considerar su uso para analizar la información y con diferentes estilos de captura.

📋Los demás archivos ***.py*** en la misma carpeta organizan la información en DataFrames de **Pandas** y construyen funciones **Plotly** que generan las figuras.

📈Los gráficos son construidos con **Dash** en el fichero raíz como ***dash_XXXXXXX.py*** donde se llama a la función creada con **Plotly**  

## Características del Dashboard
- **Visualización interactiva** de datos utilizando Plotly y Dash.
- Procesamiento automatizado de archivos Excel.
- Gráficos dinámicos e interactivos para fácil interpretación de datos.
- Monitoreo en tiempo real de KPIs críticos relacionados con calidad y mantenimiento.

## Tecnologías Utilizadas

- **Python**
- **Dash (Plotly)**
- **Pandas**
- **NumPy**

## Estructura del proyecto

- `dash_calidad.py`: Dashboard para monitorear indicadores de calidad.
- `dash_mantenimiento.py`: Dashboard para gestión y seguimiento del mantenimiento.
- `eficiencia_mtto.py` y `porc_mtto.py`: Scripts que procesan datos relacionados con mantenimientos preventivos y su eficiencia.
- `mb_indicadores.py`: Análisis de indicadores microbiológicos como mesofílicos y coliformes.
- `BPM.py`: Análisis y visualización de Buenas Prácticas de Manufactura (BPM).
- `load_aci.py`: Carga automatizada de datos desde archivos Excel.

## Cómo Ejecutar el Proyecto
1. **Clonar el repositorio:**
```bash
git clone https://github.com/mrdsantoyo/KPI-FoodSafety.git
```
2. **Instalar dependencias:**
```bash
pip install pandas plotly dash numpy
```
3. **Ejecutar dashboards:**
Ejemplo para iniciar el dashboard de calidad:
```bash
python dash_calidad.py
```
Luego abre en tu navegador:
```
http://127.0.0.1:1111 #Para el Dashboard de Mantenimiento
http://127.0.0.1:1112 #Para el Dashboard de Aseguramiento de Calidad 
```
1. Haz un **fork** del repositorio.
2. Crea una rama para tu mejora o corrección (`git checkout -b feature/nueva-mejora`).
3. Realiza tus cambios y haz commit.
4. Envía tu rama al repositorio (`git push origin feature/nueva-mejora`).
5. Abre un pull request.

6. **Implementación del Dashboard** 
- [x] Dashboard Calidad
- [x] Dashboard Mantenimiento
- [ ] Dashboard SGIA (en desarrollo)

7. **Visualización del Dashboard**

![Dashboard mantenimiento](https://drive.google.com/uc?export=view&id=195cHAswBmxNXgAB0FwbcsXkBlXWbyGfY)

![Dashboard mantenimiento 0](https://drive.google.com/uc?export=view&id=1F5gm9SFGqt4aDOvxRBmjBhMGkGlrvK33)

![Dasboard mantenimiento 1](https://drive.google.com/uc?export=view&id=1C4Oc7Wi6tr4Htgte1B6DcbaCFpl-6KJL)

![Dashboard ACI](https://drive.google.com/uc?export=view&id=1SXdj0kxvZitSCu6T8VxdHK-bU2F0TEVl)

![Dasboard ACI 1](https://drive.google.com/uc?export=view&id=1jWAmZz-z4x8tPiiXpUIbxWNpr1xMmVxX)

## Uso y confidencialidad de datos
Los archivos fuente en formato Excel (.xlsx) utilizados para la generación de los dashboards y análisis presentados en este proyecto son propiedad intelectual de la organización y no están incluidos en este repositorio debido a temas de confidencialidad y privacidad. Dichos archivos son utilizados únicamente con fines ilustrativos y demostrativos del funcionamiento del código.

Si deseas utilizar el proyecto con tus propios datos, deberás adaptar las rutas y archivos según corresponda a tu entorno.

## Autor
Desarrollado por [Daniel Santoyo](https://github.com/mrdsantoyo).  
Contacto: danielsa00@gmail.com | LinkedIn: www.linkedin.com/in/daniel-santoyo00

**Este proyecto está licenciado bajo la Licencia MIT. Para más detalles, consulta el archivo `LICENSE`.
