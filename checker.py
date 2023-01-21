import random
import tkinter as tk
from collections import namedtuple
from tkinter import messagebox, ttk
from tkinter.simpledialog import askstring
from prototype import (
    spotify,
    SpotifyException,
    get_song_list,
    PLAYLISTS,
    add_custom_playlist,
    generate_24_numbers,
    split_list,
)

Song = namedtuple("Song", ["song", "letter"])

RUDE_MESSAGES = [
    "You are swine you vulgar little maggot.",
    "Don't you know that you are pathetic?",
    "You worthless bag of filth.",
    "I bet you couldn't pour piss out of a boot with instructions on the heel.",
    "You are a canker. A sore that won't go away. A zit on the butt of society.",
    "I would rather kiss a lawyer than be seen with you.",
    "You are a fiend and a coward, and you have bad breath.",
    "You are degenerate, noxious and depraved.",
    "I feel debased just for knowing you exist.",
    "I despise everything about you.",
    "I wish you would just go away.",
    "You're a putrescence mass, a walking vomit.",
    "You are a spineless little worm deserving nothing but the profoundest contempt.",
    " You are a jerk, a cad, a weasel.",
    "Your life is a monument to stupidity.",
    "You are a stench, a revulsion, a big suck on a sour lemon.",
    "I will never get over the embarrassment of belonging to the same species as you.",
    "You are a monster, an ogre, a malformity.",
    "I barf at the very thought of you.",
    "You have all the appeal of a paper cut.",
    "Lepers avoid you.",
    "Because of your face, the rabbit population actually decreased.",
    "You are vile, worthless, and less than nothing.",
    "You are a weed, a fungus, the dregs of this earth. And did I mention you smell?",
    "If you aren't an idiot, you made a world-class effort at simulating one.",
    "May you choke on the queasy, convulsing nausea of your own trite, foolish beliefs.",
    "You are weary, stale, flat and unprofitable.",
    "You are grimy, squalid, nasty and profane.",
    "You are foul and disgusting.",
    "You're a fool, an ignoramus.",
    "Monkeys look down on you.",
    "Even sheep won't have sex with you.",
    "You are unreservedly pathetic, starved for attention, and lost in a land that reality forgot.",
    "You are a waste of flesh.",
    "You have no rhythm.",
    "You are ridiculous and obnoxious.",
    "You are the moral equivalent of a leech.",
    "You are a living emptiness, a meaningless void.",
    "You are sour and senile.",
    "You are a disease, you puerile one-handed slack-jawed drooling meat-slapper.",
    "On a good day you're a half-wit.",
    "You remind me of drool.",
    "You are deficient in all that lends character.",
    "You have the personality of wallpaper.",
    "You are dank and filthy.",
    "You are asinine and benighted.",
    "You are the source of all unpleasantness.",
    "You spread misery and sorrow wherever you go.",
    "I cannot believe how incredibly stupid you are. I mean rock-hard stupid. Dehydrated-rock-hard stupid. Stupid so stupid that it goes way beyond the stupid we know into a whole different dimension of stupid. You are trans-stupid stupid. Meta-stupid. Stupid collapsed on itself so far that even the neutrons have collapsed. Stupid gotten so dense that no intellect can escape. Singularity stupid. Blazing hot mid-day sun on Mercury stupid. You emit more stupid in one second than our entire galaxy emits in a year. Quasar stupid. Your writing has to be a troll. Nothing in our universe can really be this stupid. Perhaps this is some primordial fragment from the original big bang of stupid. Some pure essence of a stupid so uncontaminated by anything else as to be beyond the laws of physics that we know. I'm sorry. I can't go on. This is an epiphany of stupid for me. After this, you may not hear from me again for a while.",
    "Maybe later in life, after you have learned to read, write, spell, and count, you will have more success.",
    "I wish you the best of luck in the emotional, and social struggles that seem to be placing such a demand on you.",
]

COMPLETE_LINES = [
    # Horizontal Lines
    [1, 6, 11, 15, 20],
    [2, 7, 12, 16, 21],
    [3, 8, 17, 22],
    [4, 9, 13, 18, 23],
    [5, 10, 14, 19, 24],
    # Vertical Lines
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14],
    [15, 16, 17, 18, 19],
    [20, 21, 22, 23, 24],
    # Diagonal
    [1, 7, 18, 24],
    [5, 9, 16, 20],
]


class BingoChecker(tk.Tk):
    """The Bingo Checker application window."""

    def __init__(self) -> None:
        """Initializes the Bingo Checker application window."""
        tk.Tk.__init__(self)
        self.title("Bingo Controller")
        self.geometry("1200x707")
        self.resizable(True, True)
        icon = tk.PhotoImage(file="imgs/icon.png")
        self.wm_iconphoto(False, icon)
        self.playlist_count = 8
        self.song_list = []
        self.init_gui()
        self.init_menu()
        self.load_playlist()

    def init_gui(self) -> None:
        """Initializes the GUI for the application."""
        # Create top-level frames
        top_frame = tk.Frame(self, padx=10, pady=10)
        middle_frame = tk.Frame(self, padx=10)
        bottom_frame = tk.Frame(self, padx=10, pady=10)

        # Setup playlist viewer
        self.init_viewer(top_frame)
        self.viewer_frame.grid(row=0, column=0, sticky="nsew")

        # Setup selector
        self.init_bingo_selector(middle_frame)
        self.selector_frame.grid(row=0, column=0)

        # Setup card checker
        self.init_card_checker(bottom_frame)
        self.checker_frame.grid(row=0, column=0, sticky="nsew")

        # Align top level frames
        top_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        middle_frame.grid(row=0, column=1, sticky="nsew")
        bottom_frame.grid(row=1, column=1, sticky="nsew")

        # Configure content filling
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        top_frame.columnconfigure(0, weight=1)
        top_frame.rowconfigure(0, weight=1)
        middle_frame.columnconfigure(0, weight=1)
        middle_frame.rowconfigure(0, weight=1)
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.rowconfigure(0, weight=1)

        # Binds
        self.list.bind("<<ListboxSelect>>", self.fill_search)
        self.search.bind("<KeyRelease>", self.check_entry)

    def init_menu(self) -> None:
        """Initializes the menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Initialize menus
        file_menu = tk.Menu(menubar, tearoff=0)
        settings_menu = tk.Menu(menubar, tearoff=0)
        self.playlist_menu = tk.Menu(menubar, tearoff=0)

        # Create main menus
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        # Add command(s) to File menu
        file_menu.add_command(
            label="Select Custom Playlist",
            command=lambda: self.custom_playlist(),
        )

        # Add command(s) to Settings menu
        settings_menu.add_cascade(label="Change Playlist", menu=self.playlist_menu)

        # Add playlists to Playlist menu
        self.playlist = tk.IntVar()
        self.playlist.set(0)
        self.playlist_menu.add_radiobutton(
            label="70s",
            variable=self.playlist,
            value=0,
            command=lambda: self.load_playlist(),
        )
        self.playlist_menu.add_radiobutton(
            label="80s",
            variable=self.playlist,
            value=1,
            command=lambda: self.load_playlist(),
        )
        self.playlist_menu.add_radiobutton(
            label="90s",
            variable=self.playlist,
            value=2,
            command=lambda: self.load_playlist(),
        )
        self.playlist_menu.add_radiobutton(
            label="2000s 1",
            variable=self.playlist,
            value=3,
            command=lambda: self.load_playlist(),
        )
        self.playlist_menu.add_radiobutton(
            label="2000s 2",
            variable=self.playlist,
            value=4,
            command=lambda: self.load_playlist(),
        )
        self.playlist_menu.add_radiobutton(
            label="2010s 1",
            variable=self.playlist,
            value=5,
            command=lambda: self.load_playlist(),
        )
        self.playlist_menu.add_radiobutton(
            label="2010s 2",
            variable=self.playlist,
            value=6,
            command=lambda: self.load_playlist(),
        )
        self.playlist_menu.add_radiobutton(
            label="2010s 3",
            variable=self.playlist,
            value=7,
            command=lambda: self.load_playlist(),
        )

    def init_viewer(self, frame: tk.Frame) -> None:
        """Sets up and configures the playlist viewers."""
        # Create topmost frame contents
        self.viewer_frame = tk.Frame(frame)

        self.search = tk.Entry(self.viewer_frame)
        playlist_label = tk.Label(self.viewer_frame, text="Available Songs")
        self.list = tk.Listbox(self.viewer_frame, exportselection=False)
        add_button = tk.Button(self.viewer_frame, text=">>", command=self.add_song)
        remove_button = tk.Button(
            self.viewer_frame, text="<<", command=self.remove_song
        )
        played_label = tk.Label(self.viewer_frame, text="Played Songs")
        self.played = tk.Listbox(self.viewer_frame, exportselection=False)

        # Setup "Available Songs" Listbox scrollbars
        h_scrollbar_1 = tk.Scrollbar(self.viewer_frame, orient="horizontal")
        h_scrollbar_1.config(command=self.list.xview)
        v_scrollbar_1 = tk.Scrollbar(self.viewer_frame, orient="vertical")
        v_scrollbar_1.config(command=self.list.yview)
        self.list.config(
            yscrollcommand=v_scrollbar_1.set, xscrollcommand=h_scrollbar_1.set
        )

        # Setup "Played Songs" Listbox scrollbars
        h_scrollbar_2 = tk.Scrollbar(self.viewer_frame, orient="horizontal")
        h_scrollbar_2.config(command=self.played.xview)
        v_scrollbar_2 = tk.Scrollbar(self.viewer_frame, orient="vertical")
        v_scrollbar_2.config(command=self.played.yview)
        self.played.config(
            yscrollcommand=v_scrollbar_2.set, xscrollcommand=h_scrollbar_2.set
        )

        # Align topmost frame contents
        self.search.grid(row=0, column=0, sticky="ew")
        playlist_label.grid(row=1, column=0, sticky="ew")
        played_label.grid(row=1, column=3, sticky="ew")
        self.list.grid(row=2, column=0, rowspan=4, sticky="nsew")
        self.played.grid(row=2, column=3, rowspan=4, sticky="nsew")
        add_button.grid(row=3, column=2, padx=5, pady=2.5, sticky="nsew")
        remove_button.grid(row=4, column=2, padx=5, pady=2.5, sticky="nsew")
        h_scrollbar_1.grid(row=6, column=0, sticky="nsew")
        v_scrollbar_1.grid(row=2, column=1, rowspan=4, sticky="nsew")
        h_scrollbar_2.grid(row=6, column=3, sticky="nsew")
        v_scrollbar_2.grid(row=2, column=4, rowspan=4, sticky="nsew")

        # Configure content filling
        self.viewer_frame.columnconfigure(0, weight=1)
        self.viewer_frame.columnconfigure(1, weight=0)
        self.viewer_frame.columnconfigure(2, weight=0)
        self.viewer_frame.columnconfigure(3, weight=1)
        self.viewer_frame.columnconfigure(4, weight=0)
        self.viewer_frame.rowconfigure(0, weight=0)
        self.viewer_frame.rowconfigure(1, weight=0)
        self.viewer_frame.rowconfigure(2, weight=1)
        self.viewer_frame.rowconfigure(3, weight=0)
        self.viewer_frame.rowconfigure(4, weight=0)
        self.viewer_frame.rowconfigure(5, weight=1)
        self.viewer_frame.rowconfigure(6, weight=0)

    def init_bingo_selector(self, frame: tk.Frame) -> None:
        """Sets up and configures the randomized song selector."""
        # Create frames
        self.selector_frame = tk.Frame(frame)

        top_frame = tk.Frame(self.selector_frame)
        separator = ttk.Separator(self.selector_frame, orient="horizontal")
        bottom_frame = tk.Frame(self.selector_frame)

        # Create topmost frame contents
        b_button = tk.Button(
            top_frame,
            text="B",
            height=5,
            width=10,
            bg="#3db2e3",
            command=lambda: self.random_song(0),
        )
        i_button = tk.Button(
            top_frame,
            text="I",
            height=5,
            width=10,
            bg="#ae3de3",
            command=lambda: self.random_song(1),
        )
        n_button = tk.Button(
            top_frame,
            text="N",
            height=5,
            width=10,
            bg="#3de36f",
            command=lambda: self.random_song(2),
        )
        g_button = tk.Button(
            top_frame,
            text="G",
            height=5,
            width=10,
            bg="#e3b43d",
            command=lambda: self.random_song(3),
        )
        o_button = tk.Button(
            top_frame,
            text="O",
            height=5,
            width=10,
            bg="#e33d53",
            command=lambda: self.random_song(4),
        )

        # Create bottommost frame contents
        song_label = tk.Label(bottom_frame, text="Song:")
        self.chosen_song = tk.Label(bottom_frame, text="")

        # Align toplevel frames
        top_frame.grid(row=0, column=0, sticky="n", padx=10, pady=10)
        separator.grid(row=1, column=0, sticky="nsew", padx=10)
        bottom_frame.grid(row=2, column=0, sticky="n", padx=10, pady=10)

        # Align top grid
        b_button.grid(row=0, column=0, sticky="nw", padx=0)
        i_button.grid(row=0, column=1, padx=5)
        n_button.grid(row=0, column=2, padx=0)
        g_button.grid(row=0, column=3, padx=5)
        o_button.grid(row=0, column=4, padx=0)

        # Align bottom grid
        song_label.grid(row=0, column=0, sticky="new")
        self.chosen_song.grid(row=1, column=0, sticky="new")

        # Configure content filling
        top_frame.rowconfigure(0, weight=0)
        top_frame.columnconfigure(0, weight=0)
        top_frame.columnconfigure(1, weight=0)
        top_frame.columnconfigure(2, weight=0)
        top_frame.columnconfigure(3, weight=0)
        top_frame.columnconfigure(4, weight=0)
        bottom_frame.rowconfigure(0, weight=0)
        bottom_frame.rowconfigure(1, weight=0)
        bottom_frame.columnconfigure(0, weight=0)

    def init_card_checker(self, frame: tk.Frame) -> None:
        """Sets up and configures the card checker."""
        # Create elements
        self.checker_frame = tk.Frame(frame)

        seed_label = tk.Label(self.checker_frame, text="Seed")
        self.seed = tk.Entry(self.checker_frame)
        check_button = tk.Button(
            self.checker_frame, text="Check", command=self.check_seed
        )

        # Align bottommost frame contents
        seed_label.grid(row=0, column=0, sticky="s")
        self.seed.grid(row=1, column=0, pady=5)
        check_button.grid(row=2, column=0, sticky="n")

        # Configure content filling
        self.checker_frame.columnconfigure(0, weight=1)
        self.checker_frame.rowconfigure(0, weight=1)
        self.checker_frame.rowconfigure(1, weight=0)
        self.checker_frame.rowconfigure(2, weight=1)

    def add_song(self) -> None:
        """Adds a song to the 'Played' ListBox."""
        # Do nothing if nothing is selected
        if self.list.curselection() == ():
            return

        # Remove the selected song from the available songs and add to the played songs
        for i in self.list.curselection():
            song = self.list.get(i)
            self.played.insert(tk.END, song)
            self.list.delete(i)

        # Update the current list of available songs
        self.current_list.remove(song)

        # Check which letter the song is under and remove from that letter
        # TODO: Update this with the new Python 3.10 "match" switch statement
        for element in self.letter_record:
            if element.song == song:
                if element.letter == "B":
                    self.b.remove(song)
                elif element.letter == "I":
                    self.i.remove(song)
                elif element.letter == "N":
                    self.n.remove(song)
                elif element.letter == "G":
                    self.g.remove(song)
                elif element.letter == "O":
                    self.o.remove(song)

    def remove_song(self) -> None:
        """Removes a song from the 'Played' ListBox."""
        # Do nothing if nothing is selected
        if self.played.curselection() == ():
            return

        # Remove the selected song from the played songs and add to the available songs
        for i in self.played.curselection():
            song = self.played.get(i)
            self.list.insert(tk.END, song)
            self.played.delete(i)

        # Update the current list of available songs
        self.current_list.append(song)

        # Check which letter the song is under and re-add to that letter
        # TODO: Update this with the new Python 3.10 "match" switch statement
        for element in self.letter_record:
            if element.song == song:
                if element.letter == "B":
                    self.b.append(song)
                elif element.letter == "I":
                    self.i.append(song)
                elif element.letter == "N":
                    self.n.append(song)
                elif element.letter == "G":
                    self.g.append(song)
                elif element.letter == "O":
                    self.o.append(song)

    def update(self, data: list) -> None:
        """Updates the 'Available Songs' ListBox.

        Args:
            data: a list where each item is an entry in the ListBox
        """
        # Clear the "Available Songs" Listbox
        self.list.delete(0, tk.END)

        # Add contents
        for item in data:
            self.list.insert(tk.END, item)

    def fill_search(self, event: tk.Event) -> None:
        """Fills the search bar with the selection in the 'Available Songs' ListBox.

        Args:
            event: an event passed by Listbox.bind()
        """
        # Clear search bar
        self.search.delete(0, tk.END)

        # Add selected entry to the search bar
        self.search.insert(0, self.list.get(tk.ACTIVE))

    def check_entry(self, event: tk.Event) -> None:
        """Updates the 'Available Songs' ListBox with the typed string in the search box.

        Args:
            event: an event passed by Entry.bind()
        """
        # Get the typed string in the search bar
        typed = self.search.get()

        # Show all current available songs if nothing is typed, else show matches
        if typed == "":
            data = self.current_list
        else:
            data = []
            for item in self.current_list:
                if typed.lower() in item.lower():
                    data.append(item)

        # Update the "Available Songs" Listbox
        self.update(data)

    def check_seed(self) -> None:
        """Checks a given seed to see if it is a winning bingo card."""
        # Do nothing is no seed has been entered
        if self.seed.get() == "":
            return

        # TODO: Add type checking (i.e. only accept integers)

        # Save the current random state
        old_state = random.getstate()

        # Get the indexes of the songs using the provided seed
        random.seed(int(self.seed.get()))
        nums = generate_24_numbers(self.playlist.get())

        # Restore the old random state
        random.setstate(old_state)

        # Convert the list indexes to the respective songs
        lines = []
        for i in COMPLETE_LINES:
            line = []
            for num in i:
                x = nums[num - 1]
                line.append(self.song_list[x])
            lines.append(line)

        # Get the list of all songs that have been played
        played = self.played.get(0, tk.END)

        # Count the number of lines
        count = 0
        for line in lines:
            if set(played).issuperset(set(line)):
                count += 1

        # Display results to the user
        # TODO: Add functionality to allow the number of desired lines to be configurable
        if count >= 2:
            messagebox.showinfo("Congratulations!", "This card is a winner!")
        else:
            messagebox.showerror("WRONG", random.choice(RUDE_MESSAGES))

    def load_playlist(self, seed: int = None) -> None:
        """Loads a playlist to display in the 'Available Songs' Listbox.

        Args:
            seed: seed to use for card generation
        """
        # Get the list of songs
        self.song_list = get_song_list(PLAYLISTS[self.playlist.get()])

        # Clear both Listboxes
        self.list.delete(0, tk.END)
        self.played.delete(0, tk.END)

        # Trim data and add to the "Available Songs" Listbox
        # TODO: Move the name trimming inside get_song_list()
        temp_list = []
        for i, song in enumerate(self.song_list):
            title = song[0].rsplit(" - ")[0]
            temp_list.append(f"{title} - {song[1]}")
            self.list.insert(i, f"{title} - {song[1]}")
        self.song_list = temp_list

        # Shuffle the songs in a repeatable manner
        # TODO: Move the repeatable shuffle into get_song_list()
        random.Random(1).shuffle(self.song_list)
        self.current_list = list(self.list.get(0, tk.END))

        # Evenly divide the list into 5 segments and assign to a letter
        split = split_list(self.song_list, 5)
        self.b = split[0]
        self.i = split[1]
        self.n = split[2]
        self.g = split[3]
        self.o = split[4]

        # Keep a record of which letter each song is under
        # TODO: Attach the letter information to each entry so that this container can be removed
        self.letter_record = []
        for song in self.song_list:
            if song in self.b:
                self.letter_record.append(Song(song, "B"))
            elif song in self.i:
                self.letter_record.append(Song(song, "I"))
            elif song in self.n:
                self.letter_record.append(Song(song, "N"))
            elif song in self.g:
                self.letter_record.append(Song(song, "G"))
            elif song in self.o:
                self.letter_record.append(Song(song, "O"))

    def custom_playlist(self):
        """Opens the Playlist popup window."""
        # Prompt the user to enter a Spotify playlist URL
        url = askstring("Add Custom Playlist", "Enter Spotify playlist URL:\t\t\t\t")

        # Do nothing if nothing is typed
        if url is None:
            return

        # Verify the playlist is longer than 24 songs
        try:
            num_songs = spotify.playlist(url)["tracks"]["total"]
            if num_songs < 25:
                messagebox.showerror("Error", "Playlist must be longer than 24 songs.")
                return
        except SpotifyException:
            return

        # Add the custom playlist as an option to the menubar
        # TODO: Make the label of the menu item the name of the custom playlist
        if add_custom_playlist(url):
            self.playlist_menu.add_radiobutton(
                label="Custom Playlist",
                variable=self.playlist,
                value=self.playlist_count,
                command=lambda: self.load_playlist(),
            )

        # Set the active playlist and increment the number of playlists
        self.playlist.set(self.playlist_count)
        self.playlist_count += 1

        # Load the new playlist
        self.load_playlist()

    def random_song(self, letter: int) -> None:
        """Selects a random song from a given column (letter)."""
        # TODO: Update this with the new Python 3.10 "match" switch statement
        if letter == 0:
            if len(self.b) == 0:
                song = "Empty"
            else:
                song = random.choice(self.b)
                self.b.remove(song)
        elif letter == 1:
            if len(self.i) == 0:
                song = "Empty"
            else:
                song = random.choice(self.i)
                self.i.remove(song)
        elif letter == 2:
            if len(self.n) == 0:
                song = "Empty"
            else:
                song = random.choice(self.n)
                self.n.remove(song)
        elif letter == 3:
            if len(self.g) == 0:
                song = "Empty"
            else:
                song = random.choice(self.g)
                self.g.remove(song)
        elif letter == 4:
            if len(self.o) == 0:
                song = "Empty"
            else:
                song = random.choice(self.o)
                self.o.remove(song)

        # Update the chosen song label
        self.chosen_song.config(text=f"{song}")

        # Return if the column is empty
        if song == "Empty":
            return

        # Add the random song to the "Played Songs" Listbox
        self.played.insert(tk.END, song)

        # Remove the random song from the "Available Songs" Listbox
        for i, element in enumerate(self.list.get(0, tk.END)):
            if element == song:
                self.list.delete(i)

        # Remove the random song from the current list of available songs
        self.current_list.remove(song)


window = BingoChecker()
window.mainloop()
