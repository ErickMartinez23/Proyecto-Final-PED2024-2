import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Input, Output

# Cargar el archivo de datos climáticos
data = pd.read_csv("datos_climaticos/clima_tijuana_limpio.csv")

# Crear el layout del filtro
def filtros():
    tarjeta_filtros = dbc.Card(
        dbc.CardBody([
            html.Div([
                dbc.Label("Filtrar por condición climática:"),
                dcc.Dropdown(
                    id="ddlCondicion",
                    options=[{"label": cond, "value": cond} for cond in sorted(data['Condición Climática'].unique())],
                    value=None,
                    placeholder="Selecciona una condición climática"
                ),
            ]),
            html.Br(),
            html.Div([
                dbc.Label("Rango de fechas:"),
                dcc.DatePickerRange(
                    id="datePicker",
                    min_date_allowed=data['Fecha'].min(),
                    max_date_allowed=data['Fecha'].max(),
                    start_date=data['Fecha'].min(),
                    end_date=data['Fecha'].max()
                ),
            ])
        ])
    )
    return tarjeta_filtros

# Crear el layout del dashboard
def dashboard():
    body = html.Div([
        html.H2("Dashboard de Análisis Climático - Tijuana", style={"textAlign": "center", "color": "blue"}),
        html.P("Explora las tendencias climáticas de Tijuana a través de gráficos interactivos."),
        html.Hr(),
        dbc.Row([
            dbc.Col(filtros(), width=3),
            dbc.Col([
                dbc.Row([
                    dbc.Col(dcc.Graph(id="figTemperatura")),
                    dbc.Col(dcc.Graph(id="figCondiciones")),
                ]),
                dbc.Row([
                    dbc.Col(dcc.Graph(id="figPromedioMensual")),
                ]),
            ], width=9)
        ])
    ])
    return body

# Callback para actualizar gráficos
@callback(
    Output("figTemperatura", "figure"),
    Output("figCondiciones", "figure"),
    Output("figPromedioMensual", "figure"),
    Input("ddlCondicion", "value"),
    Input("datePicker", "start_date"),
    Input("datePicker", "end_date"),
)
def actualizar_graficos(condicion, start_date, end_date):
    # Filtrar los datos según la condición y el rango de fechas
    datos_filtrados = data.copy()
    if condicion:
        datos_filtrados = datos_filtrados[datos_filtrados['Condición Climática'] == condicion]
    if start_date and end_date:
        datos_filtrados = datos_filtrados[(datos_filtrados['Fecha'] >= start_date) & (datos_filtrados['Fecha'] <= end_date)]

    # Gráfico de temperatura máxima y mínima por fecha
    fig_temperatura = px.line(
        datos_filtrados,
        x="Fecha",
        y=["Temperatura Máxima", "Temperatura Mínima"],
        title="Evolución de Temperaturas Máxima y Mínima",
        labels={"value": "Temperatura (°C)", "variable": "Tipo de Temperatura"}
    )

    # Gráfico de frecuencia de condiciones climáticas
    fig_condiciones = px.bar(
        datos_filtrados['Condición Climática'].value_counts().reset_index(),
        x='index',
        y='Condición Climática',
        title="Frecuencia de Condiciones Climáticas",
        labels={"index": "Condición Climática", "Condición Climática": "Frecuencia"}
    )

    # Promedio mensual de temperatura
    datos_filtrados['Mes'] = pd.to_datetime(datos_filtrados['Fecha']).dt.month
    promedio_mensual = datos_filtrados.groupby('Mes')[['Temperatura Máxima', 'Temperatura Mínima']].mean().reset_index()
    fig_promedio_mensual = px.bar(
        promedio_mensual,
        x="Mes",
        y=["Temperatura Máxima", "Temperatura Mínima"],
        title="Promedio Mensual de Temperaturas",
        labels={"value": "Temperatura (°C)", "variable": "Tipo de Temperatura"}
    )

    return fig_temperatura, fig_condiciones, fig_promedio_mensual

# Configuración de la aplicación Dash
if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
    app.layout = dashboard()
    app.run_server(debug=True)
