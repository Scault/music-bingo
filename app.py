import tkinter as tk
from PIL import Image, ImageTk
from prototype import generate_card


class LoadWindow(object):
    """The Load Card pop-up window."""

    def __init__(self, master) -> None:
        """Initializes the Load Card Window.

        Args:
            master: the parent window
        """
        self.top = tk.Toplevel(master)
        self.top.geometry("200x75")
        self.top.resizable(False, False)
        icon = tk.PhotoImage(file="imgs/icon.png")
        self.top.wm_iconphoto(False, icon)
        self.frame = tk.Frame(self.top)
        self.frame.pack(anchor="nw", fill="both", expand=1)
        self.label = tk.Label(self.frame, text="Enter Seed:")
        self.label.pack(anchor="center", fill="both", expand=1)
        self.entry = tk.Entry(self.frame)
        self.entry.pack(anchor="center")
        self.button = tk.Button(self.frame, text="Ok", command=self.cleanup)
        self.button.pack(anchor="center")

    def cleanup(self) -> None:
        """Destroys the Load Card window and retrieves the user entry."""
        self.value = self.entry.get()
        self.top.destroy()


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
        self.init_menu()
        self.init_canvas()
        self.bind("<Control-z>", lambda e: self.clear())
        self.bind("<Control-l>", lambda e: self.popup())
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
        playlist_menu = tk.Menu(menubar, tearoff=0)
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
            label="Load Card", accelerator="Ctrl+L", command=lambda: self.popup()
        )
        file_menu.add_command(
            label="Generate New Card",
            accelerator="Ctrl+N",
            command=lambda: self.generate_new_card(),
        )

        # Add command(s) to Settings menu
        settings_menu.add_cascade(label="Change Colour", menu=colour_menu)
        settings_menu.add_separator()
        settings_menu.add_cascade(label="Change Cursor Size", menu=size_menu)
        settings_menu.add_separator()
        settings_menu.add_cascade(label="Change Playlist", menu=playlist_menu)

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
        playlist_menu.add_radiobutton(
            label="70s",
            variable=self.playlist,
            value=0,
            command=lambda: self.generate_new_card(),
        )
        playlist_menu.add_radiobutton(
            label="80s",
            variable=self.playlist,
            value=1,
            command=lambda: self.generate_new_card(),
        )
        playlist_menu.add_radiobutton(
            label="90s",
            variable=self.playlist,
            value=2,
            command=lambda: self.generate_new_card(),
        )
        playlist_menu.add_radiobutton(
            label="2000s 1",
            variable=self.playlist,
            value=3,
            command=lambda: self.generate_new_card(),
        )
        playlist_menu.add_radiobutton(
            label="2000s 2",
            variable=self.playlist,
            value=4,
            command=lambda: self.generate_new_card(),
        )
        playlist_menu.add_radiobutton(
            label="2010s 1",
            variable=self.playlist,
            value=5,
            command=lambda: self.generate_new_card(),
        )
        playlist_menu.add_radiobutton(
            label="2010s 2",
            variable=self.playlist,
            value=6,
            command=lambda: self.generate_new_card(),
        )
        playlist_menu.add_radiobutton(
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

    def popup(self) -> None:
        """Opens the Load Card popup window."""
        self.load = LoadWindow(self)
        self.wait_window(self.load.top)
        try:
            if int(self.load.value) == self.seed:
                pass
            else:
                self.generate_new_card(self.load.value)
        except (AttributeError, ValueError):
            pass

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
