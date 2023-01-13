import random
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.simpledialog import askstring
from prototype import (
    spotify,
    SpotifyException,
    get_song_list,
    PLAYLISTS,
    add_custom_playlist,
    generate_24_numbers,
)

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
    [1, 7, 18, 23],
    [5, 9, 16, 20],
]


class Window(tk.Tk):
    """The Bingo Checker application window."""

    def __init__(self) -> None:
        """Initializes the Bingo Checker application window."""
        tk.Tk.__init__(self)
        self.title("Bingo Card Checker")
        self.geometry("800x605")
        self.resizable(True, True)
        self.playlist_count = 8
        self.song_list = []
        self.init_gui()
        self.init_menu()
        self.load_playlist()

    def init_gui(self) -> None:
        """Initializes the GUI for the application."""
        # Create top level frames
        top_frame = tk.Frame(self)
        separator = ttk.Separator(self, orient="vertical")
        bottom_frame = tk.Frame(self)

        # Create top-most frame contents
        self.search = tk.Entry(top_frame)
        playlist_label = tk.Label(top_frame, text="Available Songs")
        self.list = tk.Listbox(top_frame, exportselection=False)
        add_button = tk.Button(top_frame, text=">>", command=self.add_song)
        remove_button = tk.Button(top_frame, text="<<", command=self.remove_song)
        played_label = tk.Label(top_frame, text="Played Songs")
        self.played = tk.Listbox(top_frame, exportselection=False)

        # Create bottom-most frame contents
        seed_label = tk.Label(bottom_frame, text="Seed")
        self.seed = tk.Entry(bottom_frame)
        check_button = tk.Button(bottom_frame, text="Check", command=self.check_seed)

        # Setup playlist scrollbars
        h_scrollbar_1 = tk.Scrollbar(top_frame, orient="horizontal")
        h_scrollbar_1.config(command=self.list.xview)
        h_scrollbar_1.grid(row=4, column=0, sticky="ew")
        v_scrollbar_1 = tk.Scrollbar(top_frame, orient="vertical")
        v_scrollbar_1.config(command=self.list.yview)
        v_scrollbar_1.grid(row=2, column=1, rowspan=2, sticky="nsw")
        self.list.config(
            yscrollcommand=v_scrollbar_1.set, xscrollcommand=h_scrollbar_1.set
        )

        # Setup played scrollbars
        h_scrollbar_2 = tk.Scrollbar(top_frame, orient="horizontal")
        h_scrollbar_2.config(command=self.played.xview)
        h_scrollbar_2.grid(row=4, column=3, sticky="ew")
        v_scrollbar_2 = tk.Scrollbar(top_frame, orient="vertical")
        v_scrollbar_2.config(command=self.played.yview)
        v_scrollbar_2.grid(row=2, column=4, rowspan=2, sticky="ns")
        self.played.config(
            yscrollcommand=v_scrollbar_2.set, xscrollcommand=h_scrollbar_2.set
        )

        # Align top-most frame contents
        self.search.grid(row=0, column=0, sticky="ew")
        playlist_label.grid(row=1, column=0, sticky="s")
        played_label.grid(row=1, column=3, sticky="s")
        self.list.grid(row=2, column=0, rowspan=4, sticky="nsew")
        add_button.grid(row=2, column=2, sticky="s", padx=5, pady=2.5)
        self.played.grid(row=2, column=3, rowspan=3, sticky="nsew")
        remove_button.grid(row=3, column=2, sticky="n", padx=5, pady=2.5)

        # Align bottom-most frame contents
        seed_label.grid(row=0, column=0)
        self.seed.grid(row=1, column=0, pady=5)
        check_button.grid(row=2, column=0)

        # Align top level frames
        top_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        separator.grid(row=1, column=0)
        bottom_frame.grid(row=2, column=0, padx=10, pady=10)

        # Configure window
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Configure grid
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=0)
        top_frame.columnconfigure(2, weight=0)
        top_frame.columnconfigure(3, weight=1)
        top_frame.columnconfigure(4, weight=0)
        top_frame.rowconfigure(0, weight=0)
        top_frame.rowconfigure(1, weight=0)
        top_frame.rowconfigure(2, weight=1)
        top_frame.rowconfigure(3, weight=1)
        top_frame.rowconfigure(4, weight=0)

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

    def add_song(self) -> None:
        """Adds a song to the 'Played' ListBox."""
        if self.list.curselection() == ():
            return
        for i in self.list.curselection():
            song = self.list.get(i)
            self.played.insert(tk.END, song)
            self.list.delete(i)

        self.current_list.remove(song)

    def remove_song(self) -> None:
        """Removes a song from the 'Played' ListBox."""
        if self.played.curselection() == ():
            return
        for i in self.played.curselection():
            song = self.played.get(i)
            self.list.insert(tk.END, song)
            self.played.delete(i)

        self.current_list.append(song)

    def update(self, data: list) -> None:
        """Updates the 'Playlist' ListBox.

        Args:
            data: a list where each item is an entry in the ListBox
        """
        # Clear listbox
        self.list.delete(0, tk.END)

        # Add contents
        for item in data:
            self.list.insert(tk.END, item)

    def fill_search(self, event: tk.Event) -> None:
        """Fills the search bar with the selection in the 'Playlist' ListBox.

        Args:
            event: an event passed by Listbox.bind()
        """
        self.search.delete(0, tk.END)
        self.search.insert(0, self.list.get(tk.ACTIVE))

    def check_entry(self, event: tk.Event) -> None:
        """Updates the 'Played' ListBox with the typed string in the search box.

        Args:
            event: an event passed by Entry.bind()
        """
        typed = self.search.get()

        if typed == "":
            data = self.current_list
        else:
            data = []
            for item in self.current_list:
                if typed.lower() in item.lower():
                    data.append(item)

        self.update(data)

    def check_seed(self) -> None:
        """Checks a given seed to see if it is a winning bingo card."""
        if self.seed.get() == "":
            return

        old_state = random.getstate()
        random.seed(int(self.seed.get()))
        nums = generate_24_numbers(self.playlist.get())
        random.setstate(old_state)

        lines = []
        for i in COMPLETE_LINES:
            line = []
            for num in i:
                x = nums[num - 1]
                line.append(self.song_list[x])
            lines.append(line)

        played = self.played.get(0, tk.END)

        count = 0
        for line in lines:
            if set(played).issuperset(set(line)):
                count += 1

        if count >= 2:
            messagebox.showinfo("Congratulations!", "This card is a winner!")

        else:
            # random.seed(random.randint(1000000, 99999999))
            messagebox.showerror("WRONG", random.choice(RUDE_MESSAGES))

    def load_playlist(self, seed: int = None) -> None:
        """Loads a playlist to display in the 'Playlist' window.

        Args:
            seed: seed to use for card generation
        """
        self.song_list = get_song_list(PLAYLISTS[self.playlist.get()])
        self.list.delete(0, tk.END)
        self.played.delete(0, tk.END)
        temp_list = []
        for i, song in enumerate(self.song_list):
            title = song[0].rsplit(" - ")[0]
            temp_list.append(f"{title} - {song[1]}")
            self.list.insert(i, f"{title} - {song[1]}")
        self.song_list = temp_list
        random.Random(1).shuffle(self.song_list)
        self.current_list = list(self.list.get(0, tk.END))

    def custom_playlist(self):
        """Opens the Playlist popup window."""
        url = askstring("Add Custom Playlist", "Enter Spotify playlist URL:\t\t\t\t")

        if url is None:
            return

        try:
            num_songs = spotify.playlist(url)["tracks"]["total"]
            if num_songs < 25:
                messagebox.showerror("Error", "Playlist must be longer than 24 songs.")
                return
        except SpotifyException:
            return

        if add_custom_playlist(url):
            self.playlist_menu.add_radiobutton(
                label="Custom Playlist",
                variable=self.playlist,
                value=self.playlist_count,
                command=lambda: self.load_playlist(),
            )
        self.playlist.set(self.playlist_count)
        self.playlist_count += 1
        self.load_playlist()


window = Window()
window.mainloop()
