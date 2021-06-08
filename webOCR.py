"""Detects text in the file."""
#비전 API 설정법
#https://cloud.google.com/vision/docs/setup?hl=ko#windows

#json파일명
#ppt2codeocr-b106561ef2c5.json
#deductive-motif-316110-2d8de37aca8c.json"
from google.cloud import vision
import cv2
import io, json
from google.cloud import vision_v1
from google.cloud.vision_v1 import AnnotateImageResponse
#구글 ocr기본
import proto

def ocr():
    
    client = vision.ImageAnnotatorClient()
    # path = './6-1 로그인.png'
    path = './naver_login.png'

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    price_candidate = []
    card_number_candidate = []
    date_candidate = []

    response = client.text_detection(image=image)
    # serialize / deserialize proto (binary)
    serialized_proto_plus = AnnotateImageResponse.serialize(response)
    response = AnnotateImageResponse.deserialize(serialized_proto_plus)
    print(response.full_text_annotation.text)
    # print(response.full_text_annotation.text)

    # serialize / deserialize json
    response_json = AnnotateImageResponse.to_json(response)
    response = json.loads(response_json)
    print(response['fullTextAnnotation']['text'])

    with open("student_file.json", "w") as json_file:
        json.dump(response, json_file)


    # print(type(response))

    f = open("new.txt", 'w')
    f2 = open("xy.txt", 'w')
    # for i in range(0,count):
        # f2.write(string)
        # f2.write(texts[i])
        # print(i)
        # print(texts[i])
    f2.write(response)
    f2.close()
    # print('Texts:')
    
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
