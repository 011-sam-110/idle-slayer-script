import json
from tracemalloc import start
import pyautogui, keyboard
import time

SPACE_PRESSES_PER_SECOND = 8
SPACE_DURATION = 1      # seconds
WAIT_AFTER_SPACE = 0.5  # seconds
SPACE_INTERVAL = 1 / SPACE_PRESSES_PER_SECOND

def getConfigSettings(settings : list):   
    """"""
    returnedSettings = []
    with open("src/config.json") as file:
        config = json.load(file)
        for setting in settings:
            returnedSettings.append(config[setting])

    return returnedSettings

def movementCycle():
    """"""
    while True:
        time.sleep(1)
        movement_enabled, paused, high_jump_enabled, rage_enabled = getConfigSettings(
            ["movement", "paused", "high_jump", "use_rage"])

        while movement_enabled and paused == False:
            time.sleep(.2)
            while paused == False:
                time.sleep(.2)
                start_time = time.time()
                print("movement cycle")
                while time.time() - start_time < SPACE_DURATION:
                    keyboard.press_and_release("space")
                    time.sleep(SPACE_INTERVAL)

                if high_jump_enabled:
                    time.sleep(0.2)
                    pyautogui.keyDown("space")
                    time.sleep(0.3)
                    pyautogui.keyUp("space")

                if rage_enabled:
                    keyboard.press_and_release("r")

#               Check if paused
                paused, movement_enabled = getConfigSettings(["paused", "movement"])