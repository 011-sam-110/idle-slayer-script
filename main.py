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
from src.clockTrial import clockTrial
from src.saverChest import findSaverChest
from src.gameOver import findCloseButton
from src.clockChestHunt import clockChestHunt
from src.chestIdentification import getChestCoordinates

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
pyautogui.FAILSAFE = False

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

#   Load the JSON file
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

#   Update the value
    config["movement"] = value                               

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
            logger.info(" Triggered chest hunt") 
            chestPositions = getChestCoordinates()
            print(chestPositions)
#           stop movement
            update_movement(False) 
            for i in range(30):
                chest_hunt_check_alive = findCloseButton()
#               chest hunt check #1 | runs after each chest is opened
                if chest_hunt_check_alive is not None:
                    close_chest_hunt()
                    logger.info(" Triggered chest hunt close")
                    update_movement(True)
                if i == 1:
                    coords = findSaverChest()
                    x, y = coords[0], coords[1]
                    click_pos(x, y)

                x, y = chestPositions[i]
                click_pos(x, y)


#       trial check #3
        trial_check_alive = clockTrial()
        if trial_check_alive is not None:
            update_movement(False)
            logger.info(" Triggered trial")
            start_trial()
        elif trial_check_alive is None:
            update_movement(True)

#       chest hunt check #2
        chest_hunt_check_alive = findCloseButton()
        if chest_hunt_check_alive is not None:
            close_chest_hunt()
            logger.info("Triggered chest hunt close")
            update_movement(True)


time.sleep(1)
threading.Thread(target=movementRun).start()
run()
