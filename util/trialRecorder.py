import keyboard
import time
import json

#generated with chatGPT, prompt:

# ---------------- CONFIG ----------------
HIGH_JUMP_THRESHOLD = 0.18   # seconds (tweak this)
OUTPUT_FILE = "jumps.json"
# ----------------------------------------

start_time = time.perf_counter()
space_down_time = None
recorded_jumps = []

def on_space_down(e):
    global space_down_time
    if space_down_time is None:
        space_down_time = time.perf_counter()

def on_space_up(e):
    global space_down_time

    if space_down_time is None:
        return

    release_time = time.perf_counter()
    hold_duration = release_time - space_down_time
    timestamp = space_down_time - start_time

    jump_type = "high" if hold_duration >= HIGH_JUMP_THRESHOLD else "short"

    jump = {
        "time": round(timestamp, 4),
        "hold_duration": round(hold_duration, 4),
        "type": jump_type
    }

    recorded_jumps.append(jump)
    print(jump)

    space_down_time = None

# Hooks
keyboard.on_press_key("space", on_space_down)
keyboard.on_release_key("space", on_space_up)

print("Recording jumps... Press ESC to stop.")
keyboard.wait("esc")

# Save to file
with open(OUTPUT_FILE, "w") as f:
    json.dump(recorded_jumps, f, indent=4)

print(f"Saved {len(recorded_jumps)} jumps to {OUTPUT_FILE}")