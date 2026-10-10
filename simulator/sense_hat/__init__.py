"""A stand-in for the Raspberry Pi Sense HAT's Python library.

The games import `sense_hat` exactly as they do on a Pi. When the simulator
puts this package first on the path, they get this one instead: the same
API, with the 8x8 LED matrix and the joystick provided by a window
(simulator/run.py) or a web page (web/). No game code changes.

It behaves like the hardware where the games can tell:

- The LEDs store colours in 16 bits (5 red, 6 green, 5 blue), as the real
  framebuffer does, so get_pixel() returns what the hardware would:
  (150, 75, 0) reads back as (144, 72, 0).
- Joystick callbacks run on a thread of their own, as the real library's do,
  so a callback that sleeps (Zelda's item pickup) does not freeze the display.

Front ends call set_display_hook() to be told whenever the LEDs change and
press() to feed joystick events in.
"""

import threading
import time
from collections import namedtuple

from ._bmp import read_bmp
from ._font import glyph

__all__ = [
    "SenseHat", "SenseStick", "InputEvent",
    "ACTION_PRESSED", "ACTION_RELEASED", "ACTION_HELD",
    "DIRECTION_UP", "DIRECTION_DOWN", "DIRECTION_LEFT", "DIRECTION_RIGHT", "DIRECTION_MIDDLE",
]

ACTION_PRESSED = "pressed"
ACTION_RELEASED = "released"
ACTION_HELD = "held"
DIRECTION_UP = "up"
DIRECTION_DOWN = "down"
DIRECTION_LEFT = "left"
DIRECTION_RIGHT = "right"
DIRECTION_MIDDLE = "middle"

InputEvent = namedtuple("InputEvent", ("timestamp", "direction", "action"))

# The one LED matrix, shared by every SenseHat() a program makes, as on the
# hardware. Each entry is a packed RGB565 value.
_leds = [0] * 64
_lock = threading.RLock()
_hooks = []
_low_light = False
_stick = None
# Callbacks run here rather than on the caller's thread. On the web there are
# no threads, so the front end sets this to call straight through.
_run_callback = None


def set_display_hook(fn):
    """fn(pixels, low_light) is called after every change, with 64 [r, g, b] lists."""
    _hooks.append(fn)
    fn(_pixels(), _low_light)


def _pack(rgb):
    r, g, b = (int(v) for v in rgb)
    for v in (r, g, b):
        if not 0 <= v <= 255:
            raise ValueError(f"Pixel elements must be between 0 and 255, got {rgb}")
    return ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)


def _unpack(packed):
    return [((packed >> 11) & 0x1F) << 3, ((packed >> 5) & 0x3F) << 2, (packed & 0x1F) << 3]


def _pixels():
    return [_unpack(p) for p in _leds]


def _changed():
    pixels = _pixels()
    for fn in _hooks:
        fn(pixels, _low_light)


def press(direction, action=ACTION_PRESSED):
    """Feeds a joystick event in, as if the stick had moved."""
    if _stick is not None:
        _stick._event(direction, action)


class SenseStick:
    def __init__(self):
        self._callbacks = {}
        self._queue = []
        self._pending = []
        self._cond = threading.Condition()
        self._worker = None

    def _event(self, direction, action):
        event = InputEvent(time.time(), direction, action)
        with self._cond:
            self._queue.append(event)
            self._cond.notify_all()
        callbacks = [self._callbacks.get(direction), self._callbacks.get("any")]
        for cb in callbacks:
            if cb is not None:
                self._call(cb, event)

    def _call(self, cb, event):
        def run():
            try:
                cb(event)
            except TypeError:
                cb()  # the real library also accepts callbacks without the event
        if _run_callback is not None:
            _run_callback(run)
            return
        # One worker thread runs the callbacks in order, like the real stick thread.
        with self._cond:
            self._pending.append(run)
            if self._worker is None:
                self._worker = threading.Thread(target=self._drain, daemon=True)
                self._worker.start()
            self._cond.notify_all()

    def _drain(self):
        while True:
            with self._cond:
                while not self._pending:
                    self._cond.wait()
                run = self._pending.pop(0)
            try:
                run()
            except Exception:
                import traceback
                traceback.print_exc()

    def get_events(self):
        with self._cond:
            events, self._queue = self._queue, []
        return events

    def wait_for_event(self, emptybuffer=False):
        with self._cond:
            if emptybuffer:
                self._queue = []
            while not self._queue:
                self._cond.wait()
            return self._queue.pop(0)

    def _prop(direction):
        return property(lambda self: self._callbacks.get(direction),
                        lambda self, fn: self._callbacks.__setitem__(direction, fn))

    direction_up = _prop(DIRECTION_UP)
    direction_down = _prop(DIRECTION_DOWN)
    direction_left = _prop(DIRECTION_LEFT)
    direction_right = _prop(DIRECTION_RIGHT)
    direction_middle = _prop(DIRECTION_MIDDLE)
    direction_any = _prop("any")
    del _prop


class SenseHat:
    def __init__(self, *args, **kwargs):
        global _stick
        if _stick is None:
            _stick = SenseStick()
        self._stick = _stick
        self._rotation = 0

    @property
    def stick(self):
        return self._stick

    # The LED matrix

    def _index(self, x, y):
        if not (0 <= x <= 7 and 0 <= y <= 7):
            raise ValueError(f"X position must be between 0 and 7, Y position must be between 0 and 7")
        # Rotation turns the picture as the real library does.
        for _ in range(self._rotation // 90):
            x, y = 7 - y, x
        return y * 8 + x

    def set_pixel(self, x, y, *args):
        rgb = args[0] if len(args) == 1 else args
        with _lock:
            _leds[self._index(x, y)] = _pack(rgb)
        _changed()

    def get_pixel(self, x, y):
        with _lock:
            return _unpack(_leds[self._index(x, y)])

    def set_pixels(self, pixel_list):
        if len(pixel_list) != 64:
            raise ValueError("Pixel lists must have 64 elements")
        with _lock:
            for i, rgb in enumerate(pixel_list):
                _leds[self._index(i % 8, i // 8)] = _pack(rgb)
        _changed()

    def get_pixels(self):
        with _lock:
            return [_unpack(_leds[self._index(i % 8, i // 8)]) for i in range(64)]

    def clear(self, *args):
        rgb = (0, 0, 0) if not args else (args[0] if len(args) == 1 else args)
        self.set_pixels([rgb] * 64)

    def load_image(self, file_path, redraw=True):
        pixels = read_bmp(file_path)
        if redraw:
            self.set_pixels(pixels)
        return pixels

    def set_rotation(self, r=0, redraw=True):
        if r not in (0, 90, 180, 270):
            raise ValueError("Rotation must be 0, 90, 180 or 270 degrees")
        pixels = self.get_pixels()
        self._rotation = r
        if redraw:
            self.set_pixels(pixels)

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, r):
        self.set_rotation(r)

    def flip_h(self, redraw=True):
        p = self.get_pixels()
        flipped = [p[y * 8 + (7 - x)] for y in range(8) for x in range(8)]
        if redraw:
            self.set_pixels(flipped)
        return flipped

    def flip_v(self, redraw=True):
        p = self.get_pixels()
        flipped = [p[(7 - y) * 8 + x] for y in range(8) for x in range(8)]
        if redraw:
            self.set_pixels(flipped)
        return flipped

    @property
    def low_light(self):
        return _low_light

    @low_light.setter
    def low_light(self, value):
        global _low_light
        _low_light = bool(value)
        _changed()

    @property
    def gamma(self):
        return list(range(32))

    @gamma.setter
    def gamma(self, value):
        pass

    def gamma_reset(self):
        pass

    # Text

    def show_letter(self, s, text_colour=(255, 255, 255), back_colour=(0, 0, 0)):
        if len(s) != 1:
            raise ValueError("Only one character may be passed into this method")
        rows = glyph(s)
        pixels = [list(back_colour)] * 64
        for y, row in enumerate(rows):
            for x, on in enumerate(row):
                if on:
                    pixels[y * 8 + x + 1] = list(text_colour)
        self.set_pixels(pixels)

    def show_message(self, text_string, scroll_speed=0.1, text_colour=(255, 255, 255), back_colour=(0, 0, 0)):
        # Columns of the whole message, scrolled right to left one at a time.
        columns = [[False] * 8 for _ in range(8)]
        for ch in text_string:
            rows = glyph(ch)
            width = max((len(r) for r in rows), default=5)
            for x in range(width):
                columns.append([x < len(rows[y]) and bool(rows[y][x]) if y < len(rows) else False for y in range(8)])
            columns.append([False] * 8)
        columns += [[False] * 8 for _ in range(8)]
        for start in range(len(columns) - 7):
            pixels = []
            for y in range(8):
                for x in range(8):
                    pixels.append(list(text_colour) if columns[start + x][y] else list(back_colour))
            self.set_pixels(pixels)
            time.sleep(scroll_speed)

    # Sensors: steady, plausible readings, since a desktop has none.

    def get_humidity(self): return 45.0
    def get_temperature(self): return 24.0
    def get_temperature_from_humidity(self): return 24.0
    def get_temperature_from_pressure(self): return 24.0
    def get_pressure(self): return 1013.25
    def get_orientation_radians(self): return {"pitch": 0.0, "roll": 0.0, "yaw": 0.0}
    def get_orientation_degrees(self): return {"pitch": 0.0, "roll": 0.0, "yaw": 0.0}
    get_orientation = get_orientation_degrees
    def get_compass(self): return 0.0
    def get_compass_raw(self): return {"x": 0.0, "y": 0.0, "z": 0.0}
    def get_gyroscope(self): return {"pitch": 0.0, "roll": 0.0, "yaw": 0.0}
    def get_gyroscope_raw(self): return {"x": 0.0, "y": 0.0, "z": 0.0}
    def get_accelerometer(self): return {"pitch": 0.0, "roll": 0.0, "yaw": 0.0}
    def get_accelerometer_raw(self): return {"x": 0.0, "y": 0.0, "z": 1.0}
    def set_imu_config(self, compass_enabled, gyro_enabled, accel_enabled): pass

    orientation = property(get_orientation_degrees)
    orientation_radians = property(get_orientation_radians)
    compass = property(get_compass)
    gyro = property(get_gyroscope)
    accel = property(get_accelerometer)
    humidity = property(get_humidity)
    temp = property(get_temperature)
    temperature = property(get_temperature)
    pressure = property(get_pressure)
