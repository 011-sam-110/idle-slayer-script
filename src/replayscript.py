import json
import time
import pyautogui



def replay():

    INPUT_FILE = "jumps.json"
    
    # Load jump data
    with open(INPUT_FILE, "r") as f:
        jumps = json.load(f)
    start_time = time.perf_counter()

    for jump in jumps:
        # Wait until it's time for this jump
        target_time = jump["time"]
        while (time.perf_counter() - start_time) < target_time:
            time.sleep(0.001)

        # Perform jump
        pyautogui.keyDown("space")
        time.sleep(jump["hold_duration"])
        pyautogui.keyUp("space")

        print(f"Jumped ({jump['type']}) at {jump['time']}s")

print("trial finished")