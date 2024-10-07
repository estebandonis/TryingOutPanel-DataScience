import panel as pn
import pandas as pd
import hvplot.pandas

# Activar extensiones de Panel
pn.extension()

# Leer el archivo Excel
data_consumo_new = pd.read_excel('consumo.xlsx')
data_consumo_new.drop(columns=['Aceites lubricantes'], inplace=True)

# Asegurarse de que la columna 'Fecha' sea de tipo datetime
data_consumo_new['Fecha'] = pd.to_datetime(data_consumo_new['Fecha'], errors='coerce')

# Extraer el año de la columna 'Fecha'
data_consumo_new['Año'] = data_consumo_new['Fecha'].dt.year

# Crear un selector para elegir el año
year_selector = pn.widgets.Select(name='Año', options=list(data_consumo_new['Año'].unique()))

# Crear widgets para seleccionar las columnas a visualizar en el nuevo dataset
x_selector_new = pn.widgets.Select(name='Eje X', options=['Fecha'], value='Fecha')
y_selector_new = pn.widgets.Select(name='Eje Y', options=list(data_consumo_new.columns[1:]))


# Función para generar gráficos interactivos para el nuevo dataset
@pn.depends(x_selector_new.param.value, y_selector_new.param.value)
def plot_consumo_new(x_col, y_col):
    if x_col and y_col:
        return data_consumo_new.hvplot.line(x='Fecha', y=y_col, title=f'Consumo de {y_col} a lo largo del tiempo')
    return "Por favor seleccione ambas columnas."

# Función para generar la gráfica de barras por año
@pn.depends(year_selector.param.value)
def plot_consumo_por_año(selected_year):
    if selected_year:
        # Filtrar los datos para el año seleccionado
        data_year = data_consumo_new[data_consumo_new['Año'] == selected_year]
        
        # Sumar el consumo por categoría para el año seleccionado
        data_year_sum = data_year.drop(columns=['Fecha', 'Año', 'Total']).sum()
        
        # Crear un DataFrame para la gráfica de barras
        data_barras = pd.DataFrame({'Categoría': data_year_sum.index, 'Consumo': data_year_sum.values})
        
        # Crear la gráfica de barras con tamaño personalizado
        return data_barras.hvplot.bar(x='Categoría', y='Consumo', title=f'Consumo total por categoría en el año {selected_year}', rot=90, width=800, height=600)
    return "Por favor seleccione un año."

# Crear el layout del dashboard para el nuevo dataset
dashboard_new = pn.Column(
    pn.Row(x_selector_new, y_selector_new),
    plot_consumo_new,
    pn.Row(year_selector),
    plot_consumo_por_año
)

# Ejecutar el servidor de Panel
dashboard_new.show()
