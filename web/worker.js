// Runs one Sense HAT game in Python, in the background, with Pyodide.
//
// The game's own .py files run unchanged against the simulator's sense_hat
// package. Two things differ from a Pi, both handled here: there are no
// threads in a browser, so threading.Timer becomes a browser timer and the
// joystick's callbacks run straight away; and time.sleep() blocks this
// worker rather than the page, so the LEDs keep showing while a game pauses.
//
// Messages in:  {start: "<game folder>"}, {press: "<direction>", action: "pressed" | "held" | "released"}
// Messages out: {ready}, {leds: [r, g, b, ... x64], low}, {error: "..."}

importScripts("https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js");

let pyodide = null;
const queue = [];

async function boot() {
  pyodide = await loadPyodide();
  const files = await (await fetch("files.json")).json();
  for (const path of files) {
    const data = new Uint8Array(await (await fetch(path)).arrayBuffer());
    const dir = path.split("/").slice(0, -1).join("/");
    if (dir) pyodide.FS.mkdirTree("/game/" + dir);
    pyodide.FS.writeFile("/game/" + path, data);
  }
  pyodide.globals.set("post", (leds, low) => postMessage({ leds: leds.toJs(), low }));
  await pyodide.runPythonAsync(`
import os, sys, threading
import js
from pyodide.ffi import create_once_callable

os.chdir("/game")
sys.path.insert(0, "/game/simulator")
import sense_hat

# No threads here: a Timer is a browser timer, and stick callbacks run at once.
class Timer:
    def __init__(self, interval, function, args=None, kwargs=None):
        self.interval, self.function = interval, function
        self.args, self.kwargs = args or [], kwargs or {}
        self.handle = None
    def _fire(self):
        self.handle = None
        try:
            self.function(*self.args, **self.kwargs)
        except Exception:
            import traceback; traceback.print_exc()
    def start(self):
        self.handle = js.setTimeout(create_once_callable(self._fire), int(self.interval * 1000))
    def cancel(self):
        if self.handle is not None:
            js.clearTimeout(self.handle)
            self.handle = None
    def is_alive(self):
        return self.handle is not None
threading.Timer = Timer
sense_hat._run_callback = lambda run: run()
sense_hat.set_display_hook(lambda px, low: post([v for p in px for v in p], low))
`);
  postMessage({ ready: true });
  while (queue.length) handle(queue.shift());
}

function handle(msg) {
  try {
    if (msg.start) {
      const folder = msg.start;
      pyodide.runPython(`
import runpy, sys
sys.path.insert(0, "/game/${folder}")
runpy.run_path({"spaceInvaders": "spaceInvaders/space_invaders.py",
                "legendOfZelda": "legendOfZelda/legend_of_zelda.py"}["${folder}"], run_name="__main__")
`);
    } else if (msg.press) {
      pyodide.globals.get("sense_hat").press(msg.press, msg.action);
    }
  } catch (e) {
    postMessage({ error: String(e) });
  }
}

onmessage = e => (pyodide ? handle(e.data) : queue.push(e.data));
boot().catch(e => postMessage({ error: String(e) }));
