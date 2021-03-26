import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.datasets as dset
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torch.optim import lr_scheduler
import cv2
import matplotlib.pyplot as plt
import numpy as np

batch_size = 1
learning_rate = 0.001
#신경망
class CNN(nn.Module):
    def __init__(self):
        super(CNN,self).__init__()
        self.layer = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.Conv2d(16, 32, 3,padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),           
            nn.Conv2d(32, 64, 3,padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)        
        )
        self.fc_layer = nn.Sequential(
            nn.Linear(13*7*7, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),            
            nn.Linear(64, 10),
        ) 
    def forward(self,x):
        out = self.layer(x)
        out = out.view(batch_size, -1)
        out = self.fc_layer(out)
        return out

img = cv2.imread("400.jpg") # 이미지 읽어오기
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) # 컬러 사진이기 때문에 흑백으로 변환해야함. 흑백으로 변환
# 그러면 사진의 연결되어 있는 것만 픽셀화함. numpy의 배열값으로 변환 해준다.
img_checker = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 191, 15)
plt.imshow(img_checker)
plt.show()
# 이미지에서 숫자가 있다면, 그 경계를 찾아주는 함수입니다.
contours, hierarchy = cv2.findContours(img_checker, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# 그래서 경계선을 찾을것을 바탕으로 사각형화 시키는 것. 시작점의 X,y좌표와 너비와 높이를 배열에 저장.
rects = [cv2.boundingRect(contour) for contour in contours]

# 그 사각형 좌표들을 for문을 돌면서 체킹
for rect in rects:
    if rect[2]*rect[3] < 1000: # 너무 작은 점도 인식하기때문에, 그 작은 점의 넓이가 1000정도 되면 매우 작은 점은 인식하지 않고 넘길 수 있다.
        continue
    # 사진 내에 숫자가 인식된 경우, 그 테두리를 초록색으로 그립니다.
    cv2.rectangle(img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3)
    if rect[2] < 50: # 전처리시 1 같은 너비가 좁은 숫자는 인식률이 좀 낮아서 너비를 넓히는 방향으로 진행.
        margin = 100
    else:
        margin = 30
    # x좌표-마진부터 x좌표+너비+마진 크기만큼 즉, 사각형의 배열의 일정 부분보다 좀더 가져올 수 있다.
    roi = img_checker[rect[1]-margin:rect[1]+rect[3]+margin, rect[0]-margin:rect[0]+rect[2]+margin]
    # 이미지 사이즈를 28*28사이즈로 줄임.
    try:
        roi = cv2.resize(roi, (28, 28), cv2.INTER_AREA)
    except Exception as e:
        print(str(e))
    # 딥러닝 모델 불러오기
    PATH = os.getcwd() + '/pytorch_cnn.pt'
    model = torch.load(PATH)
    model.eval()
    # roi 배열의 모든 값을 255.0으로 나눕니다
    roi = roi/255.0 *3.233 -0.4242
    # 딥러닝 모델에 알맞게 input 데이터를 변형합니다.
    img_input = roi.reshape(1, 1, 28, 28)
    # 그리고 그 딥러닝 모델을 예측합니다.
    img_input = torch.from_numpy(img_input).float()
    output = model.forward(img_input)
    # 그 예측값을 통해 argmax로 값을 직접 숫자화 합니다.
    num = np.argmax(output.detach().numpy())
    print(num)
    location = (rect[0]+rect[2], rect[1] + 20)
    # 사진안에 그 이미지가 있는 위치에 예측되어진 숫자를 넣는다.
    cv2.putText(img, str(num), location, cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 0), 2)

#사진 보여주고 종료
cv2.imwrite("answer.jpg", img)
