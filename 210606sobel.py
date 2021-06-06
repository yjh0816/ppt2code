# =============================================================================
import cv2

img_color = cv2.imread('naver_login.png', cv2.IMREAD_COLOR)
img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

img_sobel_x = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
img_sobel_x = cv2.convertScaleAbs(img_sobel_x)

img_sobel_y = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)
img_sobel_y = cv2.convertScaleAbs(img_sobel_y)


img_sobel = cv2.addWeighted(img_sobel_x, 1, img_sobel_y, 1, 0);


#cv2.imshow("Sobel X", img_sobel_x)
#cv2.imshow("Sobel Y", img_sobel_y)
cv2.imshow("Sobel", img_sobel)
#cv2.imshow('CHAIN_APPROX_SIMPLE', img_sobel)
cv2.imwrite('naver_login_sobel.png',img_sobel)
# =============================================================================

image = cv2.imread('./naver_login.png')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,3))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, close_kernel, iterations=1)

dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,3))
dilate = cv2.dilate(close, dilate_kernel, iterations=1)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    #if area > 200 and area < 26391:
    if area > 300 and area < 30000:

        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(img_sobel, (x, y), (x + w, y + h), (0,0,0), -1)
        cv2.line(img_sobel,(x,y),(x+w, y),(0,0,0))
        cv2.line(img_sobel,(x,y),(x, y+h),(0,0,0))
        cv2.line(img_sobel,(x+w,y),(x+w, y+h),(0,0,0))
        cv2.line(img_sobel,(x,y+h),(x+w, y+h),(0,0,0))
        cv2.rectangle(image, (x, y), (x + w, y + h), (0,0,0), -1)
        cv2.line(image,(x,y),(x+w, y),(0,0,0))
        cv2.line(image,(x,y),(x, y+h),(0,0,0))
        cv2.line(image,(x+w,y),(x+w, y+h),(0,0,0))
        cv2.line(image,(x,y+h),(x+w, y+h),(0,0,0))

#image = cv2.resize(image, dsize=(0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
cv2.imshow('img_sobel', img_sobel)
cv2.imshow('image', image)
# cv2.imwrite('naver_login_OCR.png', image)
# =============================================================================
cv2.waitKey(0)
cv2.destroyAllWindows()
# =============================================================================