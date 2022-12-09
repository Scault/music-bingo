import random
import argparse
from png_prototype import create_card

# TODO: Update this number automatically with the number of songs in the playlist
NUM_SONGS = 601

PLAYLIST = (
    "https://open.spotify.com/playlist/1uWD5EA3peWrkdO4VNKoh0?si=2aa8a205ed9c4fdc"
)


def generate_24_numbers():
    int_list = []
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
    # TODO: Convert these numbers to their respective (song name, artist) tuple

    songs = []
    for i, value in enumerate(nums):
        # TODO: Change song name and artist to actual values
        songs.append((str(value), "Artist" + str(i + 1)))

    create_card(songs).save("results.jpg")
