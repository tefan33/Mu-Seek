from navbar import create_navbar
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from app import app
import plotly.express as px
import pandas as pd
import dash
nav = create_navbar()
################################ FICHIERS DE SCRAPP SNEP ################################
# on récupère le dataframe
#link = 'https://raw.githubusercontent.com/Yann-ML/PROJET_3_WCS/main/API_SPOTIFY/df_spotify_1754.zip'
link = 'https://raw.githubusercontent.com/Yann-ML/PROJET_3_WCS/main/df_pres.zip'
df = pd.read_csv(link)
fig = px.bar(data_frame=df['label'].value_counts()[0:10])
# on créé la liste des artistes pour alimenter notre dropBox
list_artiste = sorted(df['artist_name'].unique().tolist())
image_path = '/assets/logo.png'


################################ CREATION PAGE ACCUEIL ################################
def create_page_5():
    layout = html.Div([
        nav,  # Navbar en haut
        # Contenu principal
        
        # Div contenant les boutons et les dropdowns
        html.Div([
            html.Button("Titres par album", id="btn-titre", n_clicks=0, className='button_style'),
            dcc.Dropdown(
                    id='artiste',
                    options=list_artiste,
                    value='Nirvana',
                    clearable=False,
                    style={'width' : '100%'}
                ),
            html.Hr(style={'border': '1px solid white', 'width': '100%'}),
            html.Button("Top 10 Labels", id="btn-labels", n_clicks=0, className='button_style'),
            html.Button("Top 20 followers", id="btn-followers", n_clicks=0, className='button_style'),
            html.Button("Top 20 Genres", id="btn-genres", n_clicks=0, className='button_style'),
            html.Hr(style={'border': '1px solid white', 'width': '100%'}),
            html.Button("Popularité:", id="btn-popu-album", n_clicks=0, className='button_style'),
            html.Button("Top 20 par Artiste", id="btn-popu-artiste", n_clicks=0, className='button_style'),
            html.Button("Top 20 par Album", id="btn-popu-album", n_clicks=0, className='button_style'),
            html.Div([
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
                  "top": "80px",  # Assure-toi que c'est la hauteur de la navbar
                  "left": "0",
                  "height": "calc(100vh - 100px)",
                  "width": "210px",
                  "overflow-y": "auto",
                  'margin-top' : '80px'}),
        #Div contenant le tableau de classement
        html.Div([
            html.Div([
                html.Div(children=[
                html.Label(
                                str(df['album_name'].drop_duplicates().count())+" artistes au total",
                                className='button_style',
                                id='pop_button')
                            ], style={'padding': 10, 'flex': 1}),
                html.Div(children=[
                        html.Label(
                                str(df['track_id'].count()) + " albums au total",
                                className='button_style',
                                id='pop_button')
                            ], style={'padding': 10, 'flex': 1}),
                # Affichage followers
                html.Div(children=[
                        html.Label(
                                str(df['track_id'].drop_duplicates().count()) + " titres au total",
                                className='button_style',
                                id='follow_button')
                            ], style={'padding': 10, 'flex': 1}),
            ],style={'display': 'flex', 'flex-direction': 'row'}),
            dcc.Graph(figure=fig, id='graph1', 
                      style={'margin-right' : '40px'}),
        ], style={'margin-top' : '10px', 'position': 'fixed', 'top': '100px', 'left': '250px', 'right': '10px', 'bottom': '10px', 'overflow-y': 'auto'}),
    ], className='body')
    return layout
################################ CALLBACK ################################
# callback de MAJ des bouton selon sélection
@app.callback(
    Output(component_id='graph1', component_property='figure'),
    [Input('btn-titre', 'n_clicks'),
     Input('btn-labels', 'n_clicks'),
     Input('btn-followers', 'n_clicks'),
     Input('btn-genres', 'n_clicks'),
     Input('btn-popu-artiste', 'n_clicks'),
     Input('btn-popu-album', 'n_clicks'),
     Input('artiste', 'value')]
)
def update_graph(clic1, clic2, clic3, clic4, clic5, clic6, value):
    # Déterminer quel bouton a été sélectionné en dernier
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = ""
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == "btn-titre":
        fig = px.bar(data_frame=df[['album_name', 'artist_name', 'total_tracks','track_name']][df['artist_name'] == value], x='album_name', hover_data='track_name',
            ).update_layout(xaxis_title="", yaxis_title="", title='Titres par album'
            ).update_traces( hovertemplate=df['track_name'])
    elif button_id == "btn-genres":
        # on trie pour ne récupérer qu'une ligne par album
        df_temp = df[['artist_name','album_name','genres_artist']].drop_duplicates()
        # on remplace les crochet et quote puisque la colonne est considérée comme string et non liste.
        liste_genre = df_temp['genres_artist'].apply(lambda x: x.replace('[', '').replace(']', '').replace("'", ""))
        # on ne garde que les colonnes non vides
        liste_genre_2 = liste_genre[liste_genre!='']
        # on sépare les éléments par les virgules pour avoir les genres séparés
        liste_finale = liste_genre_2.apply(lambda x : x.split(','))
        # on explose la nouvelle liste
        liste_finale = liste_finale.explode()
        # on retire les blancs à droite et à gauche
        liste_finale = liste_finale.apply(lambda x: x.lstrip())
        liste_finale = liste_finale.apply(lambda x: x.rstrip())
        fig = px.bar(data_frame=liste_finale.value_counts()[0:20]
            ).update_layout(xaxis_title="", yaxis_title="", title='Top 20 Genres',showlegend=False
            ).update_traces( hovertemplate=None)
    elif button_id == "btn-followers":
        df_follower = df[['artist_name','artist_followers','artist_id']]
        df_follower.drop_duplicates(inplace=True)
        fig = px.bar(data_frame=df_follower.sort_values(by='artist_followers', ascending=False)[0:20],
            x='artist_name',
            y='artist_followers',
            ).update_layout(xaxis_title="", yaxis_title="", title='Top 20 followers'
            )
    elif button_id == "btn-labels":
        fig = px.bar(data_frame=df['label'].value_counts()[0:10]
            ).update_layout(xaxis_title="", yaxis_title="", title='Top 10 Labels',showlegend=False
            ).update_traces( hovertemplate=None)
    elif button_id == "btn-popu-artiste":
        df_popularity = df[['artist_name','popularity_artist']]
        df_popularity.drop_duplicates(inplace=True)
        fig = px.bar(data_frame=df_popularity.sort_values(by='popularity_artist', ascending=False)[0:20],
             x='artist_name',
             y='popularity_artist',
             ).update_layout(xaxis_title="", yaxis_title="", title='Top 20 popularité / Artiste'
            )
    elif button_id == "btn-popu-album":
        df_popularity = df[['artist_name','album_name','popularity_album']]
        df_popularity.drop_duplicates(inplace=True)
        df_popularity.sort_values(by='popularity_album', ascending=False)[0:20]
        fig = px.bar(data_frame=df_popularity.sort_values(by='popularity_album', ascending=False)[0:20],
             x='artist_name',
             y='popularity_album',
             hover_data='album_name',
             ).update_layout(xaxis_title="", yaxis_title="", title='Top 20 popularité / Album'
            )
    else:
        fig = px.bar(data_frame=df[['album_name', 'artist_name', 'total_tracks','track_name']][df['artist_name'] == value], x='album_name', hover_data='track_name',
            ).update_layout(xaxis_title="", yaxis_title="", title='Titres par album'
            ).update_traces( hovertemplate=df['track_name'])
    return fig