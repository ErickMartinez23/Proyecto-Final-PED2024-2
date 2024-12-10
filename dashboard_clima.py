import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output


def dashboard_clima(app):
    # Leer los datos climáticos
    data = pd.read_csv("archivos/clima_tijuana_limpio.csv", encoding="utf-8")

    # Gráficos iniciales
    fig = px.line(data, x="Date", y=["Temperatura Máxima", "Temperatura Mínima"],
                  title="Tendencias de Temperaturas", template="plotly_dark")
    fig_box = px.box(data, y=["Temperatura Máxima", "Temperatura Mínima"],
                     title="Distribución de Temperaturas", template="plotly_dark")

    # Layout del Dashboard
    layout = html.Div(
        [
            dbc.Row(
                [
                    html.H2("Dashboard Climático de Tijuana", style={"color": "white"}),
                    dcc.Dropdown(
                        options=[
                            {"label": "Todo", "value": "all"},
                            {"label": "Temperatura Máxima", "value": "Temperatura Máxima"},
                            {"label": "Temperatura Mínima", "value": "Temperatura Mínima"},
                            {"label": "Condición Climática", "value": "Condición Climática"},
                        ],
                        value="all",
                        id="dropdown-variable"
                    ),
                    html.Hr(),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=fig, id="line-graph"), width=6),
                    dbc.Col(dcc.Graph(figure=fig_box, id="box-plot"), width=6),
                ]
            ),
        ],
        style={"background-color": "#000000", "padding": "20px"}
    )

    # Callback para actualizar los gráficos
    @app.callback(
        [Output("line-graph", "figure"), Output("box-plot", "figure")],
        [Input("dropdown-variable", "value")]
    )
    def update_graphs(selected_variable):
        if selected_variable == "all":
            selected_columns = ["Temperatura Máxima", "Temperatura Mínima"]
        else:
            selected_columns = [selected_variable]

        fig = px.line(
            data,
            x="Date",
            y=selected_columns,
            title="Tendencias de Temperaturas",
            template="plotly_dark"
        )

        fig_box = px.box(
            data,
            y=selected_columns,
            title="Distribución de Temperaturas",
            template="plotly_dark"
        )

        return fig, fig_box

    return layout
