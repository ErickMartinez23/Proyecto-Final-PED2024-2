from grafica1 import html


def welcome():
    body = html.Div(
        [
            html.H3("dashboard comparativo de clima de TIJ"),
            html.P("Objetivo: responder a 3 preguntas basado en la informacion extraida de la pagina web"),
            html.Hr(),
            html.H4("Listas Desordenadas"),
            html.Ul(
                [
                    html.Li("Martinez Gonzalez Erick"),
                    html.Li("Victor Alejandro lopez Sureaz"),
                    html.Li("joan 3")
                ]
            ),
            html.Hr(),
            html.H4("Lista ordenada de archivos realizados"),
            html.Ol(
                [
                    html.Li("webscrapper"),
                    html.Li("archivo csv con datos brutos"),
                    html.Li("script de base de datos"),
                    html.Li("codigo de limpieza"),
                    html.Li("archivo csv limpio"),
                    html.Li("ccodigo de lectura y subida de datos a BD"),
                    html.Li("ccodigos de estructura de dasboards"),
                    html.Li(" documentacion ")
                ]
            ),
            html.Hr(),
            html.H4("Ligas"),
            html.A(children="Github", href="https://github.com/ErickMartinez23/Proyecto-Final-PED2024-2",
                   target="_blank")

        ]
    )
    return body
