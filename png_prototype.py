from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, List
from os import path, makedirs

BLANK_SQUARE_IMG = "imgs/blank_sq.jpg"
FREE_SPACE_IMG = "imgs/free_space.jpg"

Song = Tuple[str, str]

example_songs = [
    ("Song1", "Artist1"),
    ("Song2", "Artist2"),
    ("Song3", "Artist3"),
    ("Song4", "Artist4"),
    ("Song5", "Artist5"),
    ("Song6", "Artist6"),
    ("Song7", "Artist7"),
    ("Song8", "Artist8"),
    ("Song9", "Artist9"),
    ("Song10", "Artist10"),
    ("Song11", "Artist11"),
    ("Song12", "Artist12"),
    ("Song13", "Artist13"),
    ("Song14", "Artist14"),
    ("Song15", "Artist15"),
    ("Song16", "Artist16"),
    ("Song17", "Artist17"),
    ("Song18", "Artist18"),
    ("Song19", "Artist19"),
    ("Song20", "Artist20"),
    ("Song21", "Artist21"),
    ("Song22", "Artist22"),
    ("Song23", "Artist23"),
    ("Song24", "Artist24")
]


def create_square(title: str, artist: str) -> Image:
    """Create a bingo square

    Args:
        title: song title
        artist: song artist

    Returns:
        the resulting Image object
    """
    img = Image.open(BLANK_SQUARE_IMG)
    text = ImageDraw.Draw(img)

    # Font selection
    century_gothic = ImageFont.truetype('./fonts/CenturyGothic.ttf', 150)

    # Song name mustn't exceed 38 characters, else split to multiple lines
    # TODO: check for song and artist lengths
    text.multiline_text(
        xy=(500, 500),
        text=f"{title}\nby\n{artist}",
        fill="black",
        anchor="ms",
        align="center",
        font=century_gothic
    )

    return img


def create_free_space() -> Image:
    """Create the "Free Space" square

    Returns:
        the Free Space Image object
    """
    img = Image.open(BLANK_SQUARE_IMG)
    text = ImageDraw.Draw(img)

    # Font selection
    century_gothic = ImageFont.truetype('./fonts/CenturyGothicBold.ttf', 200)

    # Song name mustn't exceed 38 characters, else split to multiple lines
    # TODO: check for song and artist lengths
    text.multiline_text(
        xy=(500, 500),
        text="FREE\nSPACE",
        fill="black",
        anchor="ms",
        align="center",
        font=century_gothic
    )

    return img


def merge_images_horizontally(image1: Image, image2: Image) -> Image:
    """Merge two images into one, displayed side by side

    Args:
        file1: path to the first image file
        file2: path to the second image file

    Returns:
        the resulting Image object
    """
    (width1, height1) = image1.size
    (width2, height2) = image2.size

    result_width = width1 + width2
    result_height = max(height1, height2)

    result = Image.new('RGB', (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(width1, 0))

    return result


def merge_images_vertically(image1: Image, image2: Image) -> Image:
    """Merge two images into one, displayed one on top of the other

    Args:
        file1: path to the first image file
        file2: path to the second image file

    Returns:
        the resulting Image object
    """
    (width1, height1) = image1.size
    (width2, height2) = image2.size

    result_width = max(width1, width2)
    result_height = height1 + height2

    result = Image.new('RGB', (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(0, height1))

    return result


def create_column(songs: List[Song]) -> Image:
    """Create a bingo column

    Args:
        songs: a list of (song_title, song_artist) tuples, length of 5

    Returns:
        the resulting Image object
    """
    return merge_images_vertically(
        merge_images_vertically(
            merge_images_vertically(
                create_square(songs[0][0], songs[0][1]),
                create_square(songs[1][0], songs[1][1])
            ),
            merge_images_vertically(
                create_square(songs[2][0], songs[2][1]),
                create_square(songs[3][0], songs[3][1])
            )
        ),
        create_square(songs[4][0], songs[4][1])
    )


def create_middle_column(songs: List[Song]) -> Image:
    """Create a bingo column

    Args:
        songs: a list of (song_title, song_artist) tuples, length of 4

    Returns:
        the resulting Image object, with a "FREE SPACE" in the middle
    """
    return merge_images_vertically(
        merge_images_vertically(
            merge_images_vertically(
                create_square(songs[0][0], songs[0][1]),
                create_square(songs[1][0], songs[2][1])
            ),
            create_free_space(),
        ),
        merge_images_vertically(
            create_square(songs[2][0], songs[2][1]),
            create_square(songs[3][0], songs[3][1])
        )
    )


def create_card(songs: List[Song]) -> Image:
    """Create a bingo card

    Args:
        songs: a list of (song_title, song_artist) tuples, length of 24

    Returns:
        the resulting Image object
    """
    return merge_images_horizontally(
        merge_images_horizontally(
            merge_images_horizontally(
                create_column(songs[0:5]),
                create_column(songs[5:10])
            ),
            create_middle_column(songs[10:14])
        ),
        merge_images_horizontally(
            create_column(songs[14:19]),
            create_column(songs[19:])
        )
    )


if __name__ == "__main__":
    img = create_card(example_songs)
    if not path.exists("output/"):
        makedirs("output/")
    img.save("output/results.jpg")
    print(img.size)
