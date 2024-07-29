import json

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from const import client_id, client_secret, redirect_uri, playlist_id
import pandas as pd


def write_files():
    files = [
        open('file1.txt', 'w', encoding='utf-8'),
        open('file2.txt', 'w', encoding='utf-8'),
        open('file3.txt', 'w', encoding='utf-8'),
        open('file4.txt', 'w', encoding='utf-8'),
        open('file5.txt', 'w', encoding='utf-8')
    ]
    ranges = [
        (0, 0.45),
        (0.45, 0.5),
        (0.5, 0.55),
        (0.55, 0.7),
        (0.7, 1.0)
    ]
    for key, value in songs_energy.items():
        for i, (lower_bound, upper_bound) in enumerate(ranges):
            if lower_bound <= value < upper_bound:
                files[i].write(f"{key}\n")
                break
    for f in files:
        f.close()


sp = spotipy.Spotify(
    retries=20, auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                                          scope='user-library-read playlist-modify-private playlist-modify-public'))


def get_all_liked_songs():
    offset = 0
    limit = 50
    all_liked_songs = []
    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        if not results['items']:
            break

        all_liked_songs.extend(results['items'])
        offset += limit
        print(f"{offset} songs are in the list")
    return all_liked_songs


liked_songs = get_all_liked_songs()

def to_name_and_id(song):
    return song['track']['name'], song['track']['id']


songs_names_and_ids = dict(map(to_name_and_id, liked_songs))

songs_ids = list(songs_names_and_ids.values())
sublists = [songs_ids[i:i + 100] for i in range(0, len(songs_ids), 100)]

songs_energy: dict[str, int] = {}

energies = []
for sublist in sublists:
    results = sp.audio_features(tracks=sublist)
    for result in results:
        energies.append(result['energy'])

for song_name, energy in zip(songs_names_and_ids, energies):
    songs_energy[song_name] = energy

write_files()

# sorted_dict = dict(sorted(songs_energy.items(), key=lambda item: item[1]))

# for song in liked_songs:
#     song_name = song['track']['name']
#     song_id = song['track']['id']
#     songs_energy[song_name] = sp.audio_features(song_id)[0]['energy']
#     print(f"added {song_name}, {len(songs_energy)} are on the list")

# photograph = sp.search("photograph ed sheeran")['tracks']['items'][0]['id']
# drugs = sp.search("drugs falling in reverse")['tracks']['items'][0]['id']
# unwritten = sp.search("unwritten natasha")['tracks']['items'][0]['id']
# nights_and_curses = sp.search("לילות וקללות עומר אדם")['tracks']['items'][0]['id']
# # track_id_ = liked_songs['items'][18]['track']['id']
# photograph_analysis = sp.audio_features(photograph)[0]
# drugs_analysis = sp.audio_features(drugs)[0]
# unwritten_analysis = sp.audio_features(unwritten)[0]
# nights_and_curses_analysis = sp.audio_features(nights_and_curses)[0]
#
# df2 = pd.DataFrame(drugs_analysis, index=['drugs'])
# df3 = pd.DataFrame(unwritten_analysis, index=['unwritten'])
# df4 = pd.DataFrame(nights_and_curses_analysis, index=['nights'])
# df1 = pd.DataFrame(photograph_analysis, index=['photograph'])
#
# result = pd.concat([df1, df2, df3, df4])
#
# result.to_excel('comparison.xlsx')

# df1 = pd.DataFrame(songs_energy)
# df1.to_excel('comparison_energy.xlsx')
