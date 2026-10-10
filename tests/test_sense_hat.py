"""Tests for the simulator's stand-in sense_hat package.

    python -m unittest discover tests
"""

import os
import sys
import threading
import time
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "simulator"))

import sense_hat  # noqa: E402
from sense_hat import ACTION_PRESSED, SenseHat  # noqa: E402


class LedTests(unittest.TestCase):
    def setUp(self):
        self.sense = SenseHat()
        self.sense.clear()

    def test_colours_read_back_as_the_hardware_stores_them(self):
        # 5 bits of red, 6 of green, 5 of blue, as Zelda's door check relies on.
        self.sense.set_pixel(0, 0, 150, 75, 0)
        self.assertEqual(self.sense.get_pixel(0, 0), [144, 72, 0])
        self.sense.set_pixel(1, 0, [192, 192, 192])
        self.assertEqual(self.sense.get_pixel(1, 0), [192, 192, 192])

    def test_bad_positions_and_colours_are_refused(self):
        with self.assertRaises(ValueError):
            self.sense.set_pixel(8, 0, 255, 0, 0)
        with self.assertRaises(ValueError):
            self.sense.set_pixel(0, 0, 256, 0, 0)

    def test_load_image_reads_the_games_bitmaps(self):
        pixels = self.sense.load_image(os.path.join(ROOT, "legendOfZelda/img/loz_link.bmp"))
        self.assertEqual(len(pixels), 64)
        self.assertEqual(self.sense.get_pixels()[1], [0, 252, 0])  # green cap, as stored

    def test_show_letter_lights_the_letter(self):
        self.sense.show_letter("W", text_colour=[255, 0, 0])
        lit = sum(1 for p in self.sense.get_pixels() if p != [0, 0, 0])
        self.assertGreater(lit, 10)

    def test_display_hook_sees_every_change(self):
        seen = []
        sense_hat.set_display_hook(lambda px, low: seen.append(px[2]))
        self.sense.set_pixel(2, 0, 0, 0, 255)
        self.assertEqual(seen[-1], [0, 0, 248])


class StickTests(unittest.TestCase):
    def test_callbacks_run_off_the_callers_thread(self):
        # As on a Pi, so a callback that sleeps does not hold up whoever pressed.
        sense = SenseHat()
        got = threading.Event()
        threads = []

        def pushed(event):
            threads.append(threading.current_thread())
            self.assertEqual(event.action, ACTION_PRESSED)
            got.set()

        sense.stick.direction_left = pushed
        sense_hat.press("left")
        self.assertTrue(got.wait(1))
        self.assertIsNot(threads[0], threading.current_thread())
        sense.stick.direction_left = None

    def test_events_queue_for_get_events(self):
        sense = SenseHat()
        sense.stick.get_events()
        sense_hat.press("up")
        time.sleep(0.05)
        events = sense.stick.get_events()
        self.assertEqual([e.direction for e in events], ["up"])


if __name__ == "__main__":
    unittest.main()
