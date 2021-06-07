# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import json
#import cv2

img = ('naver_login.png')
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
# =============================================================================
#             if(Y_filter[x][y-1] == 0 ):
#                 Y_filter[x][y] = 10
#             else:
# =============================================================================
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
# np.savetxt("D_filter.txt",D_filter,fmt='%d')
# =============================================================================


for x in range(0, w):
    for y in range(0, h):
        if(D_filter[x][y] != 0):
            D_filter[x][y] = 1

text = []
with open('./student_file.json', 'r') as f:
    json_data = json.load(f)

count = 0

for i in json_data["textAnnotations"]:
    text.append(i['boundingPoly']['vertices'])
    # for j in range(0,4):
    #     print(text[count][j]['y'],text[count][j]['x'])
        # D_filter[text[count][j]['y']][text[count][j]['x']] = 0
        # for x in range(0, text[count][j]['y']):
        #     for y in range(0, text[count][j]['x']):
        #         D_filter[x][y] = 4
    count = count + 1
    # print()
# for x in range(text[3][0]['y'], text[3][2]['y']):
#         for y in range(text[3][0]['x'], text[3][2]['x']):
#             D_filter[x][y] = 4
for index in range(1,count):
    print(text[index][0]['x'],text[index][0]['y'],text[index][2]['x'],text[index][2]['y'])
    for x in range(text[index][0]['y'], text[index][2]['y']):
        for y in range(text[index][0]['x'], text[index][2]['x']):
            D_filter[x][y] = 0

np.savetxt("D_filter.txt",D_filter,fmt='%d')    


plt.imsave('filename.png', D_filter)
# =============================================================================
# #사각형의 꼭짓점만으로 진위판단
# rect = []
# rectx = []
# recty = []
# rect2 = []
# 
# 
# 
# for x in range(0, w):
#     for y in range(0, h):
#         if(D_filter[x][y] == 20):         
#             if y in rect:
#                 rectx.append(x)
#                 recty.append(y)
#                 
#             rect.append(y)
#         if(D_filter[x][y] == 3):
#             if x in rectx:
#                 rect2.append((x,y))
# print('rectx',rectx)
# print('recty',recty)
# print('rect2',rect2)
# =============================================================================
        












