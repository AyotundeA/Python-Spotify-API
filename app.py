#Python Spotify API #1 Tutorial by Jason Goodison

from flask import Flask, request, url_for, session, redirect
import spotipy 
from spotipy.oauth2 import SpotifyOAuth


app = Flask(_name_)


app.secret_key = "ONcs92894fhno"
app.config['SESSION_COOKIE_NAME'] = 'Jasons Cookie'
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return 'redirect'

@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        redirect("/")

    sp = spotipy.Spotify(auth=token_info['access_token'])
    all_songs = []
    iter = 0
    while True:
        items = sp.current_user_saved_tracks(limit=50, offset=0)['items']
        iter += 1
        all_songs += items
        if (len(items) < 50):
            break
    return str(len(all_songs))

    return str(sp.current_user_saved_tracks(limit=50, offset=0)['items'][0])

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now =  int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id="fde68bf48a3549e58b20c8bf3a58decc",
        client_secret="ae5b6492353394f789bd5d9297957fe40",
        redirect_url=url_for('redirect', _external=True),
        scope="user-library-read"

    )