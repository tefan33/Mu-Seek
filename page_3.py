from dash import dcc, html
from navbar import create_navbar
import pandas as pd
from app import app
from dash.dependencies import Input, Output
import google.generativeai as genai  # IA
from dotenv import load_dotenv  # IA
import os  # IA
import requests  # pour requêter l'API YouTube

################################## CHARGEMENT VARIABLE ENVIRONNEMENT ##################################

load_dotenv()

################################## CONNEXION GOOGLE CHATBOT ##################################

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

################################## BARRE DE NAVIGATION ##################################

nav = create_navbar()

################################## LECTURE FICHIER ##################################

df = pd.read_csv('https://raw.githubusercontent.com/Yann-ML/PROJET_3_WCS/main/df_pres.zip')

# On crée la liste des artistes pour alimenter notre dropBox

list_artiste = sorted(df['artist_name'].unique().tolist())

########################## INTEGRATION API YOUTUBE ##########################

YOUTUBE_API_KEY = 'AIzaSyDBN7phKSHYQBcjJIrkOt4XJ3B-DUXgb3U'

# Fonction de récupération de la vidéo depuis YouTube

def get_video_id(artist, title):
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': f'{artist} {title} official music video',
        'key': YOUTUBE_API_KEY,
        'type': 'video',
        'maxResults': 1
    }
    response = requests.get(search_url, params=params)
    data = response.json()
    if 'items' in data and len(data['items']) > 0:
        return data['items'][0]['id']['videoId']
    else:
        return None

################################## APPLICATION ##################################

def create_page_3():
    layout = html.Div([
        nav,

        ######################### SECTION PRINCIPALE (2 COLONNES) #########################
        html.Div([

            ########## COLONNE GAUCHE : Dropdowns + Lecteurs ##########
            html.Div([
                html.Div(
                    children="Vous voulez écouter un morceau ?",
                    style={"font-weight": "bold",
                            'margin-bottom': '10px',
                            'margin-left': '50px',
                            'font-family': 'calibri',
                            'color': 'white'},
                ),

                # Dropdowns
                dcc.Dropdown(
                    list_artiste,
                    id="search_artist",
                    placeholder="Choisissez un artiste :",
                    className='dropdown_p3',
                    style={'width': '400px'}
                ),
                dcc.Dropdown(
                    id="search_album",
                    placeholder="Choisissez un album :",
                    className='dropdown_p3',
                    style={'width': '400px'}
                ),
                dcc.Dropdown(
                    id="search_track",
                    placeholder="Choisissez un morceau :",
                    className='dropdown_p3',
                    style={'width': '400px'}
                ),

                # Lecteur de musique Spotify
                html.Iframe(
                    src="",
                    id="play_track_spotify",
                    width="400px",
                    height="100",
                    allow="encrypted-media",
                    style={'border': 'none',
                           'margin-top': '20px',
                           'margin-left' : '45px'}
                ),

                html.H1(id="track_title", style={'color': 'white', 'margin-left': '45px'}),

                # Lecteur vidéo YouTube
                html.Iframe(
                    src="",
                    id="play_track_youtube",
                    width="560",
                    height="315",
                    allow="fullscreen",
                    style={'border': 'none',
                           'margin-top': '20px',
                           'margin-left' : '45px'}
                ),

                html.Div(id="zone_texte", style={'marginTop': 20}),

                # Stockage des variables
                html.Div([
                    dcc.Store(id="stored_album"),
                    dcc.Store(id="stored_track"),
                    dcc.Store(id="click_parole", data=2)
                ])
            ], style={'width': '100%', 'padding': '20px'}),

            ########## COLONNE DROITE : Bouton + Paroles ##########

            html.Div([
                html.Button(
                    "Activer la récupération des paroles",
                    id='button_parole',
                    className='dropdown_p3',
                    style={'width': '400px', 'margin-bottom': '20px'}
                ),

                html.Div([
                    html.H3(id='nom_titre', style={'color': 'white'}),
                    html.Div(id='texte_paroles', style={'color': 'white'}),
                ])
            ], style={'width': '100%', 'padding': '20px'}),

        ], style={
            'display': 'flex',
            'flex-direction': 'row',
            'justify-content': 'space-between',
            'align-items': 'flex-start',
            'width': '90%',
            'margin': 'auto',
            'margin-top': '20px'
        }),

    ], className="body")

    return layout

####################################### CALLBACKS #######################################

# Callback recherche album en fonction de l'artiste sélectionné dans la première dropdown

@app.callback(
    Output(component_id="search_album", component_property="options"),
    [Input(component_id="search_artist", component_property="value")]
)
def update_dropDown_album(value):
    if value:
        # On récupère les albums de l'artiste sélectionné
        list_album = df[df['artist_name'] == value]['album_name'].drop_duplicates().tolist()
        return [{'label': album, 'value': album} for album in list_album]
    return []

# Callback recherche titre en fonction de l'album choisi

@app.callback(
    [Output(component_id="search_track", component_property="options"),
     Output("stored_album", "data")],
    Input(component_id="search_album", component_property="value")
)
def update_dropDown_track(value):
    if value:
        list_track = df[df['album_name'] == value]['track_name'].drop_duplicates().tolist()
        return [{'label': track, 'value': track} for track in list_track], value
    return [], None

# Callback de gestion du bouton d'activation des paroles

@app.callback(
    [Output('button_parole', 'children'),
     Output('click_parole',"data")],
    [Input('button_parole', 'n_clicks')])
def clicks(n_clicks):
    # Si le nombre de clics est impair, on affiche un nom différent pour le texte
    if n_clicks % 2 == 1:
        return "Désactiver la récupération des paroles.", n_clicks
    # Si le nombre de clics est pair, ne rien afficher
    return "Activer la récupération des paroles", n_clicks

# Callback pour mettre à jour les lecteurs Spotify et YouTube

@app.callback(
    [Output(component_id="play_track_spotify", component_property="src"),
     Output(component_id="play_track_youtube", component_property="src"),
     Output("stored_track", "data"),
     Output("track_title", "children"),
     Output("texte_paroles","children")],
    [Input(component_id="search_track", component_property="value"),
     Input("stored_album", "data"),
     Input("click_parole", "data")]
)
def update_play_track(value, album, n_clicks):
    if value and album:
        artist = df[df['track_name'] == value]['artist_name'].values[0]
        track_id = df[(df['track_name'] == value) & (df['album_name'] == album)]['track_id'].values[0]
        spotify_embed_url = f'https://open.spotify.com/embed/track/{track_id}?utm_source=generator'

        video_id = get_video_id(artist, value)
        if video_id:
            video_embed_url = f'https://www.youtube.com/embed/{video_id}'
        else:
            video_embed_url = ""

        # On teste si on récupère les paroles ou pas :
        if n_clicks % 2 == 1:
            # Partie génération d'un prompt
            prompt = (f"Peux-tu m'afficher les paroles du titre {value} de l'album {album} tirées du site "
                      f"https://genius.com/ ? Je ne veux que les paroles et pas d'informations supplémentaires, "
                      f"pas de texte de ta part à part les paroles. Si tu ne trouves pas de résultats, indique "
                      f"juste la phrase : Je ne trouve pas de paroles pour ce titre !"
                      f"Je souhaite que tu les affiches de la même manière que sur le site (en mode verset), que tu peux webscrapper si tu le souhaites.")
            reponse = model.generate_content(prompt)
            return spotify_embed_url, video_embed_url, value, f"Vous écoutez: {artist} - {value}", reponse.text

        return spotify_embed_url, video_embed_url, '', f"Vous écoutez: {artist} - {value}", ''

    return "", "", None, "", ""

# Callback pour afficher le titre stocké

@app.callback(
    Output("nom_titre", "children"),
    Input("stored_track", "data")
)
def display_stored_track(stored_value):
    if stored_value:
        return f"Paroles de : {stored_value}"
    return ""
