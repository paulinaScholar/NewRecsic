from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

navbar = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("Recsic", href="/", className="text-white"),
        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        dbc.Collapse(
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Inicio", href="/")),
                dbc.NavItem(dbc.NavLink("Generador", href="/generator")),
                dbc.NavItem(dbc.NavLink("Recomendaciones", href="/recommendations")),
                dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard")),
                dbc.NavItem(dbc.NavLink("Perfil", href="perfil")),
            ], className="ms-auto"),
        id="navbar-collapse",
        navbar=True
        ),
    ]),
    color="primary",
    dark=True,
    className="navbar navbar-expand-lg bg-primary"
)
