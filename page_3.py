from dash import dcc, html
from navbar import create_navbar
import pandas as pd
from app import app
from dash.dependencies import Input, Output
import google.generativeai as genai  #IA
from dotenv import load_dotenv  # IA
import os  # IA
# CHARGER LES VARIABLES D'ENVIRONNEMENT DEPUIS .env pour récupérer le google_api_key
load_dotenv()
# CONFIGURATION DE LA CONNEXION
genai.configure(api_key= os.getenv("GOOGLE_API_KEY"))
# on créé le model
model = genai.GenerativeModel('gemini-1.5-flash')
# on créé la barre de navigation
nav = create_navbar()
# on récupère le dataframe
df = pd.read_csv('https://raw.githubusercontent.com/Yann-ML/PROJET_3_WCS/main/df_spotify_1754.zip')
# on créé la liste des artistes pour alimenter notre dropBox
list_artiste = sorted(df['artist_name'].unique().tolist())
# mise en place du layout par la fonction
def create_page_3():
    layout = html.Div(
                    children =[
                        nav,
                        html.Div(
                            children=[
                                html.Div(
                                    children="Vous voulez écouter un morceau ?",
                                    style={"font-style": "italic", "font-weight": "bold", 'margin-bottom': '50px'},
                                ),
                                html.Button("Activer la récupération des paroles", id='button_parole',style={'margin-bottom': '50px'}),
                                html.Div([
                                        dcc.Dropdown(
                                            list_artiste,
                                            id="search_artist",
                                            placeholder="Choisissez un titre :",
                                        ),
                                    ],
                                    style={"width": "50%"},
                                ),
                                html.Div(
                                    style={'margin-bottom': '50px'},  # pour les écarts verticaux
                                ),
                                html.Div(
                                    style={'padding-top': '50px'},  # pour les écarts horizontaux
                                ),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="search_album",
                                            placeholder="Choisissez un album :",
                                        ),
                                    ],
                                    style={"width": "50%", 'margin-bottom': '100px'},
                                ),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="search_track",
                                            placeholder="Choisissez un morceau :", # cela permet d'avoir un texte de base affiché.
                                        ),
                                    ],
                                    style={"width": "50%", 'margin-bottom': '100px'},
                                ),
                                # Plus utilisé pour l'instant
                                # html.Div(
                                #     html.Div(
                                #         id="display_stored_value"  # Ici on affiche la variable stockée dans le store
                                #     ),
                                # ),
                                html.Iframe(  # partie lecteur de musique
                                    src="",
                                    id = "play_track",
                                    width="25%",
                                    height="25%",
                                    allow="encrypted-media",
                                    style={'border' : 'none'}
                                ),
                                html.Div(
                                    id="zone_texte",
                                    style={'marginTop': 20},
                                ),
                                # Stockage de mes DCC.Store
                                html.Div(
                                    [
                                        dcc.Store(id="stored_album"),  # ici on utilise un store de variable pour conserver des traces des choix et en particulier pour choisir le titre et ne pas se tromper d'album.
                                        dcc.Store(id="stored_track"),
                                        dcc.Store(id="click_parole", data=2) # on instancie la variable récupération des paroles à 2 car si elle est à 0 on ne peut pas utiliser le lecteur de musique
                                    ]
                                ),
                            ]
                        ),
                        # affichage des paroles du titre
                        html.Div(
                            children=[                      # élément qui seront mis à jour par les callback
                                html.H3(id='nom_titre'),
                                html.Div(
                                    id='texte_paroles'
                                ),
                            ], style={'color' : 'white'}
                        ),
                    ]
                )
    return layout
# call back de la recherche des artistes
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
# dans ce callBack on va récupérer la donnée de choix d'album pour la stocker dans le store en plus de faire la recherche des titres
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
# Partie de la gestion ds bouttons
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
# mises à jour de mon div display_stored_value avec ma variable stockée dans mon stored_album  Plus utilisé pour l'instant
# @app.callback(
#     Output("display_stored_value", "children"),
#     Input("stored_album", "data")
# )
# def display_stored_album(stored_value):
#     if stored_value:
#         return f"Stored Album Value: {stored_value}"
#     return ""
# mises à jour de mon div nom_titre avec ma variable stockée dans mon stored_track
@app.callback(
    Output("nom_titre", "children"),
    Input("stored_track", "data")
)
def display_stored_track(stored_value):
    if stored_value:
        return f"Paroles de : {stored_value}"
    return ""
# ici on recherche le titre choisi par l'utilisateur mais en s'assurant d'être sur le bon album.
# on récupère aussi la variable choisie par l'utilisateur pour stocker le nom du titre et l'utiliser plus tard.
@app.callback(
    [Output(component_id="play_track", component_property="src"),
     Output("stored_track", "data"),
     Output("texte_paroles","children")],
    [Input(component_id="search_track", component_property="value"),
     Input("stored_album", "data"),
     Input("click_parole", "data")]
)
def update_play_track(value, album, n_clicks):
    if value:
        # on test si on récupère les paroles ou pas :
        if n_clicks % 2 == 1:
            # partie génération d'un prompt
            prompt = f"Peux tu m'afficher les paroles du titre {value} de l'album {value} tirées du site https://genius.com/ , je ne veux que les paroles et pas d'informations supplémentaire, pas de texte de ta part à part les paroles. Si tu ne trouve pas de résultats indique juste la phrase : Je ne trouve pas de paroles pour ce titre !"
            reponse = model.generate_content(prompt)
            return f"https://open.spotify.com/embed/track/{df[(df['track_name'] == value) & (df['album_name'] == album)]['track_id'].drop_duplicates().values[0]}?utm_source=generator",value,reponse.text
        return f"https://open.spotify.com/embed/track/{df[(df['track_name'] == value) & (df['album_name'] == album)]['track_id'].drop_duplicates().values[0]}?utm_source=generator",'', ''
    return "", None, ""
