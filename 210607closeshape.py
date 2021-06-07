# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from PIL import Image
#import cv2

img = ('./naver_login.png')
im = Image.open(img)
print(im.size)
h, w = im.size

pix = np.array(im)
print(im.size)
X_filter = np.zeros([w,h])
Y_filter = np.zeros([w,h])
D_filter = np.zeros([w,h])

#하단과 픽셀값의 변화
for y in range(0, h):
    for x in range(0, w-1):
        if (pix[x][y][0] == pix[x+1][y][0]and
            pix[x][y][1] == pix[x+1][y][1]and
            pix[x][y][2] == pix[x+1][y][2]):
            Y_filter[x][y] = 0
        else:
            if(Y_filter[x][y-1] == 0 ):
                Y_filter[x][y] = 10
            else:
                Y_filter[x][y] = 1
    Y_filter[w-1][y] = 1        
        
#우측과 픽셀값의 변화 
for x in range(0, w):
    for y in range(0, h-1):
        if (pix[x][y][0] == pix[x][y+1][0]and
            pix[x][y][1] == pix[x][y+1][1]and
            pix[x][y][2] == pix[x][y+1][2]):
            X_filter[x][y] = 0
        else:
# =============================================================================
#             if(X_filter[x-1][y] == 0):
#                 X_filter[x][y] = 2
#             else:
# =============================================================================
            X_filter[x][y] = 1
    X_filter[x][h-1] = 1   

 
        
D_filter = X_filter + 2*Y_filter
print(D_filter)
# =============================================================================
# np.savetxt("X_filter.txt",X_filter,fmt='%d')
# np.savetxt("Y_filter.txt",Y_filter,fmt='%d')
np.savetxt("D_filter.txt",D_filter,fmt='%d')
# =============================================================================

rect = []
rectx = []
recty = []
for x in range(0, w):
    for y in range(0, h):
        if(D_filter[x][y] == 20):       
            if y in rect:
                rectx.append(x)
                recty.append(y)
            rect.append(y)
                
print(rectx,recty)
        












