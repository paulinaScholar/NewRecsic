from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pages.recommendations import recommendations_layout
from pages.home import home_layout
from pages.dashboard import dashboard_layout
from pages.generator import generator_layout
from pages.login import login_layout
from pages.registro import registro_layout
from pages.inicio import inicio_layout
from pages.perfil import perfil_layout
from pages.navbar import navbar


external_stylesheets = [
    dbc.themes.PULSE,
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
]

app = Dash(
    __name__, 
    external_stylesheets=external_stylesheets, 
    suppress_callback_exceptions=True,
    title="Recsic 🎵"
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False), 
    navbar,
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)

def display_page(pathname):
    match pathname:
        case '/recommendations':
            return recommendations_layout 
        case '/dashboard':
                return dashboard_layout 
        case '/generator':
              return generator_layout
        case '/login':
              return login_layout 
        case '/registro':
              return registro_layout 
        case '/inicio':
              return inicio_layout
        case '/perfil':
              return perfil_layout
        case '/home':
              return home_layout
        case _:
            return inicio_layout 

if __name__ == '__main__':
    app.run(debug=True)
