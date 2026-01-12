import pyautogui
import time
import keyboard

keystrokes = []

while True:
    time.sleep(1)
    keystrokes.append(pyautogui.position())
    print(len(keystrokes))
    print(keystrokes)



#drag coords
#Point(x=1047, y=1483), Point(x=1887, y=1485)]