"""Detects text in the file."""
#비전 API 설정법
#https://cloud.google.com/vision/docs/setup?hl=ko#windows

#json파일명
#ppt2codeocr-b106561ef2c5.json
from google.cloud import vision
import io
import cv2
import json
#구글 ocr기본

def ocr():
    
    client = vision.ImageAnnotatorClient()
    path = './6-1 로그인.png'
    # path = './naver_login_sobel.png'

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    price_candidate = []
    card_number_candidate = []
    date_candidate = []

    response = client.text_detection(image=image)
    texts = response.text_annotations
    count = len(texts)
    #print(str(count))
    for i in range(0,count):
        #print(i)
        print(texts[i]['EntityAnnotation'])
        #print(type(texts[i]))
    #print(type(texts))

    f = open("new.txt", 'w')
    print('Texts:')
    
    for text in texts:
        content = text.description
        content = content.replace(',','')
        f.write('"{}"'.format(content))
    f.close()
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

#구글 ocr에다가 opencv적용중
def ocr2():
    
    client = vision.ImageAnnotatorClient()
    path = './naver.png'

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    price_candidate = []
    card_number_candidate = []
    date_candidate = []

    response = client.text_detection(image=image)
    texts = response.text_annotations
    f = open("new.txt", 'w')
    #f.write(str(texts))
    print(type(texts))

    for text in texts:
        content = text.description
        content = content.replace(',','')
        f.write('"{}"'.format(content))
    f.close()
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

ocr()
