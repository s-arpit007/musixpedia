import os
from spotipy.oauth2 import SpotifyOAuth
import utils as utils
from spotipy.client import Spotify

# print(os.path.abspath(__file__))
# print(os.path.dirname(os.path.realpath(__file__)))

scope = 'playlist-read-private'
auth_manager = SpotifyOAuth(scope=scope, cache_handler=utils.CacheFileHandler())
print("Client_ID:", auth_manager.client_id)
# print("Client_SECRET:", auth_manager.client_secret)
print("Cache handler:", auth_manager.cache_handler)
# print(auth_manager.state)
print("Open Browser:", auth_manager.open_browser)
# print(auth_manager.get_access_token(as_dict=False))

print("Creating Spotify object")
sp = Spotify(auth_manager=auth_manager)
print("Done with Spotify")
print(sp.auth_manager.get_access_token(as_dict=False))

results = sp.current_user_playlists(limit=50)

for i, result in enumerate(results["items"]):
    print(i+1, result["name"])

id = input("Playlist ID:")
results = sp.playlist(playlist_id=id)
    
for i, result in enumerate(results["tracks"]["items"]):
    print(i+1, result["track"]["name"], result['track']['album']['name'])
    
if os.path.exists(sp.auth_manager.cache_handler.cache_path):
    os.remove(sp.auth_manager.cache_handler.cache_path)
else:
    print("Cache does not exists.")
