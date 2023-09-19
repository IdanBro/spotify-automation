import spotipy
from spotipy.oauth2 import SpotifyOAuth

from const import client_id, client_secret, redirect_uri, playlist_id

predefined_artists = ['Omer Adam', 'Adir Getz', 'Amir Benayoun', 'Aya Korem', 'Berry Sakharof', 'Boaz Banai',
                      'Boaz Sharabi', 'Doli & Penn', 'Eden Hason', 'Liran Danino', 'Dor Daniel', 'Dudi Bar David',
                      'Dudu Aharon', 'Dudu Tassa', 'Eden Ben Zaken', 'Eliran Aslan', 'Elisha Banai', 'Eyal Golan',
                      'Gal Adam', 'Gilad Segev', 'Peer Tasi', 'Harel Moyal', 'Idan Yaniv', 'Ishay Levi', 'Ishay Ribo',
                      'Itay Levi', 'Izhar Ashdot', 'Kobi Aflalo', 'Maor Edri', 'Moshe Peretz', 'Moshik Afia', 'Narkis',
                      'Ninet Tayeb', 'Niv Demiral', 'Odeya', 'Roei Adam', 'Osher Cohen', 'Ron Shoval', 'Rotem Gabay',
                      'Sarit Hadad', 'Shay Amar', 'Shir Levi', 'Shlomi Shabat', 'Tamar Yahalomy', 'Yonatan Kalimi',
                      'Shaked Komemy', 'Yossi Shitrit', 'Zehava Ben', 'יהודה סעדו', 'כפיר פופוביץ', 'Shilo',
                      'אליאב זוהר']

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                              scope='user-library-read playlist-modify-private playlist-modify-public'))


def get_all_liked_songs():
    offset = 0
    limit = 50
    all_liked_songs = []
    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        if not results['items']:
            break  # No more items to fetch

        all_liked_songs.extend(results['items'])
        offset += limit
        print(f"{offset} songs are in the list")
    return all_liked_songs


def save_mizrahit_songs(all_liked_songs):
    for item in all_liked_songs:
        track = item['track']
        artists = [artist['name'] for artist in track['artists']]
        song_name = track['name']

        if any(artist in predefined_artists for artist in artists):
            print(f"Adding '{song_name}' to the playlist.")
            sp.playlist_add_items(playlist_id, [track['id']])
    print("Done!")


def write_songs_names_to_file(all_liked_songs):
    output_file = "liked_songs.txt"
    song_names = []

    for item in all_liked_songs:
        track = item['track']
        song_name = track['name']
        song_names.append(song_name)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(song_names))

    print(f"Successfully wrote {len(song_names)} liked song names to {output_file}.")


all_liked_songs = get_all_liked_songs()
write_songs_names_to_file(all_liked_songs)
# save_mizrahit_songs(all_liked_songs)
