import requests
from bs4 import BeautifulSoup

base_url = "http://api.genius.com"
headers = {'Authorization' : 'Bearer uGSGWVuUcBn4CXsTeIgqVBPg7xoTTdVWUpO5w_PNSU5INwEyddPb3jyILAvixUfr', 'User-Agent' : 'curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)'}


def lyrics(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html5lib")
    lyrics = soup.find_all("" , {"class":"lyrics"})
    return lyrics[0].text.strip()

if __name__ == "__main__":
    artist_name = input("Artist: ")
    song_title = input("Title: ")
    search_url = base_url + "/search"
    data = {'q': song_title}
    response = requests.get(search_url, params=data, headers=headers)
    
    json = response.json()# json contains all information about song
    
    song_info = None
    for hit in json["response"]["hits"]:
        if artist_name.lower() in hit["result"]["primary_artist"]["name"].lower():
            song_info = hit
            break
    if song_info:
        song_url = song_info["result"]["url"]
    lyric = lyrics(song_url)
    print(lyric)