import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

inicio_layout = dbc.Container(
    fluid=True,
    className="inicio-container",
    children=[
        dbc.Row(
            className="header align-items-center py-3 px-4",
            style={"background-color": "#f5f6fa"},
            children=[
                dbc.Col(
                    html.Div(
                        html.Img(
                            src="/static/Recsic-11.png",
                            className="logo",
                            alt="Logo",
                            style={"height": "80px"}
                        ),
                        className="logo-container"
                    ),
                    width="auto"
                ),

                dbc.Col(),

                dbc.Col(
                    html.Div(
                        [
                            dbc.Button(
                                "Perfil",
                                href="/perfil",
                                color="primary",
                                className="me-3 custom-button"
                            ),
                            dbc.Button(
                                "Cerrar sesión",
                                href="/logout",
                                color="danger",
                                className="custom-button"
                            )
                        ],
                        className="d-flex justify-content-end"
                    ),
                    width="auto"
                ),
            ]
        ),

        dbc.Row(
            className="hero align-items-center text-center my-5 py-5 px-3",
            style={"background": "linear-gradient(to right, #ffffff, #dbe6fd)", "border-radius": "15px"},
            children=[
                dbc.Col(
                    [
                        html.H1(
                            "Bienvenido a Recsic",
                            className="display-3 fw-bold",
                            style={"color": "#1a1a2e"}
                        ),
                        html.P(
                            "Accede a tus estadísticas, perfil y descubre nuevas recomendaciones.",
                            className="lead",
                            style={"font-size": "1.3rem", "color": "#162447"}
                        ),
                        dbc.Button("Comenzar", href="/dashboard", color="primary", className="mt-3 px-4 py-2 custom-button")
                    ],
                    md=6,
                    className="text-md-start mb-4 mb-md-0"
                ),
                dbc.Col(
                    html.Img(
                        src="/static/Recsic_Mesa de trabajo 1.png",
                        className="img-fluid rounded shadow-lg",
                        style={"max-height": "400px"}
                    ),
                    md=6
                )
            ]
        ),

        dbc.Row(
            className="my-5 gy-4 px-2",
            children=[
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardImg(
                                src="/static/stats.png",
                                top=True,
                                className="p-3 card-img-hover",
                                style={"height": "200px", "object-fit": "contain"}
                            ),
                            dbc.CardBody(
                                [
                                    html.H4("Tus estadísticas", className="card-title"),
                                    html.P(
                                        "Explora tus métricas musicales y descubre nuevas tendencias.",
                                        style={"font-size": "0.95rem"}
                                    ),
                                    dbc.Button(
                                        "Ver estadísticas",
                                        href="/dashboard",
                                        color="primary",
                                        className="mt-2 w-100 custom-button"
                                    ),
                                ]
                            ),
                        ],
                        className="h-100 shadow rounded-4 card-hover"
                    ),
                    md=6, lg=4
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardImg(
                                src="/static/music.png",
                                top=True,
                                className="p-3 card-img-hover",
                                style={"height": "200px", "object-fit": "contain"}
                            ),
                            dbc.CardBody(
                                [
                                    html.H4("Explorar música", className="card-title"),
                                    html.P(
                                        "Descubre nuevas canciones y artistas recomendados.",
                                        style={"font-size": "0.95rem"}
                                    ),
                                    dbc.Button(
                                        "Explorar",
                                        href="/explorar",
                                        color="success",
                                        className="mt-2 w-100 custom-button"
                                    ),
                                ]
                            ),
                        ],
                        className="h-100 shadow rounded-4 card-hover"
                    ),
                    md=6, lg=4
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardImg(
                                src="/static/settings.png",
                                top=True,
                                className="p-3 card-img-hover",
                                style={"height": "200px", "object-fit": "contain"}
                            ),
                            dbc.CardBody(
                                [
                                    html.H4("Configuración", className="card-title"),
                                    html.P(
                                        "Personaliza tu experiencia y ajusta tus preferencias.",
                                        style={"font-size": "0.95rem"}
                                    ),
                                    dbc.Button(
                                        "Configurar",
                                        href="/perfil",
                                        color="secondary",
                                        className="mt-2 w-100 custom-button"
                                    ),
                                ]
                            ),
                        ],
                        className="h-100 shadow rounded-4 card-hover"
                    ),
                    md=6, lg=4
                ),
            ]
        )
    ]
)
