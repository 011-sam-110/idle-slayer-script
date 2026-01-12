

import cv2 as cv
import numpy as np
 
img = cv.imread('Screenshot2.png')
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray,50,150,apertureSize = 3)
lines = cv.HoughLinesP(edges,1,np.pi/180,100,minLineLength=100,maxLineGap=10)
for line in lines:
    x1,y1,x2,y2 = line[0]
    cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)

h, w = img.shape[:2]


scale = 0.5
img= cv.resize(img, (int(w*scale), int(h*scale)), interpolation=cv.INTER_AREA)

cv.imshow('image', img)
cv.waitKey(0)