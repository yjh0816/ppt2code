# import numpy as np
# from PIL import Image
# import matplotlib.pyplot as plt

# path = './naver.png'

# image_pil = Image.open(path)
# image = np.array(image_pil)
# image.shape

# #이미지 range 확인
# np.min(image), np.max(image)


# plt.imshow(image)
# plt.show()

# import cv2
# import numpy as np

# img = cv2.imread('./naver.png')
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(gray,50,150,apertureSize = 3)

# lines = cv2.HoughLines(edges,1,np.pi/180,150)
# for line in lines:
#     rho,theta = line[0]
#     a = np.cos(theta)
#     b = np.sin(theta)
#     x0 = a*rho
#     y0 = b*rho
#     x1 = int(x0 + 1000*(-b))
#     y1 = int(y0 + 1000*(a))
#     x2 = int(x0 - 1000*(-b))
#     y2 = int(y0 - 1000*(a))

#     cv2.line(img,(x1,y1),(x2,y2),(0,0,255),1)

# cv2.imshow('edges', edges)
# cv2.imshow('result', img)
# cv2.waitKey()
# cv2.destroyAllWindows()

import cv2
import numpy as np
import matplotlib.pyplot as plt

#img = cv2.imread('./naver.png')
img = cv2.imread('./naver_login.png')
#img = cv2.imread('./6-1 로그인.png')
# img = cv2.imread('./7-1 기본 설정.png')
#img = cv2.imread('./9-1 상품연결.png')
#img = cv2.imread('./10-1 컨텐츠 관리 (프리미엄).png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
minLineLength = 50
maxLineGap = 10

lines = cv2.HoughLinesP(edges,1,np.pi/2,11,minLineLength,maxLineGap)

for line in lines:
    x1,y1,x2,y2 = line[0]
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),1)
    print(x1,y1,x2,y2)

cv2.imshow('edges', edges)
cv2.imshow('result', img)
plt.imsave('opcv.png', edges)

cv2.waitKey()
cv2.destroyAllWindows()

# import numpy as np
# import cv2
# import matplotlib.pyplot as plt
# from PIL import Image
# def canny():
#     #img = cv2.imread('./naver.png', cv2.IMREAD_GRAYSCALE)
#     img = cv2.imread('./naver2.png')
#     #img = cv2.imread('./6-1 로그인.png')
#     #img = cv2.imread('./7-1 기본 설정.png')
#     #img = cv2.imread('./9-1 상품연결.png')
#     #img = cv2.imread('./10-1 컨텐츠 관리 (프리미엄).png')
#     # plt.imshow(img)
#     # plt.xticks([]) # x축 눈금
#     # plt.yticks([]) # y축 눈금
#     # plt.show()
#     #cv2.imshow('0', img)

#     edge1 = img
#     #edge1 = img[1:958,1:1366]
#     #edge1 = 255-cv2.Canny(img, 50, 200)

#     image_size = edge1.shape
#     image_size2 = list(image_size)
#     print(image_size2)
#     print(edge1[0][0])
#     print(edge1[image_size2[0]-1][image_size2[1]-1])
     
#     a = 0
#     cont_check = 0 #default = 0이며 빨간선그으면 1, 그다음줄부턴 0 ,마지막은1
#     print(image_size2[0]-1)
#     print(image_size2[1]-1)
#     print(image_size2[1])

#     # print(edge1.item(image_size2[0]-1,image_size2[1]-1,0))
#     # print(edge1.item(image_size2[0]-1,image_size2[1]-1,1))
#     # print(edge1.item(image_size2[0]-1,image_size2[1]-1,2))

#     for y in range(0,image_size2[0]):
#         a = 0
#         for x in range(0,image_size2[1]):
#             #if(edge1[y][x] != [255,255,255]):
#             if(((edge1.item(y,x,0)) != (edge1.item(y,0,0)))&((edge1.item(y,x,1)) != (edge1.item(y,0,1)))&((edge1.item(y,x,2)) != (edge1.item(y,0,2)))):    
#                 if(cont_check == 1):
#                     for x in range(0, image_size2[1]):
#                         edge1[y-1][x] = [255,0,0]
#                 cont_check = 0
#                 break
#             else:
#                 if(x == image_size2[1]-1):
#                     a = 1
#         if(a == 1):
#             if(cont_check == 0):
#                 for x in range(0, image_size2[1]):
#                     edge1[y][x] = [0,0,255]
#                 cont_check = 1

#     # a = 0
#     # for x in range(0,image_size2[1]):
#     #     a = 0
#     #     for y in range(0,image_size2[0]):
#     #         #if(edge1[y][x] != [255,255,255]):
#     #         if(((edge1.item(y,x,0)) != (edge1.item(0,x,0)))&((edge1.item(y,x,1)) != (edge1.item(0,x,1)))&((edge1.item(y,x,2)) != (edge1.item(0,x,2)))):    
#     #             break
#     #         else:
#     #             if(y == image_size2[0]-1):
#     #                 a = 1
#     #     if(a == 1):
#     #         for y in range(0, image_size2[0]):
#     #             edge1[y][x] = [0,0,255]
#     #cv2.imshow('2', edge1)
#     plt.imshow(edge1)
#     plt.xticks([]) # x축 눈금
#     plt.yticks([]) # y축 눈금
#     plt.show()
#     #cv2.waitKey(0)
#     #cv2.destroyAllWindows

# canny()