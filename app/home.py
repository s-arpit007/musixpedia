import os
from tempfile import gettempdir
from flask import Flask, render_template, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from app import app
from app.utils import *
from flask_session import Session
from werkzeug.utils import redirect

if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-.cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-.cache"
        return response


# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
def index():
    print("******INDEX******")
    print(session)
    if session.get("spotify"):
        print("Redirecting to home...")
        return redirect(url_for('profile'))

    print("Opening Index page.")
    return render_template('index.html')


@app.route("/playlists", methods=["GET", "POST"])
@login_required
def playlists():
    print("******HOME*****")
    sp = session['spotify']
    results = sp.current_user_playlists(limit=50)

    return render_template('playlists.html', results=results)


@app.route('/login', methods=["GET", "POST"])
def login():
    """
    :TODO: close login window after successful login
    :return:
    """
    print("*****LOGIN*****")
    scope = get_scopes()
    auth_manager = SpotifyOAuth(scope=scope, cache_handler=CacheFileHandler())

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    session['spotify'] = spotify

    return redirect(url_for('profile'))


@app.route('/me', methods=['GET', 'POST'])
@login_required
def profile():
    details = session["spotify"].me()

    return render_template('profile.html', details=details)


@app.route('/logout', methods=["POST"])
def logout():
    print("******LOGOUT******")
    sp = session['spotify']
    if os.path.exists(sp.auth_manager.cache_handler.cache_path):
        os.remove(sp.auth_manager.cache_handler.cache_path)
        del session['spotify']
    else:
        print("Cache does not exists.")

    return redirect(url_for('index'))
