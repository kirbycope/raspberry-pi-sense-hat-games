"""Plays the Sense HAT games on a desktop, without a Raspberry Pi.

    python simulator/run.py                    # pick a game
    python simulator/run.py spaceInvaders      # or name its folder
    python simulator/run.py legendOfZelda

The game's own code runs unchanged: this puts the stand-in sense_hat package
(simulator/sense_hat) first on the path, so `from sense_hat import SenseHat`
finds it, and shows the LEDs in a window. The arrow keys move the joystick
and Enter or Space presses it in; you can also click the joystick. Needs
Python 3 with tkinter, and nothing else.
"""

import os
import runpy
import sys
import threading
import tkinter as tk

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import sense_hat  # noqa: E402  (the stand-in)

GAMES = {
    "spaceInvaders": ("Space Invaders", "spaceInvaders/space_invaders.py"),
    "legendOfZelda": ("The Legend of Zelda", "legendOfZelda/legend_of_zelda.py"),
}

PCB = "#0b6b3a"
PCB_EDGE = "#08502b"
OFF = "#202020"
CELL, GAP = 46, 8
KEYS = {"Up": "up", "Down": "down", "Left": "left", "Right": "right", "Return": "middle", "space": "middle"}


class Board:
    def __init__(self, root):
        self.root = root
        self.pixels = [[0, 0, 0]] * 64
        self.low_light = False
        self.dirty = True
        self.held = set()
        size = 8 * CELL + 7 * GAP
        self.ox, self.oy = 40, 40
        w = self.ox + size + 40 + 200
        h = self.oy + size + 40
        self.canvas = tk.Canvas(root, width=w, height=h, bg=PCB, highlightthickness=0)
        self.canvas.pack()
        c = self.canvas
        c.create_rectangle(4, 4, w - 4, h - 4, outline=PCB_EDGE, width=4)
        for x, y in ((18, 18), (w - 18, 18), (18, h - 18), (w - 18, h - 18)):
            c.create_oval(x - 9, y - 9, x + 9, y + 9, fill="#c9a557", outline="")
            c.create_oval(x - 5, y - 5, x + 5, y + 5, fill="#111", outline="")
        c.create_rectangle(self.ox - 10, self.oy - 10, self.ox + size + 10, self.oy + size + 10, fill="#111", outline="")
        self.leds = []
        for i in range(64):
            x0 = self.ox + (i % 8) * (CELL + GAP)
            y0 = self.oy + (i // 8) * (CELL + GAP)
            self.leds.append(c.create_rectangle(x0, y0, x0 + CELL, y0 + CELL, fill=OFF, outline="#2c2c2c", width=2))
        # The joystick: a cross of four arrows round a centre press.
        jx, jy = self.ox + size + 140, self.oy + size // 2
        c.create_text(jx, self.oy + 4, text="Sense HAT", fill="#e8f5ec", font=("Helvetica", 16, "bold"))
        c.create_oval(jx - 70, jy - 70, jx + 70, jy + 70, fill="#0a5a31", outline="#0e7c44", width=2)
        self.pads = {}
        for direction, dx, dy, label in (("up", 0, -44, "^"), ("down", 0, 44, "v"), ("left", -44, 0, "<"),
                                         ("right", 44, 0, ">"), ("middle", 0, 0, "o")):
            r = 22 if direction == "middle" else 18
            pad = c.create_oval(jx + dx - r, jy + dy - r, jx + dx + r, jy + dy + r, fill="#d9d9d9", outline="#8a8a8a", width=2)
            text = c.create_text(jx + dx, jy + dy, text=label, fill="#333", font=("Helvetica", 14, "bold"))
            self.pads[direction] = pad
            for item in (pad, text):
                c.tag_bind(item, "<ButtonPress-1>", lambda e, d=direction: self.down(d))
                c.tag_bind(item, "<ButtonRelease-1>", lambda e, d=direction: self.up(d))
        c.create_text(jx, jy + 100, text="Arrow keys move\nEnter or Space presses", fill="#cfe9d8",
                      font=("Helvetica", 12), justify="center")
        root.bind("<KeyPress>", self.key_down)
        root.bind("<KeyRelease>", self.key_up)
        sense_hat.set_display_hook(self.update)
        self.tick()

    def update(self, pixels, low_light):
        # Called from the game's threads; the window redraws from tick().
        self.pixels, self.low_light, self.dirty = pixels, low_light, True

    def tick(self):
        if self.dirty:
            self.dirty = False
            scale = 0.55 if self.low_light else 1.0
            for item, (r, g, b) in zip(self.leds, self.pixels):
                if r or g or b:
                    # Lit LEDs never look quite black, however dim the colour.
                    r, g, b = (min(255, int(v * scale) + 20) for v in (r, g, b))
                    self.canvas.itemconfigure(item, fill=f"#{r:02x}{g:02x}{b:02x}")
                else:
                    self.canvas.itemconfigure(item, fill=OFF)
        self.root.after(16, self.tick)

    def down(self, direction):
        action = sense_hat.ACTION_HELD if direction in self.held else sense_hat.ACTION_PRESSED
        self.held.add(direction)
        self.canvas.itemconfigure(self.pads[direction], fill="#ffd678")
        sense_hat.press(direction, action)

    def up(self, direction):
        if direction in self.held:
            self.held.discard(direction)
            self.canvas.itemconfigure(self.pads[direction], fill="#d9d9d9")
            sense_hat.press(direction, sense_hat.ACTION_RELEASED)

    def key_down(self, e):
        if e.keysym in KEYS:
            self.down(KEYS[e.keysym])

    def key_up(self, e):
        if e.keysym in KEYS:
            self.up(KEYS[e.keysym])


def run_game(folder):
    title, path = GAMES[folder]
    # The games load images by paths from the repository's top level and import
    # helpers from their own folder, as when run on a Pi from there.
    os.chdir(ROOT)
    sys.path.insert(0, os.path.join(ROOT, folder))
    threading.Thread(target=runpy.run_path, args=(os.path.join(ROOT, path),), kwargs={"run_name": "__main__"},
                     daemon=True).start()
    return title


def pick(root, then):
    frame = tk.Frame(root, bg=PCB, padx=40, pady=30)
    frame.pack()
    tk.Label(frame, text="Sense HAT Games", bg=PCB, fg="white", font=("Helvetica", 20, "bold")).pack(pady=(0, 16))
    for folder, (title, _) in GAMES.items():
        tk.Button(frame, text=title, width=22, command=lambda f=folder: (frame.destroy(), then(f))).pack(pady=6)


def main():
    root = tk.Tk()
    root.title("Sense HAT Games")
    root.configure(bg=PCB)
    root.resizable(False, False)
    # The games' timer threads never end on their own, so closing the window ends everything.
    root.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))

    def start(folder):
        Board(root)
        root.title(run_game(folder) + " - Sense HAT simulator")

    # SHG_SHOT=<file.png> [SHG_SHOT_AFTER=<ms>]: saves the window as a picture, then quits (macOS only).
    shot = os.environ.get("SHG_SHOT")
    if shot:
        def capture():
            root.lift()
            root.update()
            x, y, w, h = root.winfo_rootx(), root.winfo_rooty(), root.winfo_width(), root.winfo_height()
            os.system(f"screencapture -x -R{x},{y},{w},{h} '{shot}'")
            os._exit(0)
        root.after(int(os.environ.get("SHG_SHOT_AFTER", "2500")), capture)

    choice = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else None
    if choice:
        if choice not in GAMES:
            sys.exit(f"unknown game {choice!r}; pick one of: {', '.join(GAMES)}")
        start(choice)
    else:
        pick(root, start)
    root.mainloop()
    os._exit(0)


if __name__ == "__main__":
    main()
