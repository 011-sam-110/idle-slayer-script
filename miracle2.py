import cv2 as cv
import numpy as np

img = cv.imread('Screenshot2.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# simple binarize to separate sprites from background (tweak 200 if needed)
_, th = cv.threshold(gray, 200, 255, cv.THRESH_BINARY_INV)

# find contours and filter by size/aspect ratio to get chest candidates
contours, _ = cv.findContours(th, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
for c in contours:
    x,y,w,h = cv.boundingRect(c)
    if 20 < w < 120 and 20 < h < 120 and 0.7 < w/h < 1.6:   # tune these
        cv.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)


cv.imshow('image', img)
cv.waitKey(0)