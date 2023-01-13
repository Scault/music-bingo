import os
import sys
import glob
import random
import logging
import argparse
from os import path, makedirs, environ
from card_generator import create_card
from spotipy import SpotifyClientCredentials, Spotify, SpotifyException

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

auth_manager = SpotifyClientCredentials(
    environ["SPOTIFY_CLIENT_ID"], environ["SPOTIFY_CLIENT_SECRET"]
)
spotify = Spotify(auth_manager=auth_manager)
PLAYLIST_URL = (
    "https://open.spotify.com/playlist/5tl7iMYPGspVvMgryoA2HS?si=3812eee2d17a4cc5"
)
# playlist = spotify.playlist(PLAYLIST_URL)

# NUM_SONGS = playlist["tracks"]["total"]

PLAYLISTS = [
    "https://open.spotify.com/playlist/02Ze53FXXBgaSTfB9jpV1N?si=1a29aeb0e6b94621",  # 70s 1
    "https://open.spotify.com/playlist/2ZXxE8nsKuXplbOGVXRmk7?si=3508c19bb14343b0",  # 80s 1
    "https://open.spotify.com/playlist/4akSDZd9ppJx6LEhpWUXnJ?si=dce9d73d30714749",  # 90s 1
    "https://open.spotify.com/playlist/4WSK9EZdrSmVn94oh9fC0F?si=489fe486218b462c",  # 00s 1
    "https://open.spotify.com/playlist/340iasv2MTZsqAJBZHvScl?si=da6837376dd94468",  # 00s 2
    "https://open.spotify.com/playlist/6m9nAnMWZZ37nKqb8VxgT3?si=1ab09f9777c6417d",  # 10s 1
    "https://open.spotify.com/playlist/18i1CLpGUR1F0zl4IEWsOm?si=548426d4703d4b24",  # 10s 2
    "https://open.spotify.com/playlist/312n27j1xsU0Ee1NkyDdFw?si=0cca0803da4f44b2",  # 10s 3
]


def get_song_list(playlist_url: str) -> list:
    """Retrieves a Spotify playlist

    Args:
        playlist_url: the url of the desired playlist

    Returns:
        a list of tuples (title, artist) for the entire playlist
    """
    song_list = []
    results = spotify.playlist_tracks(playlist_url)
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


def generate_24_numbers(playlist: int = None) -> list:
    """Generates 24 unique numbers within the range of the playlist

    Returns:
        a list of numbers
    """
    url = PLAYLISTS[playlist] if playlist is not None else PLAYLIST_URL
    num_songs = spotify.playlist(url)["tracks"]["total"]

    nums = []
    div, mod = divmod(num_songs, 5)

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


def add_custom_playlist(url: str) -> bool:
    try:
        spotify.playlist(PLAYLIST_URL)
    except SpotifyException:
        return False

    PLAYLISTS.append(url)
    return True


def generate_card(seed: int = None, playlist: int = None) -> int:
    """Generates a bingo card

    Args:
        seed: seed to use for card generation

    Returns:
        the seed of the generated bingo card
    """
    if seed:
        random.seed(int(seed))
    else:
        seed = random.randint(1000000, 99999999)
        logging.info(f"Seed: {seed}")
        random.seed(seed)

    nums = generate_24_numbers(playlist)
    logging.info(f"{nums}")

    song_list = get_song_list(
        PLAYLISTS[playlist] if playlist is not None else PLAYLIST_URL
    )

    # Shuffle list in a repeatable manner (i.e. shuffle the same way every time)
    random.Random(1).shuffle(song_list)

    card_songs = []
    for num in nums:
        card_songs.append(song_list[num])

    if not path.exists("output/"):
        makedirs("output/")

    # Remove previous generated bingo cards
    files = glob.glob("output/*.jpg")
    for f in files:
        os.remove(f)

    create_card(card_songs).save(f"output/bingo_card-{seed}.jpg")
    return int(seed)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description="Generate seed and grid.")
    parser.add_argument("--load", dest="seed", action="store")

    args = parser.parse_args()

    seed = generate_card(args.seed)
