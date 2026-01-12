import cv2
import numpy as np
import pyautogui
import time
time.sleep(1)
x, y = pyautogui.position()
img = pyautogui.screenshot()
img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

print("BGR at mouse:", img[y, x])

#GETS BGR POS126