import keyboard
import time
import json
import pyautogui

SPACE_PRESSES_PER_SECOND = 50
SPACE_DURATION = 1      # seconds
WAIT_AFTER_SPACE = 0.5  # seconds
SPACE_INTERVAL = .8 / SPACE_PRESSES_PER_SECOND

high_jump = None
rage = None


def get_movement_value():
    global high_jump, rage
    """Reads movement value from config.json"""
    try:
        with open("config.json", "r") as file:
            data = json.load(file)
            high_jump = data.get("high_jump", False) #false as a preset
            rage = data.get("rage", False)
            return data.get("movement", False)
            
    except Exception:
        return False

def movementRun():
    print("Press CTRL+C to stop.")
    while True:
        movementValue = get_movement_value()
        if not movementValue:
            # If movement is False, wait a short time and check again
            time.sleep(0.2)
            continue

        # Spam SPACE for SPACE_DURATION seconds
        start_time = time.time()
        while time.time() - start_time < SPACE_DURATION:
            if not get_movement_value():
                break  # stop immediately if movement is turned off
            keyboard.press_and_release("space")
            time.sleep(SPACE_INTERVAL)

        # Wait a bit before next spam burst
        time.sleep(WAIT_AFTER_SPACE)
        if high_jump:
            pyautogui.keyDown("space")
            time.sleep(0.5)
            pyautogui.keyUp("Space") 
            time.sleep(.1)
        if rage:
            keyboard.press_and_release("r")

if __name__ == "__main__":
    run() 