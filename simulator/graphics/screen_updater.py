import time
import graphics.layers as layers


layer: layers.Layer = None
last_update = 0
view = None


def refresh():
    global layer
    global last_update
    global view
    curr_time = time.time_ns() / 1000000
    if last_update + 16 <= curr_time:
        layer.move(view.keys_used, view.move_WASD)
        view.update_idletasks()
        last_update = time.time_ns() / 1000000
        