import requests
from bs4 import BeautifulSoup

base_url = "https://genius.com/"
artist = input("Artist: ")
song_title = input("Title: ")

url = base_url + artist.replace(" ", "-") + "-" + song_title.replace(" ", "-") + "-" + "lyrics"

html = requests.get(url)
soup = BeautifulSoup(html.text, "html5lib")
lyrics = soup.find_all("" , {"class":"lyrics"})

print(lyrics[0].text.strip())