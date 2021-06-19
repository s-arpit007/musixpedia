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
    as json files on disk.
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
