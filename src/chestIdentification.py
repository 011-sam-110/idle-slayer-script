import cv2 as cv
import pyautogui
import numpy as np

#    WMIN = 168
#    WMAX = 183
#    HMIN = 90
#    HMAX = 170
#    SCALE = 0.5
#    DEV = True

def getChestCoordinates():
    #Config
    WMIN = 168
    WMAX = 183
    HMIN = 138
    HMAX = 170
    SCALE = 0.5
    DEV = False


    # Take in screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save("Chest_screen.png")
    img = cv.imread("Chest_screen.png", cv.IMREAD_GRAYSCALE)

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

    # Show image
    if DEV:
        cv.imshow(f'{len(finalcoords)} Chests found', th2)
        cv.waitKey(0)
        print(f"Chests found: {len(finalcoords)}")


    return finalcoords