import cv2
import pytesseract

img = cv2.imread("SaverChest.png")
text = pytesseract.image_to_string(img)
print(text)