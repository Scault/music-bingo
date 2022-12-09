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


def get_song_list(username, playlist_url) -> list:
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


def generate_24_numbers():
    nums = []
    div, mod = divmod(NUM_SONGS, 5)

    for i in range(5):
        nums.extend(
            random.sample(
                range(i * div + min(i, mod), (i + 1) * div + min(i + 1, mod)),
                5 if i != 2 else 4,
            )
        )

    return nums


def split_list(list_: list, n: int) -> list:
    """ "Splits a list into n (roughly) equal lists

    Args:
        list_: desired list to split
        n: number of desired sublists
    Returns:
        list of n sublists
    """
    div, mod = divmod(len(list_), n)

    return [
        list_[i * div + min(i, mod) : (i + 1) * div + min(i + 1, mod)] for i in range(n)
    ]


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

    # Shuffle list in a repeatable manner (i.e. shuffle the same way every time)
    random.Random(1).shuffle(song_list)

    card_songs = []
    for num in nums:
        card_songs.append(song_list[num])

    if not path.exists("output/"):
        makedirs("output/")
    create_card(card_songs).save("output/results.jpg")
