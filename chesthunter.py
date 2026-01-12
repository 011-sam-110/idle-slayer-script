import keyboard
import pyautogui 
import time
import random
from src.saverChest import findSaverChest
from src.clockChestHunt import clockChestHunt
from src.gameOver import findCloseButton                     
from src.movement import movementRun
from src.clockTrial import clockTrial
from src.replayscript import replay
from src.trialtempfix import trialclose
import threading

pyautogui.FAILSAFE = False                    

def clickChest(x,y):
    pyautogui.moveTo(x,y,0.6)
    time.sleep(1)
    pyautogui.click()
    time.sleep(2)

def closeChestHunt():
    pyautogui.moveTo(1410, 1623, 0.6)
    pyautogui.click()

    
def updateMovement(value):
    import json

    # Load the JSON file
    with open("config.json", "r") as f:
        config = json.load(f)
                
    # Update the value
    config["movement"] = value

    # Write back to the file
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

chestPositions = [(392, 650), (571, 653), (791, 666), (1086, 691), (1277, 683), (1552, 699), (1789, 692), (2053, 703), (2239, 712), (2486, 722), (2460, 913), (2244, 905), (2035, 922), (1792, 903), (1550, 884), (1297, 909), (1012, 917), (811, 900), (589, 926), (424, 922), (374, 1167), (549, 1143), (846, 1119), (1024, 1129), (1286, 1144), (1498, 1164), (1739, 1156), (1989, 1122), (2236, 1160), (2463, 1152)]


def startTrial():
    pyautogui.moveTo(1829,1341, 1)
    pyautogui.dragTo(988,1330, 0.5)
    time.sleep(1)
    replay()

def ChestHunt():
    threading.Thread(target=movementRun).start()
    loop = True 
    while loop:
        time.sleep(5)                       
        returnedValue = clockChestHunt()
        if returnedValue != None:             
            count = 0
            print("found chest hunt")
            updateMovement(False) #stop movement
            time.sleep(2) #give time for saver to be found

            for i in range(30):
                checkAlive = findCloseButton()
                if checkAlive != None:
                    closeChestHunt()
                    updateMovement(True)
                    

                if i == 1:
                    coords = findSaverChest()
                    x,y = coords[0], coords[1]
                    clickChest(x,y)

                x,y = chestPositions[i]
                clickChest(x,y)
        trialReturnedValue = clockTrial()
        if trialReturnedValue != None:
            updateMovement(False)
            print("found trial")
            startTrial()
        elif trialReturnedValue == None:
            updateMovement(True)
        checkAlive = findCloseButton()
        if checkAlive != None:
            closeChestHunt()
            print("closing chesthunts")
            updateMovement(True)
        trialReturnedValueFix = trialclose()
        if trialReturnedValueFix != None:
            x,y = trialReturnedValueFix
            clickChest(x,y)
        #elif returnedValue == None:
            #print("Failed chesthunt check")

            
                                           
    
time.sleep(1)
ChestHunt()