"""
Docstring for chesthunter
"""
import json
import time
import logging
import threading
import pyautogui
from src.replayscript import replay
from src.movement import movementRun
from src.trialtempfix import trialclose
from src.clockTrial import clockTrial
from src.saverChest import findSaverChest
from src.gameOver import findCloseButton
from src.clockChestHunt import clockChestHunt

logger = logging.getLogger(__name__)
pyautogui.FAILSAFE = False
chestPositions = [(392, 650), (571, 653), (791, 666), (1086, 691), (1277, 683),
    (1552, 699), (1789, 692), (2053, 703), (2239, 712), (2486, 722),
    (2460, 913), (2244, 905), (2035, 922), (1792, 903), (1550, 884),
    (1297, 909), (1012, 917), (811, 900), (589, 926), (424, 922), (374, 1167),
    (549, 1143), (846, 1119), (1024, 1129), (1286, 1144), (1498, 1164), (1739, 1156),
    (1989, 1122), (2236, 1160), (2463, 1152)]


def click_pos(x, y):
    """
    Docstring for click_pos | Clicks at the given coordinates

    :param x: X screen coordinate
    :param y: Y screen coordinate
    """
    pyautogui.moveTo(x, y, 0.6)
    time.sleep(1)
    pyautogui.click()
    time.sleep(2)


def close_chest_hunt():
    """
    Docstring for close_chest_hunt
    """
    pyautogui.moveTo(1410, 1623, 0.6)
    pyautogui.click()


def update_movement(value):
    """
    Docstring for update_movement | Disables/Enables cycled movement (jumping/boosting)

    :param value: boolean
    """

    # Load the JSON file
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    config["movement"] = value                               # Update the value

    # Write back to the file
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


def start_trial():
    """
    Docstring for start_trial | Starts trial
    """

    pyautogui.moveTo(1829, 1341, 1)
    pyautogui.dragTo(988, 1330, 0.5)
    time.sleep(1)
    replay()


def run():
    """
    Docstring for run
    """

    can_run = True

    while can_run:
        time.sleep(5)
        returned_value = clockChestHunt()
        if returned_value is not None:
            logger.info("Triggered chest hunt")
            update_movement(False)                            #stop movement
            time.sleep(2)                                     #give time for saver to be found

            for i in range(30):
                chest_hunt_check_alive = findCloseButton()
                if chest_hunt_check_alive is not None:        #checks for slayer after each opened chest
                    close_chest_hunt()
                    logger.info("Triggered chest hunt close")
                    update_movement(True)
                    
                if i == 1:
                    coords = findSaverChest()
                    x, y = coords[0], coords[1]
                    click_pos(x, y)

                x, y = chestPositions[i]
                click_pos(x, y)

        trial_check_alive = clockTrial()
        if trial_check_alive is not None:
            update_movement(False)
            print("found trial")
            start_trial()
        elif trial_check_alive is None:
            update_movement(True)

        chest_hunt_check_alive = findCloseButton()
        if chest_hunt_check_alive is not None:
            close_chest_hunt()
            print("closing chesthunts")
            update_movement(True)
        trialReturnedValueFix = trialclose()

        if trialReturnedValueFix is not None:
            x, y = trialReturnedValueFix
            click_pos(x, y)
        #elif returnedValue == None:
            #print("Failed chesthunt check")

            
                                          
    
time.sleep(1)
threading.Thread(target=movementRun).start()
run()