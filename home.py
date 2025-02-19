from navbar import create_navbar
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from app import app
import pandas as pd
import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

nav = create_navbar()

################################ FICHIERS DE SCRAPP SNEP ################################

df_album = pd.read_csv('https://raw.githubusercontent.com/Yann-ML/PROJET_3_WCS/main/WEBSCRAP/df_top_album.csv')
df_album_week = pd.read_csv('https://raw.githubusercontent.com/Yann-ML/PROJET_3_WCS/main/WEBSCRAP/df_top_album_week.csv')
df_single_week = pd.read_csv('https://raw.githubusercontent.com/Yann-ML/PROJET_3_WCS/main/WEBSCRAP/df_top_single_week.csv')
df_single = pd.read_csv('https://raw.githubusercontent.com/Yann-ML/PROJET_3_WCS/main/WEBSCRAP/df_top_singles.csv')

# création d'un dict des dataframes

dataframes = {
    "Top Albums_Semaine": df_album_week,
    "Top Singles_Semaine": df_single_week,
    "Top Albums_Année": df_album,
    "Top Singles_Année": df_single
}

image_path = '/assets/logo.png'

# header pour ne pas être masqué par la navbar (à optimiser plus tard)

header = html.H3("-",
                 style={'opacity' : '0'})


################################ CREATION PAGE ACCUEIL ################################

def create_page_home():
    
    layout = html.Div([
        nav,  # Navbar en haut

        # Contenu principal
        html.Div([
            html.Img(
                src=image_path,
                style={
                    'width': '10%',
                    'position': 'absolute',
                    'left': '35px',
                    'top': '100%',
                    'transform': 'translateY(-50%)'
                }
            ),
            html.H1(
                "Mu'Seek",
                style={
                    'font-family': 'calibri',
                    'color': 'white',
                    'font-size': '60px',
                    'margin': '0 auto',
                    'text-align': 'center'
                }
            )
        ], style={
            'width': '100%',
            'background': 'radial-gradient(#3e823e, #171717 30%)',
            'z-index': '1000',
            'padding': '15px 0',
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'center',
            'margin-top' : '100px'
        }),

        # Div contenant les boutons et les dropdowns
        html.Div([
            html.Button("Top Albums_Semaine", id="btn-albums-week", n_clicks=0, className='button_style'),
            html.Button("Top Albums_Année", id="btn-albums-year", n_clicks=0, className='button_style'),
            html.Button("Top Singles_Semaine", id="btn-singles-week", n_clicks=0, className='button_style'),
            html.Button("Top Singles_Année", id="btn-singles-year", n_clicks=0, className='button_style'),
            html.Div([
                
                # années
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[],
                    value=None,
                    clearable=False,
                    className='dropdown_style'
                ),
                # semaines
                dcc.Dropdown(
                    id='week-dropdown',
                    options=[],
                    value=None,
                    clearable=False,
                    className='dropdown_style'
                ),
            ], style={
                'display': 'flex',
                'flex-direction': 'column',
                'gap': '10px',  # espace entre les dropdowns
                'margin-top': '20px'
            })
        ], style={'background-color': '#171717', 
                  "display": "flex", 
                  "flex-direction": "column", 
                  "align-items": "flex-start", 
                  "padding": "20px", 
                  "position": "fixed", 
                  "top": "100px",  # Assure-toi que c'est la hauteur de la navbar
                  "left": "0", 
                  "height": "calc(100vh - 100px)", 
                  "width": "210px", 
                  "overflow-y": "auto",
                  'margin-top' : '100px'}),

        # Div contenant le tableau de classement
        html.Div([
            dash_table.DataTable(
                id='table-top',
                columns=[
                    {'name': '', 'id': 'url_img', 'presentation': 'markdown'},
                    {'name': 'Rang', 'id': 'rang'},
                    {'name': 'Artiste', 'id': 'artiste'},
                    {'name': 'Album', 'id': 'album'},
                    {'name': 'Spotify', 'id': 'id_spotify', 'presentation': 'markdown'},
                ],
                page_size=20,
                style_table={'overflowX': 'auto', 'width': '90%', 'height': 'calc(100vh - 160px)'},
                style_cell={'textAlign': 'left', 'padding': '5px', 'fontSize': '16px', 'color': 'white',
                            'background-color': '#171717', "border": "none", 'font-family': 'calibri'},
                style_header={'fontSize': '16px','color': 'white', "border": "none",
                            'background-color': '#171717', 'fontWeight': 'bold', 'font-family': 'calibri'},
                style_data_conditional=[
                        {
                        'if': {'column_id': 'album'},
                        'whiteSpace': 'normal',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'maxWidth': '250px'
                        }
                ],
                markdown_options={"html": True},
            ),
        ], style={'margin-top' : '150px', 'position': 'fixed', 'top': '100px', 'left': '250px', 'right': '10px', 'bottom': '10px', 'overflow-y': 'auto'}),

    ], className='body')
    
    return layout


################################ CALLBACK ################################

# callback de MAJ des tableaux selon sélection
@app.callback(
    [Output('table-top', 'data'),
     Output('year-dropdown', 'options'), Output('year-dropdown', 'value'),
     Output('week-dropdown', 'options'), Output('week-dropdown', 'value')],
    [Input('btn-albums-week', 'n_clicks'),
     Input('btn-albums-year', 'n_clicks'),
     Input('btn-singles-week', 'n_clicks'),
     Input('btn-singles-year', 'n_clicks'),
     Input('year-dropdown', 'value'),
     Input('week-dropdown', 'value')]
)

def update_table(n_albums_week, n_albums_year, n_singles_week, n_singles_year, selected_year, selected_week):
    # Déterminer quel bouton a été sélectionné en dernier
    ctx = dash.callback_context
    if not ctx.triggered:
        selected_table = "Top Albums_Semaine"  # Affichage par défaut à l'arrivée sur la page
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        selected_table = {
            "btn-albums-week": "Top Albums_Semaine",
            "btn-albums-year": "Top Albums_Année",
            "btn-singles-week": "Top Singles_Semaine",
            "btn-singles-year": "Top Singles_Année"
        }.get(button_id, "Top Albums_Semaine")

    # Sélection du DataFrame correspondant au bouton sélectionné
    df_selected = dataframes[selected_table]

    # Vérifier si 'année' existe dans le DataFrame
    if 'année' in df_selected.columns:
        year_options = [{'label': str(year), 'value': year} for year in sorted(df_selected['année'].unique(), reverse=True)]

        # Si 'année' existe et n'est pas sélectionnée, afficher la valeur max par défaut
        if selected_year not in df_selected['année'].unique():
            selected_year = df_selected['année'].max()

        # Filtrer le DataFrame choisi sur l'année sélectionnée
        filtered_df = df_selected[df_selected['année'] == selected_year].reset_index(drop=True)
    else:
        year_options = []
        selected_year = None
        filtered_df = df_selected.copy()

    # Vérifier si 'semaine' existe dans le DataFrame
    if 'semaine' in df_selected.columns:
        week_options = [{'label': str(week), 'value': week} for week in sorted(filtered_df['semaine'].unique(), reverse=True)]

        if selected_week not in filtered_df['semaine'].unique():
            selected_week = filtered_df['semaine'].max()

        filtered_df = filtered_df[filtered_df['semaine'] == selected_week].reset_index(drop=True)
    else:
        week_options = []
        selected_week = None

    # Ajouter les rangs
    filtered_df['rang'] = filtered_df.index + 1

    # Conversion des polices en 'title' pour être plus propre
    filtered_df['artiste'] = filtered_df['artiste'].str.title()

    # Vérifier si la colonne 'album' ou 'titre' existe et appliquer le formatage approprié
    if 'album' in filtered_df.columns:
        filtered_df['album'] = filtered_df['album'].str.title()
    elif 'titre' in filtered_df.columns:
        filtered_df['titre'] = filtered_df['titre'].str.title()

    # Ajouter les couvertures depuis l'URL et diminuer la taille
    filtered_df['url_img'] = filtered_df['url_img'].apply(lambda x: f'<img src="{x}" width="120">')

    # Générer l'iframe Spotify si un ID est disponible
    def generate_spotify_iframe(spotify_id):
        if spotify_id != 'no id':
            return f'<iframe src="https://open.spotify.com/embed/album/{spotify_id}" width="100%" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'
        else:
            return " / "

    filtered_df['id_spotify'] = filtered_df['id_spotify'].apply(generate_spotify_iframe)

    return filtered_df.to_dict('records'), year_options, selected_year, week_options, selected_week
