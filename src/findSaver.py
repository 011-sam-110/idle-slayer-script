import cv2 as cv
import pyautogui

def getSaverCoordinates():

    #Config
    WMIN = 190
    WMAX = 200
    HMIN = 190
    HMAX = 200
    SCALE = 0.5
    DEV = True

    screenshot = pyautogui.screenshot()
    screenshot.save("SaverChest.png")
    img = cv.imread("SaverChest.png", cv.IMREAD_GRAYSCALE)

    # Apply blur
    img = cv.medianBlur(img,5)

    # Thresholding
    th2 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C,\
                cv.THRESH_BINARY, 11, 2)
    ret, thresh = cv.threshold(th2, 127, 255, 0)

    # Find all Contours
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    th2 = cv.cvtColor(th2, cv.COLOR_GRAY2BGR)

    # Filter contours down to match desired size
    filtered = []
    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        cv.rectangle(th2, (x, y), (x + w, y + h), (0, 0,255), 2)
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

   
    #th2 = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    # Show image

    if len(finalcoords) == 1:
        return 1, finalcoords
    else:
        return 0, None
