from flask import redirect
def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.

    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return f'Hello World!'
    """
    print(request.args.get('name'))
    name = request.args.get('name')
    print("--------------------------------ocr_start--------------------------------")
    ocr(name)
    print("--------------------------------바이너리 이미지 생성--------------------------------")
    img2bin()
    print("--------------------------------bin2box_start--------------------------------")
    bin2box(name)
    print("--------------------------------createHtml_start--------------------------------")
    createHtml(name)
    return redirect('https://img2code-326013.web.app/page4.html?name='+str(name))

    

#비전 API 설정법
#https://cloud.google.com/vision/docs/setup?hl=ko#windows

#json파일명
#deductive-motif-316110-2d8de37aca8c.json"
#img2code-326013-000adcb01d14.json
import google
from google.cloud import vision
import cv2
import io, json
from google.cloud import vision_v1
from google.cloud.vision_v1 import AnnotateImageResponse
from google.cloud import storage
import proto
import matplotlib.pyplot as plt
import numpy as np
import sys
import numpy
from PIL import Image, ImageOps, ImageDraw
from scipy.ndimage import morphology, label
import urllib.request
from google.cloud import automl_v1beta1

storage_client = storage.Client()
class Node:
    def __init__(self, x_position1, x_position2, y_position1, y_position2, tag, data):
        self.xdis = x_position2 - x_position1
        self.ydis = y_position2 - y_position1
        self.x1 = x_position1
        self.y1 = y_position1
        self.x2 = x_position2
        self.y2 = y_position2
        self.ax1 = x_position1
        self.ay1 = y_position1
        self.left = None
        self.right = None
        self.tag = tag
        self.data = data
        self.result = ""
        self.left_result = ""
        self.right_result = ""
              
class BinaryTree():
    #트리 생성
    def __init__(self):
        self.root = None
        self.preorder_list = []
        #self.right_have = 0
        
    def root_finder(self):
        return self.root
        
    def insert(self, node):
        self.root = self._insert_value(self.root, node)
        return self.root is not None
           
    def _insert_value(self, sub_root, node):
        if sub_root is None:
            sub_root = node
        else:
            if sub_root.x1 <= node.x1 and sub_root.x2  >= node.x2 and sub_root.y1 <= node.y1 and sub_root.y2 >= node.y2:
                node.ax1 = node.ax1 - sub_root.ax1
                node.ay1 = node.ay1 - sub_root.ay1
                sub_root.left = self._insert_value(sub_root.left, node)            
            # elif sub_root.x1 >= node.x1 and sub_root.x2  <= node.x2 and sub_root.y1 >= node.y1 and sub_root.y2 <= node.y2:
            #     node.left = self._insert_value(node.left, sub_root)
            #     #node.right = self._insert_value(sub_root.right, sub_root)
            #     sub_root = node
            elif sub_root.x1 >= node.x2 :
                #node.left = self._insert_value(sub_root.left, sub_root)
                #node.right = self._insert_value(node.right, sub_root)
                node.right = sub_root
                sub_root = node
            else:
                sub_root.right = self._insert_value(sub_root.right, node)
                        
        return sub_root

    def preorder_traverse(self):
            if self.root_finder() is not None:
                self.__preorder(self.root_finder())

    def __preorder(self, cur):
        self.preorder_list.append(cur.tag)
        #print(str(cur.tag))
        if cur.left is not None:
            #print("왼쪽 자식")
            self.__preorder(cur.left)
        #print(str(cur.tag))
        if cur.right is not None:
            #print("오른쪽 자식")
            self.__preorder(cur.right)

    #후위 순회
    def postorder(self, node):
        if node is not None:
            # 내가 최 하단 노드인 경우
            if node.right is None and node.left is None:
                if node.tag == 'otherwise':
                    return node.result
                elif node.tag == 'p':
                    node.result = "<"+str(node.tag)+" style = \"font-size: 10px; width: " + str(node.xdis) +"px; height:" + str(node.ydis)+"px; position: absolute; top: "+str(node.ay1)+"px; left: "+str(node.ax1)+"px;"+"\">" + str(node.data) +"</"+str(node.tag)+">"
                elif node.tag == 'button':
                    node.result = "<"+str(node.tag)+" style = \" width: " + str(node.xdis) +"px; height:" + str(node.ydis)+"px; position: absolute; top: "+str(node.ay1)+"px; left: "+str(node.ax1)+"px;"+"\">" + str(node.data) +"</"+str(node.tag)+">"
                else:
                    node.result = "<"+str(node.tag)+" style = \" border:1px solid black; width: " + str(node.xdis) +"px; height:" + str(node.ydis)+"px; position: absolute; top: "+str(node.ay1)+"px; left: "+str(node.ax1)+"px;"+"\">" + "</"+str(node.tag)+">"
                return node.result

            else: 
                #오른쪽 서브트리 순회
                if node.right:
                    node.right_result = self.postorder(node.right)
                    #self.right_have = 1
                
                #왼쪽 서브트리 순회
                if node.left:
                    node.left_result = self.postorder(node.left)

                if node.tag == 'p':
                    node.result =  "<"+str(node.tag)+" style = \" font-size: 10px; width: " + str(node.xdis) +"px; height:" + str(node.ydis)+"px; position: absolute; top: "+str(node.ay1)+"px; left: "+str(node.ax1)+"px;"+"\">" + str(node.data) +node.left_result +"</"+str(node.tag)+">" + node.right_result
                elif (node.tag == 'button' or node.tag == "img" or  node.tag == "input" or node.tag == "select" or node.tag == "otherwise") and not(node.left is not None and node.left.tag == "p"):
                    node.result =  "<"+ "div" +" style = \" border:1px solid black; width: " + str(node.xdis) +"px; height:" + str(node.ydis)+"px; position: absolute; top: "+str(node.ay1)+"px; left: "+str(node.ax1)+"px;"+"\">" + node.left_result +"</"+ "div" +">" + node.right_result
                else:
                    node.result =  "<"+str(node.tag)+" style = \" border:1px solid black; width: " + str(node.xdis) +"px; height:" + str(node.ydis)+"px; position: absolute; top: "+str(node.ay1)+"px; left: "+str(node.ax1)+"px;"+"\">" +node.left_result +"</"+str(node.tag)+">" + node.right_result
                
                
        return node.result
                
    def height(self, root):
        if root == None:
            return 0
        return max(self.height(root.left), self.height(root.right)) +1


texts = []
text_corner_x1 = []
text_corner_y1 = []
text_corner_x2 = []
text_corner_y2 = []

box_corner_x1 = []
box_corner_y1 = []
box_corner_x2 = []
box_corner_y2 = []
tree = BinaryTree()

D_filter = 0
# =============================================================================
#             
#             목업 이미지에 구글 OCR 사용 텍스트 검출
#             결과값 json 타입으로 변환
#             
# =============================================================================
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# from firebase_admin import storage
from datetime import datetime
import os
# Use a service account
cred = credentials.Certificate('img2code-326013-b0c3ac96a402.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def ocr(trigger):
    image_path = 'https://firebasestorage.googleapis.com/v0/b/img2code-326013.appspot.com/o/Web_images%2F'+trigger+'.png?alt=media'
    client = vision.ImageAnnotatorClient.from_service_account_json("./img2code-326013-000adcb01d14.json")

    os.makedirs(os.path.dirname('/tmp/temp.png'), exist_ok=True)
    with urllib.request.urlopen(image_path) as url:
        with open('/tmp/temp.png', 'wb') as f:
            f.write(url.read())
    if os.path.exists('/tmp/temp.png'):
        with open('/tmp/temp.png', 'rb') as f:
            content = f.read()
    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    # serialize / deserialize proto (binary)
    serialized_proto_plus = AnnotateImageResponse.serialize(response)
    response = AnnotateImageResponse.deserialize(serialized_proto_plus)
    #print(response.full_text_annotation.text)

    # serialize / deserialize json
    response_json = AnnotateImageResponse.to_json(response)
    response = json.loads(response_json)
    #print(response['fullTextAnnotation']['text'])
    
    os.makedirs(os.path.dirname('/tmp/textInImage.json'), exist_ok=True)
    with open("/tmp/textInImage.json", "w") as json_file:
        json.dump(response, json_file)


# =============================================================================
#             
#             목업 이미지를 바이너리 이미지로 변환하여 정확한 물체 검출
#             이미지 x, y 좌표의 변화량 확인
#             
# =============================================================================
def img2bin():
    im = Image.open('/tmp/temp.png')
    #print(im.size)
    h, w = im.size
    print("-------------------------------바이너리 이미지 생성--------------------------------")
    pix = np.array(im)
    D_filter = np.zeros([w,h])

    for y in range(0, h):
        for x in range(0, w):
            for i in range(3):
                if x < w-1 and pix[x][y][i] != pix[x+1][y][i]:
                        D_filter[x][y] = 1
                if y < h-1 and pix[x][y][i] != pix[x][y+1][i]:
                        D_filter[x][y] = 1
    #print(im.size)

    text = []
    with open('/tmp/textInImage.json', 'r') as f:
        json_data = json.load(f)

    count = 0
    print("--------------------------------글자좌표투명화--------------------------------")
    for i in json_data["textAnnotations"]:
        texts.append(i['description'])
        text.append(i['boundingPoly']['vertices'])
        #print("texts",i['description'])
        #print("text",i['boundingPoly']['vertices'])
        count = count + 1

    for index in range(1,count):
        #print(text[index][0]['x'],text[index][0]['y'],text[index][2]['x'],text[index][2]['y'])
        text_corner_x1.append(text[index][0]['x'])
        text_corner_y1.append(text[index][0]['y'])
        text_corner_x2.append(text[index][2]['x'])
        text_corner_y2.append(text[index][2]['y'])
        for x in range(text_corner_y1[index-1], text_corner_y2[index-1]):
            for y in range(text_corner_x1[index-1], text_corner_x2[index-1]):
                D_filter[x][y] = 0

    np.savetxt("/tmp/D_filter.txt",D_filter,fmt='%d')    

    plt.imsave('/tmp/binaryImage.png', D_filter)
    

# =============================================================================
#             
#             바이너리 이미지로부터 박스 검출
#             
# =============================================================================
def boxes(orig,trigger):
    img = ImageOps.grayscale(orig)
    im = numpy.array(img)
    #print("--------------------------------침식연산--------------------------------")
    # Inner morphological gradient.
    im = morphology.grey_dilation(im, (3, 3)) - im
    print("--------------------------------바이너리 이미지 라벨화--------------------------------")
    # Binarize.
    mean, std = im.mean(), im.std()
    t = mean + std
    im[im < t] = 0
    im[im >= t] = 1

    # Connected components.
    lbl, numcc = label(im)
    # Size threshold.
    min_size = 200 # pixels
    box = []
    cnt = 0
    dt = datetime.now()
    #np. set_printoptions(threshold=np. inf)
    #print(label(im))
    print("--------------------------------임계값 충족 검사,검출 박스 정사각형화,좌표검출--------------------------------")
    for i in range(1, numcc + 1):
        py, px = numpy.nonzero(lbl == i)
        if len(py) < min_size:
            #im[lbl == i] = 0
            continue
        #print("--------------------------------연산과자르기--------------------------------" + str(cnt))
        xmin, xmax, ymin, ymax = px.min(), px.max(), py.min(), py.max()
        if((xmin == xmax) or (ymin == ymax)):
            continue
        #print(xmin, xmax, ymin, ymax)
        image_url = imageCrop(cnt, xmin, xmax, ymin, ymax, trigger)
        
        #print("--------------------------------DB 적재--------------------------------" + str(cnt))
        doc_ref = db.collection(u'trainingCollection').document("trainingImage").collection(trigger).document(str(cnt))
        data = {
            "image_url" : str(image_url),
            "position": [int(xmin), int(xmax), int(ymin), int(ymax)],
            "tag" : "default"
        }
        doc_ref.set(data, merge=True)
        cnt += 1
        #print("--------------------------------노드설정및박스반환--------------------------------" + str(cnt))

        # Four corners and centroid.
        box.append([
            [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)],
            (numpy.mean(px), numpy.mean(py))])
        #print("--------------------------------노드설정및박스반환끝, 반복1사이클완료--------------------------------" + str(cnt))
    get_prediction(trigger)

    doc_ref = db.collection('trainingCollection').document("trainingImage").collection(trigger)
    docs = doc_ref.stream()
    doc_list = []
    print("--------------------------------객체insert--------------------------------")
    for doc in docs:
        doc_list.append(doc.to_dict())
    print("--------------------------------p태그 insert--------------------------------")
    for i in range(0,len(texts)-1):
        p_tag = {'position':[text_corner_x1[i],text_corner_x2[i], text_corner_y1[i], text_corner_y2[i]],'tag':'p' ,'image_url':'','data':texts[i+1]}
        doc_list.append(p_tag)
    for i in doc_list:
        i['distance'] = ((int(i['position'][1]) - int(i['position'][0]))**2 + (int(i['position'][3]) - int(i['position'][2]))**2)**0.5
    print("--------------------------------객체 배열 소팅--------------------------------")
    doc_list.sort(key=(lambda x: (x['position'][2], -x['distance'])))
    #print(doc_list)
    print("--------------------------------tag insert--------------------------------")
    for i in doc_list:
        #tree.insert(Node(i["position"][0],i["position"][2],i["position"][1],i["position"][3],i["tag"],""))
        if i["tag"] == "default":
            tree.insert(Node(i["position"][0],i["position"][1],i["position"][2],i["position"][3],'div',''))
        elif i["tag"] == "p":
            tree.insert(Node(i["position"][0],i["position"][1],i["position"][2],i["position"][3],'p' ,i['data']))
        else: 
            tree.insert(Node(i["position"][0],i["position"][1],i["position"][2],i["position"][3],i["tag"],''))

    return im.astype(numpy.uint8) * 255, box


# =============================================================================
#             
#             박스 검출 함수 호출 및 박스의 중점 검출
#             
# =============================================================================
def bin2box(trigger):
    orig = Image.open("/tmp/binaryImage.png")
    im, box = boxes(orig,trigger)

    #print("--------------------------------boxfound_start--------------------------------")
    # Boxes found.
    #os.makedirs(os.path.dirname('/tmp/boxImage.png'), exist_ok=True)
    #Image.fromarray(im).save('/tmp/boxImage.png')
    #print("--------------------------------boxfound_end--------------------------------")
    #print("--------------------------------draw rectangle_start--------------------------------")
    ## Draw perfect rectangles and the component centroid.
    #img = Image.fromarray(im)
    #visual = img.convert('RGB')
    #draw = ImageDraw.Draw(visual)
    #for b, centroid in box:
    #    draw.line(b + [b[0]], fill='yellow')
    #    cx, cy = centroid
    #    draw.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill='red')
    #os.makedirs(os.path.dirname('/tmp/boxImage_middlePoint.png'), exist_ok=True)
    #visual.save('/tmp/boxImage_middlePoint.png')
    #print("--------------------------------draw rectangle_end--------------------------------")

def createHtml(trigger):
    os.makedirs(os.path.dirname('/tmp/tree.html'), exist_ok=True)
    f = open("/tmp/tree.html", 'a', encoding="UTF-8")
    print("--------------------------------후위탐색 기반 최종코드 산출--------------------------------")
    result_code = tree.postorder(tree.root_finder())
    result_code = "<html>" + result_code + "</html>"
    f.write(result_code)
    f.close()
    #print(result_code)

    f = open("/tmp/tree.html", 'r', encoding="UTF-8")
    #print(f.read())
    html_txt = str(f.read())
    #print(html_txt)
    doc_ref = db.collection(u'trainingCollection').document("trainingImage").collection(trigger).document("0")
    data = {
        "html" : html_txt
    }
    doc_ref.set(data, merge=True)

    f.close()

    # Enable Storage
    client = storage.Client()

    # Reference an existing bucket.
    bucket = client.get_bucket('img2code-326013.appspot.com')

    # Upload a local file to a new file to be created in your bucket.
    # this upload is possible but it has bugs
    zebraBlob = bucket.blob('tmp2/tree.html')
    metadata = {'Content-Encoding': 'UTF-8','Content-Language': 'ko'}
    zebraBlob.metadata = metadata
    zebraBlob.upload_from_filename(filename='/tmp/tree.html')
    zebraBlob.make_public()
    #print(zebraBlob.public_url)
    
def imageCrop(cnt, xmin, xmax, ymin, ymax, trigger):
    area = (xmin, ymin, xmax, ymax)
    im = Image.open('/tmp/temp.png')
    cropped_image = im.crop(area)
    img_size = [xmax-xmin, ymax-ymin]
    x = img_size[0] 
    y = img_size[1] 
    
    if x != y: 
        size = max(x, y)    
        resized_img = Image.new(mode = 'RGBA', size = (size, size), color = (255,255,255,0))
        offset = (round((abs(x - size)) / 2), round((abs(y - size)) / 2))
        resized_img.paste(cropped_image, offset)
        resized_img.save('/tmp/'+str(cnt)+'.png',format="png")
    elif x==y:
        cropped_image.save('/tmp/'+str(cnt)+'.png',format="png")


    # Enable Storage
    client = storage.Client()

    # Reference an existing bucket.
    bucket = client.get_bucket('img2code-326013.appspot.com')

    # Upload a local file to a new file to be created in your bucket.
    # this upload is possible but it has bugs
    zebraBlob = bucket.blob('tmp/'+trigger+'_'+str(cnt)+'.png')
    zebraBlob.upload_from_filename(filename='/tmp/'+str(cnt)+'.png')
    zebraBlob.make_public()
    #print(zebraBlob.public_url)
    return (zebraBlob.public_url)

def get_prediction(trigger):

    doc_ref = db.collection('trainingCollection').document("trainingImage").collection(trigger)
    docs = doc_ref.stream()
    doc_list = []
    cnt = 0

    for doc in docs:
        doc_list.append(doc.to_dict())

    for i in doc_list:
        os.makedirs(os.path.dirname('/tmp/predict.png'), exist_ok=True)
        with urllib.request.urlopen(i["image_url"]) as url:
            with open('/tmp/predict.png', 'wb') as f:
                f.write(url.read())
                # print("file_write"+str(i))
        if os.path.exists('/tmp/predict.png'):
            with open('/tmp/predict.png', 'rb') as f:
                content = f.read()
                # print("file_read"+str(i))


        project_id = '585361370835'
        # model_id = 'ICN6866914109368041472'
        # model_id = 'ICN1598828445251403776'
        model_id = 'ICN119114492683485184'
        prediction_client = automl_v1beta1.PredictionServiceClient()

        m_name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
        m_payload = {'image': {'image_bytes': content }}
        m_params = {}
        request = prediction_client.predict(name=m_name, payload=m_payload, params=m_params)

        try :
            if str(request.payload[0].display_name) == "button_resized":
                tag = 'button'
            elif str(request.payload[0].display_name) == "div_resized":
                tag = 'div'
            elif str(request.payload[0].display_name) == "img_resized":
                tag = 'img'
            elif str(request.payload[0].display_name) == "input_text_resized":
                tag = 'input'
            elif str(request.payload[0].display_name) == "otherwise_resized":
                tag = 'otherwise'
            elif str(request.payload[0].display_name) == "select_resized":
                tag = 'select'
            #print(str(tag))
            doc_ref = db.collection(u'trainingCollection').document("trainingImage").collection(trigger).document(str(cnt))
            data = {
                "tag" : tag
            }
            doc_ref.set(data, merge=True)
        except:
            print("None")
        cnt = cnt + 1
    # return request  # waits till request is returned