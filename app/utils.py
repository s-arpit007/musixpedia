import errno
import json
import os
from spotipy import CacheHandler
from flask import redirect, request, session, url_for
from functools import wraps

basedir = os.path.dirname(os.path.realpath(__file__))


class CacheFileHandler(CacheHandler):
    """
    Handles reading and writing cached Spotify authorization tokens
    as json files on disk. In default state, cache files will be created on
    `musixpedia/app/.cache/..cache` path on your machine, so create the directory
    if there are errors.
    """

    def __init__(self,
                 cache_path=None,
                 username=None):
        """
        Parameters:
             * cache_path: May be supplied, will otherwise be generated
                           (takes precedence over `username`)
             * username: May be supplied or set as environment variable
                         (will set `cache_path` to `..cache-{username}`)
        """

        if cache_path:
            self.cache_path = cache_path
        else:
            cache_path = os.path.join(basedir, ".cache", "..cache")
            if username:
                cache_path += "-" + str(username)
            self.cache_path = cache_path

    def get_cached_token(self):
        token_info = None

        try:
            f = open(self.cache_path)
            token_info_string = f.read()
            f.close()
            token_info = json.loads(token_info_string)
            print("Found Cache File at:", self.cache_path)

        except IOError as error:
            if error.errno == errno.ENOENT:
                print(".cache does not exist at: %s", self.cache_path)
            else:
                print("Couldn't read .cache at: %s", self.cache_path)

        return token_info

    def save_token_to_cache(self, token_info):
        try:
            print("Writing Cache File at: ", self.cache_path)
            f = open(self.cache_path, "w")
            f.write(json.dumps(token_info))
            f.close()
        except IOError:
            print("Couldn't write token to .cache at: %s", self.cache_path)


def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("spotify"):
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def get_scopes(category='all'):
    """

    :param category: options (images/listening_history/spotify_connect/playback/playlists/follow/library/users)
                it supports multiple scopes as well by passing a list of scopes like below
                1. "all"
                2. ['images', 'follow', 'users']
                3. "images, follow, users"
    :return: list of scopes
    """
    scopes = {
        "images": ['ugc-image-upload'],
        "listening_history": ['user-read-recently-played', 'user-top-read', 'user-read-playback-position'],
        "spotify_connect": ['user-read-playback-state', 'user-modify-playback-state', 'user-read-currently-playing'],
        "playback": ['app-remote-control', 'streaming'],
        "playlists": ['playlist-modify-public', 'playlist-modify-private', 'playlist-read-private',
                      'playlist-read-collaborative'],
        "follow": ['user-follow-modify', 'user-follow-read'],
        "library": ['user-library-modify', 'user-library-read'],
        "users": ['user-read-email', 'user-read-private']}

    scopes_list = []
    if category == 'all':
        category = list(scopes.keys())

    elif isinstance(category, str):
        category = category.replace(' ', '').split(',')

    for key in category:
        if key in list(scopes.keys()):
            scopes_list += scopes[key]

    return scopes_list
