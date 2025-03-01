from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from recommendations import recommendations_layout
from home import home_layout
from dashboard import dashboard_layout

app = Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP], 
    suppress_callback_exceptions=True,
    title="Recsic 🎵"
)

# Asignar el layout de la aplicación
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Para controlar las rutas
    html.Div(id='page-content')  # Aquí se mostrará el contenido de cada página
])

# Callback para cambiar el contenido según la ruta
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/recommendations':
        return recommendations_layout  # Redirige a la página de recomendaciones
    elif pathname == '/dashboard':  # Agrega la ruta para el dashboard
        return dashboard_layout  # Redirige a la página de dashboard
    else:
        return home_layout  # Página de inicio por defecto

if __name__ == '__main__':
    app.run_server(debug=True)


