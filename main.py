from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
Client_ID = os.environ.get("client_id")
Client_Secret = os.environ.get("client_secret")

data = response.text
soup = BeautifulSoup(data, "html.parser")

# print(soup.prettify())

songs = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
songs_names = [song.getText() for song in songs]
# print(songs_names)

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
# user_id = "4qg7jvzpwtgcpqlygxysyczul"

# searching song by its title
song_uris = []
year = date.split("-")[0]
for song in songs_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# for creating a new playlist in spotipy
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist['external_urls']['spotify'])

# for adding found song to playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
