import dash
import dash_bootstrap_components as dbc
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # très important pour rendez, sinon il ne lance pas le projet. Il a besoin d'un app.server
