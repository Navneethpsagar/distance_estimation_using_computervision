import numpy as np
import cv2 as cv
from resize_image_3 import *

filename = '../images/test2.jpg'
img = cv.imread(filename)
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
edge = cv.Canny(gray, 100, 200)
edge = np.float32(edge)
dst = cv.cornerHarris(edge,2,3,0.04)
#result is dilated for marking the corners, not important
dst = cv.dilate(edge,None)
# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]
cv.imshow('dst',rescaleFrame(img,0.2))
if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()