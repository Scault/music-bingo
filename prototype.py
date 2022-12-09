import random
from spotipy import SpotifyClientCredentials, Spotify
import argparse
from card_generator import create_card
from os import path, makedirs, environ

auth_manager = SpotifyClientCredentials(
    environ["SPOTIFY_CLIENT_ID"], environ["SPOTIFY_CLIENT_SECRET"]
)
spotify = Spotify(auth_manager=auth_manager)
PLAYLIST_URL = (
    "https://open.spotify.com/playlist/1uWD5EA3peWrkdO4VNKoh0?si=2aa8a205ed9c4fdc"
)
playlist = spotify.playlist(PLAYLIST_URL)

NUM_SONGS = playlist["tracks"]["total"]


def get_song_list(username: str, playlist_url: str) -> list:
    """Retrieves a Spotify playlist

    Args:
        username: Spotify user ID
        playlist_url: the url of the desired playlist

    Returns:
        a list of tuples (title, artist) for the entire playlist
    """
    song_list = []
    results = spotify.user_playlist_tracks(username, playlist_url)
    tracks = results["items"]
    while results["next"]:
        results = spotify.next(results)
        tracks.extend(results["items"])

    for song in tracks:
        artists = ""
        for artist in song["track"]["artists"]:
            artists += artist["name"] + ", "
        artists = artists[:-2]

        song_list.append((song["track"]["name"], artists))
    return song_list


def generate_24_numbers() -> list:
    """Generates 24 unique numbers within the range of the playlist

    Returns:
        a list of numbers
    """
    return random.sample(range(1, NUM_SONGS), 24)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate seed and grid.")
    parser.add_argument("--load", dest="seed", action="store")

    args = parser.parse_args()
    if args.seed:
        random.seed(int(args.seed))
    else:
        seed = random.randint(1000000, 99999999)
        print(f"Seed: {seed}")
        random.seed(seed)

    nums = generate_24_numbers()
    print(nums)

    song_list = get_song_list("scotttheriault", PLAYLIST_URL)
    card_songs = []
    for num in nums:
        card_songs.append(song_list[num])

    if not path.exists("output/"):
        makedirs("output/")
    create_card(card_songs).save("output/results.jpg")
