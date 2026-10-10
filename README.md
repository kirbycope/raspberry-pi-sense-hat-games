# Raspberry Pi Sense HAT Games

Two games for the [Raspberry Pi Sense HAT](https://www.raspberrypi.com/products/sense-hat/)'s 8x8 RGB LED
matrix and joystick, written in Python with its `sense_hat` library.

**[Play them in your browser](https://timothycope.com/raspberry-pi-sense-hat-games/)**: the same Python files,
run unchanged.

| Game | |
| --- | --- |
| [Space Invaders](spaceInvaders/README.md) | Move the laser cannon left and right, press the joystick in to fire, and clear all six invaders. |
| [The Legend of Zelda](legendOfZelda/README.md) | Walk Link through Tail Cave from Link's Awakening, picking up keys and opening doors. |

## On a Raspberry Pi

With the Sense HAT fitted, run a game from the top of this repository:

```bash
python3 spaceInvaders/space_invaders.py
python3 legendOfZelda/legend_of_zelda.py
```

## On a computer: the simulator

`simulator/` holds a stand-in for the `sense_hat` library and a window to show it in, so the games run on a
Mac, Windows or Linux machine without a Pi. The games' code is not changed: the simulator puts its own
`sense_hat` first on the path, and the games import it as usual.

```bash
python3 simulator/run.py                  # pick a game
python3 simulator/run.py spaceInvaders    # or name its folder
python3 simulator/run.py legendOfZelda
```

| Key | Joystick |
| --- | --- |
| Arrow keys | up, down, left, right (hold to repeat) |
| Enter or Space | press in |

You can also click the joystick in the window.

- **Requirements:** Python 3 with tkinter and nothing else. On a Mac with Homebrew's Python, tkinter comes
  from `brew install python-tk`.
- **Colours:** the stand-in stores colours in 16 bits as the real LEDs do, so a colour read back with
  `get_pixel()` matches the hardware. Zelda relies on that to find doors and keys.
- **The joystick:** its callbacks run on a thread of their own, as on a Pi.

The stand-in's tests:

```bash
python3 -m unittest discover tests
```

## In a browser: the web version

`web/` is the page. It runs the games with [Pyodide](https://pyodide.org), which is Python compiled to
WebAssembly, in a background worker, against the same stand-in `sense_hat`.

- **Threads:** a browser has no threads, so `threading.Timer` becomes a browser timer.
- **Sleeping:** `time.sleep()` pauses only the worker, so the LEDs stay on screen while a game waits.
- **Publishing:** GitHub Actions publishes it to GitHub Pages on every push to `master`
  (`.github/workflows/web.yml`).

To try it locally:

```bash
python3 web/build.py site
python3 -m http.server -d site            # then open http://localhost:8000
```

## Layout

| Path | Holds |
| --- | --- |
| `spaceInvaders/`, `legendOfZelda/` | The games, their pixel art and the images they load. |
| `simulator/sense_hat/` | The stand-in `sense_hat` library, shared by the desktop and web versions. |
| `simulator/run.py` | The desktop simulator's window. |
| `web/` | The web page, its Pyodide worker and the script that gathers the site. |
| `tests/` | Tests for the stand-in. |
