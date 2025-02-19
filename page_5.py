import dash
from dash import dcc, html
from navbar import create_navbar
import dash_bootstrap_components as dbc 
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from dash.dependencies import Input, Output
from app import app

# test
################################## LECTURE FICHIER ##################################

url = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/spotify.zip"

df_music = pd.read_csv(url)

# il y a des id_spotify en doublons, on les supprime
df_music = df_music.drop_duplicates(subset='track_id')

# liste des titres
search_titre = df_music['track_name'].to_list()

################################## NAVBAR ##################################

nav = create_navbar()

################################## DEFINITION DU ML ##################################

# colonnes à convertir en numérique/get_dummies

# mode à factorizer
df_music['mode_facto'] = pd.factorize(df_music['mode'])[0]

# genre et key à get_dummies
# pd.get_dummies(df_music[['genre', 'key']])

# création DF spécifique ML 
df_music_ml = pd.concat([df_music,
                        pd.get_dummies(df_music[['genre', 'key']], dtype=int)],
                         axis=1)

# déclaration variables (toutes colonnes numériques sauf popularity)
X = df_music_ml.select_dtypes(include=[float, int]).drop(columns='popularity')

# déclaration modèle NN
modelNN = NearestNeighbors(n_neighbors=6,
                           metric='cosine'          
                           )

# entrainement du modèle sur la colonne de features X
modelNN.fit(X)

################################## TITRE DE LA PAGE ##################################

header = html.H3('Bienvenue sur tes recommandations personnalisées !')

dropdown_style = {
    'font-family' : 'papyrus',
    'color': 'white'
}

################################## APPLICATION ##################################

def create_page_5():
    
    layout = html.Div([
        nav,
        header,
        html.H1("Mon système de recommandation"),
        
        ########################### CASE DE SELECTION TITRE ###########################

        dcc.Dropdown(
            id='input_search',
            options=[{'label': title, 'value': title} for title in search_titre],
            value='',
            placeholder='Rechercher un titre',
            style=dropdown_style,
            className='custom-dropdown'
        ),
        html.Div(id='recommendations')
    ])

    return layout

########################### CALLBACK DE RECHERCHE TITRE  ###########################

@app.callback(
    Output(component_id="recommendations", component_property="children"),
    [Input(component_id="input_search", component_property="value")]
)
def reco_search_titre(value):
    if value and value in df_music_ml['track_name'].values:
        # Récupérer l'index du titre
        index = df_music_ml[df_music_ml['track_name'] == value].index[0]

        if index in X.index:
            features_music = X.loc[index]

            # Modèle ML NN par rapport aux features de la musique recherchée
            distances, indices = modelNN.kneighbors([features_music], n_neighbors=30)

            # Créer le DF qui contiendra les musiques recommandées en fonction des indices du modèle NN
            music_reco = df_music_ml.iloc[indices[0]]

            # Affichage des recommandations
            recommendations = music_reco.iloc[1:4][['track_name', 'artist_name']]
            additional_recommendations = music_reco.iloc[4:].sample(5)[['track_name', 'artist_name']]

            return html.Div([
                html.H4(f"Musiques recommandées pour '{value}':"),
                # ul pour affichage en mode liste, et html.Li pour définir les éléments de la liste
                html.Ul([html.Li(f"{row['track_name']} by {row['artist_name']}") for _, row in recommendations.iterrows()]),
                html.H4("Vous pourriez aussi aimer:"),
                html.Ul([html.Li(f"{row['track_name']} by {row['artist_name']}") for _, row in additional_recommendations.iterrows()])
            ])
        else:
            return html.Div("L'index du titre n'existe pas dans les données.")
    else:
        return html.Div(f"Le titre '{value}' n'a pas été trouvée dans la base de données.")