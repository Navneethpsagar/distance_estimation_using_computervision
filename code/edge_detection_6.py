import cv2
from matplotlib import pyplot as plt
# Read input
color = cv2.imread('test2.jpg', cv2.IMREAD_COLOR)
# color = cv2.resize(color, (0, 0), fx=0.15, fy=0.15)
# RGB to gray
gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
cv2.imwrite('test_gray.png', gray)
# cv2.imwrite('output/thresh.png', thresh)
# Edge detection
edges = cv2.Canny(gray, 100, 200, apertureSize=3)
# Save the edge detected image
cv2.imwrite('test_edge.png', edges)
cv2.imshow('Color', color)
cv2.imshow('Gray', gray)
cv2.imshow('Edges', edges)
cv2.waitKey(0)