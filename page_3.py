from dash import html
from navbar import create_navbar
import requests

YOUTUBE_API_KEY = 'AIzaSyDBN7phKSHYQBcjJIrkOt4XJ3B-DUXgb3U'

nav = create_navbar()

header = html.H3("Test d'utilisation de l'API de Youtube")




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


def create_page_3():
        
    artist = 'Madonna'
    title = 'La isla bonita'
    video_id = get_video_id(artist, title)

    if video_id:
        video_embed_url = f'https://www.youtube.com/embed/{video_id}'
        video_direct_url = f'https://www.youtube.com/watch?v={video_id}'
        layout = html.Div([
            nav,
            header,
            html.H3(f'Vous écoutez: {artist} - {title} '),
            html.H1("Mon Lecteur YouTube"),
            html.Iframe(
                src=video_embed_url,
                width="560",
                height="315",
                allow="fullscreen"
            ),
            html.P([
            "Si la vidéo ne s'affiche pas, vous pouvez la regarder directement sur ",
            html.A("YouTube", href=video_direct_url, target="_blank")
            ])
        ])
    else:
        layout = html.Div([
            html.H3(f'No video found for {artist} - {title}'),
        ])

    return layout