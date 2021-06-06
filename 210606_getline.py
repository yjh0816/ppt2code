# -*- coding: utf-8 -*-
"""
Created on Tue May 11 17:06:14 2021

@author: BaeChangHo
"""

import numpy as np
import cv2
import math
# =============================================================================
# src = cv2.imread("naver14.png")
# dst = src.copy()
# gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
# canny = cv2.Canny(gray, 5000, 1500, apertureSize = 5, L2gradient = True)
# lines = cv2.HoughLines(canny, 0.8, np.pi / 2, 100, srn = 100, stn = 200, min_theta = 0, max_theta = np.pi)
# 
# for i in lines:
#     rho, theta = i[0][0], i[0][1]
#     a, b = np.cos(theta), np.sin(theta)
#     x0, y0 = a*rho, b*rho
# 
#     scale = src.shape[0] + src.shape[1]
# 
#     x1 = int(x0 + scale * -b)
#     y1 = int(y0 + scale * a)
#     x2 = int(x0 - scale * -b)
#     y2 = int(y0 - scale * a)
# 
#     cv2.line(dst, (x1, y1), (x2, y2), (0, 0, 255), 1)
#     #cv2.line(dst, (x1, y1), (x2, y2), (255, 255, 0), 1)
#     #cv2.circle(dst, (x0, y0), 3, (255, 0, 0), 5, cv2.FILLED)
# #cv2.imwrite('naver13.png', dst)
# cv2.imshow("dst", dst)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# 
# =============================================================================



# =============================================================================
# img_color = cv2.imread('alla.png', cv2.IMREAD_COLOR)
# img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
# 
# img_sobel_x = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
# img_sobel_x = cv2.convertScaleAbs(img_sobel_x)
# 
# img_sobel_y = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)
# img_sobel_y = cv2.convertScaleAbs(img_sobel_y)
# 
# 
# img_sobel = cv2.addWeighted(img_sobel_x, 1, img_sobel_y, 1, 0);
# 
# 
# #cv2.imshow("Sobel X", img_sobel_x)
# #cv2.imshow("Sobel Y", img_sobel_y)
# cv2.imshow("Sobel", img_sobel)
# #cv2.imshow('CHAIN_APPROX_SIMPLE', img_sobel)
# cv2.imwrite('alloa.png',img_sobel)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# =============================================================================


# =============================================================================
# img = cv2.imread("alloa3.png")
# 
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 
# #lines = cv2.HoughLines(gray, 1, np.pi/2, 70)
# 
# 
# 
# lines = cv2.HoughLinesP(gray, 0.8, np.pi / 2, 10, minLineLength = 10, maxLineGap = 100)
# 
# 
# # =============================================================================
# # for line in lines[0]:
# #     pt1 = (line[0],line[1])
# #     pt2 = (line[2],line[3])
# #     cv2.line(img, pt1, pt2, (0,0,255), 3)
# # =============================================================================
# 
# # =============================================================================
# # for i in range(len(lines)):
# #     for rho, theta in lines[i]:
# #         a = np.cos(theta)
# #         b = np.sin(theta)
# #         x0 = a*rho
# #         y0 = b*rho
# #         x1 = int(x0 + 1000*(-b))
# #         y1 = int(y0+1000*(a))
# #         x2 = int(x0 - 1000*(-b))
# #         y2 = int(y0 -1000*(a))
# # 
# #         cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
# # 
# # =============================================================================
# 
# for i in lines:
#     cv2.line(img, (i[0][0], i[0][1]), (i[0][2], i[0][3]), (0, 0, 255), 2)
# 
# cv2.imshow("alloa2.png", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# =============================================================================


# Load image, grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread('alloa3.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Detect horizontal lines
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50,1))
horizontal_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)

# Detect vertical lines
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,50))
vertical_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=1)

# Combine masks and remove lines
table_mask = cv2.bitwise_or(horizontal_mask, vertical_mask)
image[np.where(table_mask==255)] = [255,255,255]

#cv2.imshow('thresh', thresh)
#cv2.imshow('horizontal_mask', horizontal_mask)
#cv2.imshow('vertical_mask', vertical_mask)
cv2.imshow('table_mask', table_mask)
#cv2.imshow('image', image)
cv2.waitKey()





