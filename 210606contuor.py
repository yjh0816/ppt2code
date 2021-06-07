# import cv2
# import numpy as np

# # img = cv2.imread('./6-1 로그인.png')
# # img = cv2.imread('./7-1 기본 설정.png')
# # img = cv2.imread('./naver_login.png')
# img = cv2.imread('./naver_login_sobel.png')


# img2 = img

# # 그레이 스케일로 변환 ---①
# imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # imgray = img
# # imgray.convertTo(img,cv2.CV_32SC1)
# # 스레시홀드로 바이너리 이미지로 만들어서 검은배경에 흰색전경으로 반전 ---②
# ret, imthres = cv2.threshold(imgray, 207, 255, cv2.THRESH_BINARY_INV)

# # 가장 바깥쪽 컨투어에 대해 모든 좌표 반환 ---③
# contour, hierarchy = cv2.findContours(imthres, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# # 가장 바깥쪽 컨투어에 대해 꼭지점 좌표만 반환 ---④
# contour2, hierarchy = cv2.findContours(imthres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# # 각각의 컨투의 갯수 출력 ---⑤
# print('도형의 갯수: %d(%d)'% (len(contour), len(contour2)))

# # 모든 좌표를 갖는 컨투어 그리기, 초록색  ---⑥
# cv2.drawContours(img, contour, -1, (0,255,0), 4)
# # 꼭지점 좌표만을 갖는 컨투어 그리기, 초록색  ---⑦
# cv2.drawContours(img2, contour2, -1, (0,255,0), 4)

# # 컨투어 모든 좌표를 작은 파랑색 점(원)으로 표시 ---⑧
# for i in contour:
#     for j in i:
#         cv2.circle(img, tuple(j[0]), 1, (255,0,0), -1) 

# # 컨투어 꼭지점 좌표를 작은 파랑색 점(원)으로 표시 ---⑨
# for i in contour2:
#     for j in i:
#         cv2.circle(img2, tuple(j[0]), 1, (255,0,0), -1) 

# # 결과 출력 ---⑩
# cv2.imshow('imgray', imgray)
# cv2.imshow('imthres', imthres)
# cv2.imshow('CHAIN_APPROX_NONE', img)
# cv2.imshow('CHAIN_APPROX_SIMPLE', img2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 컨투어 계층 트리 (cntr_hierachy.py)

import cv2
import numpy as np

# 영상 읽기
img = cv2.imread('./naver_login.png')
img2 = img.copy()
# 바이너리 이미지로 변환
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, imthres = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV)

# 가장 바깥 컨투어만 수집   --- ①
contour, hierarchy = cv2.findContours(imthres, cv2.RETR_EXTERNAL, \
                                                cv2.CHAIN_APPROX_NONE)
# 컨투어 갯수와 계층 트리 출력 --- ②
print(len(contour), hierarchy)

# 모든 컨투어를 트리 계층 으로 수집 ---③
contour2, hierarchy = cv2.findContours(imthres, cv2.RETR_TREE, \
                                            cv2.CHAIN_APPROX_SIMPLE)
# 컨투어 갯수와 계층 트리 출력 ---④
print(len(contour2), hierarchy)

# 가장 바깥 컨투어만 그리기 ---⑤
cv2.drawContours(img, contour, -1, (0,255,0), 3)
# 모든 컨투어 그리기 ---⑥
for idx, cont in enumerate(contour2): 
    # 랜덤한 컬러 추출 ---⑦
    color = [int(i) for i in np.random.randint(0,255, 3)]
    # 컨투어 인덱스 마다 랜덤한 색상으로 그리기 ---⑧
    cv2.drawContours(img2, contour2, idx, color, 3)
    # 컨투어 첫 좌표에 인덱스 숫자 표시 ---⑨
    cv2.putText(img2, str(idx), tuple(cont[0][0]), cv2.FONT_HERSHEY_PLAIN, \
                                                            1, (0,0,255))

# 화면 출력
cv2.imshow('RETR_EXTERNAL', img)
cv2.imshow('RETR_TREE', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()