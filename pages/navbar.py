from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

navbar = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("Recsic", href="/", className="text-white"),
        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        dbc.Collapse(
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Home", href="/", active=True)),
                dbc.NavItem(dbc.NavLink("Generator", href="/generator")),
                dbc.NavItem(dbc.NavLink("Recommendations", href="/recommendations")),
                dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard")),
                dbc.NavItem(dbc.NavLink("Profile", href="#")),
            ], className="ms-auto"),
        id="navbar-collapse",
        navbar=True
        ),
    ]),
    color="primary",
    dark=True,
    className="navbar navbar-expand-lg bg-primary"
)