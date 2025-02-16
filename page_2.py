
from dash import html
from navbar import create_navbar
import google.generativeai as genai  #IA
from dotenv import load_dotenv  # IA
import os  # IA

# CHARGER LES VARIABLES D'ENVIRONNEMENT DEPUIS .env pour récupérer le google_api_key
load_dotenv()

# CONFIGURATION DE LA CONNEXION
genai.configure(api_key= os.getenv("GOOGLE_API_KEY"))

nav = create_navbar()

header = html.H3('Welcome to page 2!')

artiste = "Moby"
titre = "go"

# partie génération d'un prompt
model = genai.GenerativeModel('gemini-1.5-flash')
prompt = f"Peux tu me donner un lien vers une vidéo du clip de moby et du titre go"
reponse = model.generate_content(prompt)

texte = html.P(reponse.text)


def create_page_2():
    layout = html.Div([
        html.Link(rel='stylesheet', href='/assets/styles.css'),
        nav,
        header,
        html.Div('Hello, Dash!', className='my-custom-class'),
        html.H1("Mon Lecteur youtube"),
        html.Iframe(
            src="https://www.youtube.com/embed/LXb3EKWsInQ",  # URL d'intégration YouTube
            #src=f"https://geo.dailymotion.com/player.html?video={reponse.text}",
            width="560",
            height="315",
            allow="fullscreen"
            )
    ])
    return layout