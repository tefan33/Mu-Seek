from dash import Dash, html

# Créer une instance de l'application Dash
app = Dash(__name__)

# Définir la mise en page de l'application
app.layout = html.Div(
    children=[
        html.H1("Bonjour"),
        html.P("Bienvenue sur cette page Dash simple !")
    ],
    style={'textAlign': 'center', 'marginTop': '50px'}
)

# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)