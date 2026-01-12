import cv2
import numpy as np
import pyautogui

# Take a screenshot
screenshot = pyautogui.screenshot()
screenshot.save("screenshot2.png")
screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)


template = cv2.imread("imgs\\Chest.png")
w, h = template.shape[1], template.shape[0]


result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
locations = np.where(result >= threshold)


coords = list(zip(*locations[::-1]))  
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
print(max_val)
print(min_val)
print("Found objects at:", coords)


"""
min max values
0.382834255695343
-0.34862422943115234


"""