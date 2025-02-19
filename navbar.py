import dash_bootstrap_components as dbc

def create_navbar():
    
    # Create the Navbar using Dash Bootstrap Components
    navbar = dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu", # Label given to the dropdown menu
                children=[
                    dbc.DropdownMenuItem("Home", href='/'),
                    dbc.DropdownMenuItem("Artistes", href='/page-2'),
                    dbc.DropdownMenuItem("Ecouter", href='/page-3'),
                    dbc.DropdownMenuItem("Regarder", href='/page-4'),
                    dbc.DropdownMenuItem("Recommandations", href='/page-5')
                ],
            ),
        ],
    brand="Home",
    brand_href="/",
    sticky="top",
    color="dark",
    dark=True,
    className='navbar-custom'
    )

    return navbar