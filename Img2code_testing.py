#비전 API 설정법
#https://cloud.google.com/vision/docs/setup?hl=ko#windows

#json파일명
#deductive-motif-316110-2d8de37aca8c.json"
from google.cloud import vision
import cv2
import io, json
from google.cloud import vision_v1
from google.cloud.vision_v1 import AnnotateImageResponse
import proto
import matplotlib.pyplot as plt
import numpy as np
import sys
import numpy
from PIL import Image, ImageOps, ImageDraw
from scipy.ndimage import morphology, label
class Node:
    def __init__(self, x_position1, y_position1, x_position2, y_position2, name):
        self.xdis = x_position2 - x_position1
        self.ydis = y_position2 - y_position1
        self.x1 = x_position1
        self.y1 = y_position1
        self.x2 = x_position2
        self.y2 = y_position2
        self.left = None
        self.right = None
        self.parent = None
        self.data = name
              
class BinaryTree():
    #트리 생성
    def __init__(self):
        self.root = None
        self.result = ""
        self.result_temp = ""
        self.right_end = 0
        
    def root_finder(self):
        return self.root
        
    def insert(self, node):
        self.root = self._insert_value(self.root, node)
        return self.root is not None
           
    def _insert_value(self, sub_root, node):
        if sub_root is None:
            sub_root = node
            
        else:
            if sub_root.x1 < node.x1 and sub_root.x2  > node.x2 and sub_root.y1 < node.y1 and sub_root.y2 > node.y2:
                # 지금 들어온 box가 subroot의 내부에 위치하는 경우로 왼쪽의 child로 들어간다
                node.parent = sub_root
                sub_root.left = self._insert_value(sub_root.left, node) 
                
            elif (sub_root.x1 > node.x1 and sub_root.x2  < node.x2 and sub_root.y1 > node.y1 and sub_root.y2 < node.y2) or (sub_root.y1 > node.y2):
                sub_root.parent = node
                node = self._insert_value(node, sub_root)
               
                if sub_root.right is not None:
                    node = self._insert_value(node, sub_root.right)
                    sub_root.right = None
                    if sub_root.left is not None:
                        node = self._insert_value(node, sub_root.left)
                return node
            
            else:
                node.parent = sub_root
                sub_root.right = self._insert_value(sub_root.right, node)

        return sub_root
    
    #후위 순회
    def postorder(self, node):
        if node != None:
            #오른쪽 서브트리 순회
            if node.right:
                self.postorder(node.right)
                self.right_end = 1
                
            #왼쪽 서브트리 순회
            if node.left:
                self.postorder(node.left)
                self.right_end = 0
            
            #노드 방문
            if node == self.root_finder():
                self.result_temp = self.result + self.result_temp
                
            if not self.right_end:
                self.result = "<div style = \" border:1px solid black; width: " + str(node.xdis) +"px; height:" + str(node.ydis) +"px; position: absolute; top: "+str(node.y1)+"px; left: "+str(node.x1)+"px;"+"\">"  + self.result + "</div>"
            else:
                self.result_temp = self.result + self.result_temp
                self.result = ""
                self.result = "<div style = \" border:1px solid black; width: " + str(node.axdis) +"px; height:" + str(node.ydis) +"px; position: absolute; top: "+str(node.y1)+"px; left: "+str(node.x1)+"px;"+"\">" + "</div>"
         
        return self.result_temp
                
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
# =============================================================================
#             
#             목업 이미지에 구글 OCR 사용 텍스트 검출
#             결과값 json 타입으로 변환
#             
# =============================================================================
def ocr():
    
    client = vision.ImageAnnotatorClient()
    path = './naver_login.png'
    # path = './6-1 로그인.png'
    # path = './9-1 상품연결.png'
    # path = './naver.png'
    # path = './google_lee.png'

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # price_candidate = []
    # card_number_candidate = []
    # date_candidate = []

    response = client.text_detection(image=image)
    # serialize / deserialize proto (binary)
    serialized_proto_plus = AnnotateImageResponse.serialize(response)
    response = AnnotateImageResponse.deserialize(serialized_proto_plus)
    print(response.full_text_annotation.text)

    # serialize / deserialize json
    response_json = AnnotateImageResponse.to_json(response)
    response = json.loads(response_json)
    print(response['fullTextAnnotation']['text'])

    with open("textInImage.json", "w") as json_file:
        json.dump(response, json_file)


# =============================================================================
#             
#             목업 이미지를 바이너리 이미지로 변환하여 정확한 물체 검출
#             이미지 x, y 좌표의 변화량 확인
#             
# =============================================================================
def img2bin():
    img = ('naver_login.png')
    # img = ('6-1 로그인.png')
    # img = ('9-1 상품연결.png')
    # img = ('naver.png')
    # img = ('google_lee.png')

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
                X_filter[x][y] = 1
        X_filter[x][h-1] = 1   
            
    D_filter = X_filter + 2*Y_filter

    for x in range(0, w):
        for y in range(0, h):
            if(D_filter[x][y] != 0):
                D_filter[x][y] = 1

    text = []
    with open('./textInImage.json', 'r') as f:
        json_data = json.load(f)

    count = 0

    for i in json_data["textAnnotations"]:
        texts.append(i['description'])
        text.append(i['boundingPoly']['vertices'])
        count = count + 1

    for index in range(1,count):
        # print(text[index][0]['x'],text[index][0]['y'],text[index][2]['x'],text[index][2]['y'])
        text_corner_x1.append(text[index][0]['x'])
        text_corner_y1.append(text[index][0]['y'])
        text_corner_x2.append(text[index][2]['x'])
        text_corner_y2.append(text[index][2]['y'])
        for x in range(text_corner_y1[index-1], text_corner_y2[index-1]):
            for y in range(text_corner_x1[index-1], text_corner_x2[index-1]):
                D_filter[x][y] = 0

    np.savetxt("D_filter.txt",D_filter,fmt='%d')    

    plt.imsave('binaryImage.png', D_filter)


# =============================================================================
#             
#             바이너리 이미지로부터 박스 검출
#             
# =============================================================================
def boxes(orig):
    img = ImageOps.grayscale(orig)
    im = numpy.array(img)

    # Inner morphological gradient.
    im = morphology.grey_dilation(im, (3, 3)) - im

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
    for i in range(1, numcc + 1):
        py, px = numpy.nonzero(lbl == i)
        if len(py) < min_size:
            im[lbl == i] = 0
            continue

        xmin, xmax, ymin, ymax = px.min(), px.max(), py.min(), py.max()
        print(xmin, xmax, ymin, ymax)
        node = Node(xmin, ymin, xmax, ymax)
        tree.insert(node)
        # Four corners and centroid.
        box.append([
            [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)],
            (numpy.mean(px), numpy.mean(py))])
    # for i in range(0,len(box)):
    #     print(box[i])
    return im.astype(numpy.uint8) * 255, box


# =============================================================================
#             
#             박스 검출 함수 호출 및 박스의 중점 검출
#             
# =============================================================================
def bin2box():
    orig = Image.open('binaryImage.png')
    im, box = boxes(orig)

    # Boxes found.
    Image.fromarray(im).save('boxImage.png')

    # Draw perfect rectangles and the component centroid.
    img = Image.fromarray(im)
    visual = img.convert('RGB')
    draw = ImageDraw.Draw(visual)
    for b, centroid in box:
        draw.line(b + [b[0]], fill='yellow')
        cx, cy = centroid
        draw.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill='red')
    visual.save('boxImage_middlePoint.png')

def textTag():
    f = open("tree.html", 'w')
    for i in range(1,len(texts)):
        f.write("<p style=\"font-size: 10px; width:"+str(text_corner_x2[i-1]-text_corner_x1[i-1])+"px; height:"+str(text_corner_y2[i-1]-text_corner_y1[i-1])+"px; position: absolute; top: "+str(text_corner_y1[i-1])+"px; left: "+str(text_corner_x1[i-1])+"px;"+"\"> "+str(texts[i])+"</p>")
        # node = Node(text_corner_x1[i-1], text_corner_y1[i-1], text_corner_x2[i-1], text_corner_y2[i-1], str(texts[i]))
        # tree.insert(node)
        print(i,texts[i],text_corner_x1[i-1], text_corner_y1[i-1])
        print(i,texts[i],text_corner_x2[i-1], text_corner_y2[i-1])
    f.close()
def createHtml():
    
    # node1 = Node("10", 0, 0, x_size, y_size)
    # node2 = Node("20", 100, 100, 800, 250)
    # node3 = Node("30", 600, 150, 700, 200)
    # node4 = Node("40", 100, 400, 800, 550)
    # node5 = Node("50", 600, 450, 700, 500)
    # node6 = Node("60", 100, 700, 800, 850)
    # node7 = Node("70", 600, 750, 700, 800)

    # tree.insert(node1)
    # tree.insert(node2)
    # tree.insert(node3)
    # tree.insert(node4)
    # tree.insert(node5)
    # tree.insert(node6)
    # tree.insert(node7)

    f = open("tree.html", 'a')
    result_code = tree.postorder(tree.root_finder())
    result_code = "<html>" + result_code + "</html>"
    f.write(result_code)
    f.close()
    print(result_code)
    
# ocr()
img2bin()
bin2box()
textTag()
createHtml()



