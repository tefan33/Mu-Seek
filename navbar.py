import dash_bootstrap_components as dbc
from dash import html

def create_navbar():
    # Chemin du logo (le fichier doit être dans le dossier "assets")
    logo_path = "/assets/logo.png"

    navbar = dbc.Navbar(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.A(
                            html.Img(src=logo_path, height="50px", style={"vertical-align": "middle"}),
                            href="/"
                        ),
                        width="auto",
                        style={'margin-left' : '60px', "margin-right": "auto"}
                    ),
                    dbc.Col(
                        html.H1(
                            "Mu'Seek",
                            style={
                                'font-family': 'calibri',
                                'color': 'white',
                                'font-size': '50px',
                                'margin': '0',
                                'text-align': 'center'
                            }
                        ),
                        width="auto",
                        style={"display": "flex", "justify-content": "center"}
                    ),
                    dbc.Col(
                        dbc.Nav(
                            [
                                dbc.DropdownMenu(
                                    nav=True,
                                    in_navbar=True,
                                    label="Menu",
                                    children=[
                                        dbc.DropdownMenuItem("Home", href='/'),
                                        dbc.DropdownMenuItem("Artistes", href='/artists'),
                                        dbc.DropdownMenuItem("Ecouter", href='/listen'),
                                        dbc.DropdownMenuItem("Recommandations", href='/reco'),
                                        dbc.DropdownMenuItem("Statistiques", href='/stats')
                                    ],
                                ),
                            ],
                            className="ml-auto",
                            navbar=True,
                        ),
                        width="auto",
                        style={"margin-left": "auto",
                               "color" : "white",
                               'margin-right' : '80px'}
                    ),
                ],
                className="w-100",
                align="center",
            ),
        ],
        color="dark",
        dark=True,
        sticky="top",
        className='navbar-custom',
        style={
            'background': 'radial-gradient(#3e823e, #171717 40%)',
            'z-index': '1000'
        }
    )

    return navbar
