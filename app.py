from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pages.recommendations import recommendations_layout
from pages.home import home_layout
from pages.dashboard import dashboard_layout
from pages.generator import generator_layout
from pages.navbar import navbar

app = Dash(
    __name__, 
    external_stylesheets=[dbc.themes.PULSE], 
    suppress_callback_exceptions=True,
    title="Recsic 🎵"
)

# Asignar el layout de la aplicación
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Para controlar las rutas 
    navbar,
    html.Div(id='page-content')  # Aquí se mostrará el contenido de cada página
])

# Callback para cambiar el contenido según la ruta
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)

def display_page(pathname):
    match pathname:
        case '/recommendations':
            return recommendations_layout  # Redirige a la página de recomendaciones
        case '/dashboard':  # Agrega la ruta para el dashboard
                return dashboard_layout  # Redirige a la página de dashboard
        case '/generator':
              return generator_layout #Redirige a la página de generador de lista musical
        case _:
                return home_layout  # Página de inicio por defecto

if __name__ == '__main__':
    app.run(debug=True)
