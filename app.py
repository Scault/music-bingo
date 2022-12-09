import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring, askinteger
from PIL import Image, ImageTk
from prototype import generate_card, add_custom_playlist, spotify, SpotifyException


class Window(tk.Tk):
    """The Bingo application window."""

    def __init__(self) -> None:
        """Initializes the Bingo application window."""
        tk.Tk.__init__(self)
        self.title("Bingo!")
        self.geometry("600x750")
        self.resizable(False, False)
        icon = tk.PhotoImage(file="imgs/icon.png")
        self.wm_iconphoto(False, icon)
        self.color = "red"
        self.actions = []
        self.seed = "Unknown"
        self.playlist_count = 8
        self.init_menu()
        self.init_canvas()
        self.bind("<Control-z>", lambda e: self.clear())
        self.bind("<Control-l>", lambda e: self.load_seed())
        self.bind("<Control-n>", lambda e: self.generate_new_card())

    def init_menu(self) -> None:
        """Initializes the menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Initialize menus
        file_menu = tk.Menu(menubar, tearoff=0)
        settings_menu = tk.Menu(menubar, tearoff=0)
        colour_menu = tk.Menu(menubar, tearoff=0)
        size_menu = tk.Menu(menubar, tearoff=0)
        self.playlist_menu = tk.Menu(menubar, tearoff=0)
        self.info_menu = tk.Menu(menubar, tearoff=0)

        # Create main menus
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        menubar.add_cascade(label="Info", menu=self.info_menu)

        # Add command(s) to File menu
        file_menu.add_command(
            label="Clear Card", accelerator="Ctrl+Z", command=lambda: self.clear()
        )
        file_menu.add_command(
            label="Load Card", accelerator="Ctrl+L", command=lambda: self.load_seed()
        )
        file_menu.add_command(
            label="Generate New Card",
            accelerator="Ctrl+N",
            command=lambda: self.generate_new_card(),
        )
        file_menu.add_command(
            label="Select Custom Playlist",
            command=lambda: self.custom_playlist(),
        )

        # Add command(s) to Settings menu
        settings_menu.add_cascade(label="Change Colour", menu=colour_menu)
        settings_menu.add_separator()
        settings_menu.add_cascade(label="Change Cursor Size", menu=size_menu)
        settings_menu.add_separator()
        settings_menu.add_cascade(label="Change Playlist", menu=self.playlist_menu)

        # Add colour selections to Colour menu
        self.colour = tk.StringVar()
        self.colour.set("red")
        colour_menu.add_radiobutton(label="Red", variable=self.colour, value="red")
        colour_menu.add_radiobutton(label="Blue", variable=self.colour, value="blue")
        colour_menu.add_radiobutton(label="Green", variable=self.colour, value="green")

        # Add cursor size selections to Size menu
        self.cursor_size = tk.IntVar()
        self.cursor_size.set(20)
        size_menu.add_radiobutton(label="Small", variable=self.cursor_size, value=10)
        size_menu.add_radiobutton(label="Medium", variable=self.cursor_size, value=20)
        size_menu.add_radiobutton(label="Large", variable=self.cursor_size, value=30)

        # Add playlists to Playlist menu
        self.playlist = tk.IntVar()
        self.playlist.set(0)
        self.playlist_menu.add_radiobutton(
            label="70s",
            variable=self.playlist,
            value=0,
            command=lambda: self.generate_new_card(),
        )
        self.playlist_menu.add_radiobutton(
            label="80s",
            variable=self.playlist,
            value=1,
            command=lambda: self.generate_new_card(),
        )
        self.playlist_menu.add_radiobutton(
            label="90s",
            variable=self.playlist,
            value=2,
            command=lambda: self.generate_new_card(),
        )
        self.playlist_menu.add_radiobutton(
            label="2000s 1",
            variable=self.playlist,
            value=3,
            command=lambda: self.generate_new_card(),
        )
        self.playlist_menu.add_radiobutton(
            label="2000s 2",
            variable=self.playlist,
            value=4,
            command=lambda: self.generate_new_card(),
        )
        self.playlist_menu.add_radiobutton(
            label="2010s 1",
            variable=self.playlist,
            value=5,
            command=lambda: self.generate_new_card(),
        )
        self.playlist_menu.add_radiobutton(
            label="2010s 2",
            variable=self.playlist,
            value=6,
            command=lambda: self.generate_new_card(),
        )
        self.playlist_menu.add_radiobutton(
            label="2010s 3",
            variable=self.playlist,
            value=7,
            command=lambda: self.generate_new_card(),
        )

        # Add command(s) to Info menu
        self.info_menu.add_command(label=f"Seed: {self.seed}", state="disabled")

    def init_canvas(self) -> None:
        """Initializes the canvas."""
        image = Image.open("imgs/overlay.jpg")
        image = image.resize((600, 750), Image.Resampling.LANCZOS)
        self.im = ImageTk.PhotoImage(image)
        self.im_cv = tk.Canvas(self)
        self.im_cv.pack(anchor="nw", fill="both", expand=1)
        self.im_cv.create_image(0, 0, image=self.im, anchor="nw")
        self.im_cv.bind("<B1-Motion>", self.paint)

    def clear(self) -> None:
        """Clears all drawing on the canvas."""
        while self.actions:
            action = self.actions.pop()
            self.im_cv.delete(action)

    def generate_new_card(self, seed=None) -> None:
        """Generates a new bingo card on the canvas.

        Args:
            seed: seed to use for card generation
        """
        if seed:
            self.seed = generate_card(seed, self.playlist.get())
        else:
            self.seed = generate_card(playlist=self.playlist.get())

        self.im_cv.delete("all")
        image = Image.open(f"output/bingo_card-{self.seed}.jpg")
        image = image.resize((600, 750), Image.Resampling.LANCZOS)
        self.im = ImageTk.PhotoImage(image)
        self.im_cv.pack(anchor="nw", fill="both", expand=1)
        self.im_cv.create_image(0, 0, image=self.im, anchor="nw")
        self.info_menu.entryconfigure(1, label=f"Seed: {self.seed}")

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
                command=lambda: self.generate_new_card(),
            )
        self.playlist.set(self.playlist_count)
        self.playlist_count += 1
        self.generate_new_card()

    def load_seed(self) -> None:
        """Opens the Load Card popup window."""
        seed = askinteger("Load Card", "Enter a seed:\t\t\t\t")

        if seed == self.seed or seed is None:
            return
        self.generate_new_card(seed)

    def paint(self, event) -> None:
        """Paint on the canvas using the user's mouse.

        Args:
            event: an event passed by Canvas.bind()
        """
        x1, y1 = (event.x - self.cursor_size.get()), (event.y - self.cursor_size.get())
        x2, y2 = (event.x + self.cursor_size.get()), (event.y + self.cursor_size.get())
        action = self.im_cv.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill=self.colour.get(),
            width=0,
            outline=self.colour.get(),
            stipple="gray25",
        )
        self.actions.append(action)
        self.my_canvas = action


window = Window()
window.mainloop()
