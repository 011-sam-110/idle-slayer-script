import cv2 as cv
import numpy as np

#Config
WMIN = 169
WMAX = 185
HMIN = 90
HMAX = 170
SCALE = 0.5


# Take in screenshot
img = cv.imread('Screenshot2.png', cv.IMREAD_GRAYSCALE)

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

def move(x,y):
    import pyautogui
    pyautogui.moveTo(x,y,.5)


# Find center coord
for c in filtered:

    x,y,w,h = cv.boundingRect(c)
    cv.rectangle(th2, (x, y), (x + w, y + h), (0, 255,0), 2)
    move(x,y)



# Draw Countours
for i in range(len(filtered)):
    cnt = filtered[i]
    cv.drawContours(th2, [cnt], -1, (0,0,255), 3)

# Scaling
h, w = img.shape[:2]
SCALE = 0.5
img = cv.resize(img, (int(w*SCALE), int(h*SCALE)), interpolation=cv.INTER_AREA)

# Show image
cv.imshow('image', th2)
cv.waitKey(0)


filtered = np.array(filtered)
filtered = filtered.reshape(-1, 2)


