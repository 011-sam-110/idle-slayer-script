import cv2 as cv
import pyautogui
from . import findSaver
import time
import json 

def getConfigSettings(settings : list):   
    """Get specific settings from the configuration file."""
    returnedSettings = []
    with open("src/config.json") as file:
        config = json.load(file)
        for setting in settings:
            returnedSettings.append(config[setting])

    return returnedSettings

def getChestCoordinates():
    """Detect chest hunt chests on the screen and return their coordinates."""
    #Config
    WMIN = 175
    WMAX = 185
    HMIN = 125
    HMAX = 135
    SCALE = 0.5
    DEV = True

    screenshot = pyautogui.screenshot()
    screenshot.save("screen.png")
    img = cv.imread("screen.png", cv.IMREAD_GRAYSCALE)

    # Apply blur
    img = cv.medianBlur(img,5)

    # Thresholding
    th2 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C,\
                cv.THRESH_BINARY, 11, 2)
    ret, thresh = cv.threshold(th2, 127, 255, 0)

    # Find all Contours
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Convert to BGR
    th2 = cv.cvtColor(th2, cv.COLOR_GRAY2BGR)

    # Filter contours down to 29
    filtered = []
    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
    #     Width                 Height
        if WMIN <= w <= WMAX and HMIN <= h <= HMAX:
            filtered.append(cnt)
    

    # Find center coord
    finalcoords = []
    for c in filtered:

        x,y,w,h = cv.boundingRect(c)
        cv.rectangle(th2, (x, y), (x + w, y + h), (0, 255,0), 2)
        finalcoords.append([x, y])

    # Draw Countours
    for i in range(len(filtered)):
        cnt = filtered[i]
        cv.drawContours(th2, [cnt], -1, (0,0,255), 3)

    # Scaling
    h, w = img.shape[:2]
    img = cv.resize(img, (int(w*SCALE), int(h*SCALE)), interpolation=cv.INTER_AREA)
    th2 = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

    if len(finalcoords) == 29:
        return 1, finalcoords
    else:
        return 0, None
    
def Click(x, y):
    """Click at the specified coordinates with a delay."""
    pyautogui.click(x, y)
    time.sleep(getConfigSettings(["chest_hunt_click_delay"])[0])

def OpenChests(all_chest_coords, saver_chest_coords):
    """Open all chests in the chest hunt, prioritizing the saver chest."""
    for i in range(29):
        x, y = all_chest_coords[i]
        Click(x, y)
        if i == 1:
            x, y = saver_chest_coords[0]
            Click(x, y)

def ChestHuntCheck():
    """Check for chest hunts and open chests if found."""
    while True:
        time.sleep(15)
        paused = getConfigSettings(["paused"])[0]

        while paused == False:
            time.sleep(15)
            paused = getConfigSettings(["paused"])[0]

            status, all_chest_coords = getChestCoordinates()
            if status == 1:
                print("chest hunt found")
                status, saver_chest_coords = findSaver.getSaverCoordinates()
                if status == 1:
                    print("saver chest found, opening chests")
                    OpenChests(all_chest_coords, saver_chest_coords)
                else:
                    print("saver chest not found")
            else:
                print("chest hunt not found")
