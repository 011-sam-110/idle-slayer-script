import numpy as np
import pyautogui
import cv2

def findCloseButton():
    
    img = pyautogui.screenshot()
    img.save("screen.png")
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    lower = np.array([0,0,175])
    upper = np.array([0,0,175])

    mask = cv2.inRange(img, lower, upper)

    ys, xs = np.where(mask > 0)

    if len(xs) > 0:
        return int(xs[0]), int(ys[0])
    return None

if __name__ == "__main__":
    coords = findCloseButton()
    if coords:
        print(f"Found bonus chest at: {coords}")
    else:
        print("Bonus chest not found.")