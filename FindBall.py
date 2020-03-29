#Import per eseguire il programma
from __future__ import print_function
#import PIL
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import cv2
import numpy as np
import requests as rq
import time
import matplotlib.image as pli
import time as timer
from random import seed
from random import randint
#ip=!ifconfig eth0 | grep -Po 'inet \K([\d\.]+)'
ip='192.168.0.32'
#from IPython.core.display import HTML
#HTML('<img width=320" src="http://%s:3000/video/0">'%ip)
# take a snapshot
def snap(i,  pref):
    url = "http://%s:3000/image"%(ip)
    r = rq.get(url)
    file = "%s-%d.jpg"%(pref,i)
    content = r.content
    with open(file, "wb") as f:
        f.write(content)
    return file
#Analizzare la foto per vedere se c'è la palla
dir = "./data/ok"
files = [ f"{dir}/{file}" for file in os.listdir(dir) ]
classes = None
with open("yolov3.txt", 'r') as f:
    classes = [line.strip() for line in f.readlines()]
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers
def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
#Applicare lo YOLO
def app_yolo(ft):
    frame=np.zeros((32,32,3), np.uint8)
    frame[16,0:31,:]=255
    ret,buf=cv2.imencode(ft,frame)
    f=cv2.imdecode(buf,cv2.IMREAD_COLOR)
    n = 1
    image = cv2.imread(ft)
    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
            
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))
    return (class_ids, boxes, image)
#print (x,y,w,h)
def find_ball(class_ids, boxes, image):
    
    fnd = False
    time = 100
    step_move = 100
    step_rotate = 10
    dir = ""
    t = randint(0,10000000)
    i=class_ids.index(32)
    box = boxes[i]
    x = box[0]
    y = box[1]
    w = box[2]
    h = box[3]
   #in base ai calcoli si muove
    if (x > image.shape[1]/2+w+50):
         dir = "right/%d" % step_rotate         
    if (x < image.shape[1]/2-w-50):
         dir = "left/%d" % step_rotate
    if (image.shape[1]/2-w-50<=x) and (x<=image.shape[1]/2+w+50):
        step_move = 400
        dir = "forward/%d" % step_move
    if image.shape[0]/2<y:
                fnd = True
    html = 'http://%s:3000/move/%s/%d?%d'%(ip, dir, time, t)
    r = rq.get(html)
    #if dir != "":
       # display(HTML(html))
    #print(html)
    return fnd
def rotate():
    m = 0
    fnd = False
    time = 100
    step_move = 100
    step_rotate = 10
    while m<=4:
        m=m+1
        t = randint(0,10000000)
        dir = "left/%d" % step_rotate
        html = 'http://%s:3000/move/%s/%d?%d'%(ip, dir, time, t)
        r = rq.get(html)

       # if dir != "":
            #r = request.post(html)
            #display(HTML(html))
def gofw():
    m = 0
    fnd = False
    time = 100
    step_move = 100
    while m<=6:
        m=m+1
        t = randint(0,10000000)
        dir = "forward/%d" % step_move
        html = 'http://%s:3000/move/%s/%d?%d'%(ip, dir, time, t)
        r = rq.get(html)

        #if dir != "":
            #r = request.post(html)
            #display(HTML(html))
def gobk():
    time = 100
    step_move = 10
    t = randint(0,10000000)
    dir = "backward/%d" % step_move
    html = 'http://%s:3000/move/%s/%d?%d'%(ip, dir, time, t)
    r = rq.get(html)

   # if dir != "":
        #display(HTML(html))
fnd = False
rtd = False
oncefd = False
j = 0

while j<100 and fnd == False:
    ft = snap(0, "tmp/snap")
    clid, boxes, image = app_yolo(ft)
    j=j+1
    
    if (32 in clid):
        
        fnd = find_ball(clid,boxes,image)
        oncefd = True
    else: 
        if oncefd == False:
            if rtd == False:
                rotate()
                rtd = True
            else:
                gofw()
                rtd = False
        else:
            gobk()
