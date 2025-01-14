import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import shutil
import torch
import cv2
set_index = ['train2017','val2017']
classes = ["normal","dz_2","dz"]

# checkpoint = torch.load("/media/zhd/data/组件/起重检测组件-20240704/训练与推理代码/weights/v4.2_300e_12000精简/hoisting_yolov8_20240816_12000_v1_1.pt")
# print("end")
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(in_file, out_file,xml_file,src_path,jpg_file):
    in_file = open(in_file)
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    out_file = open(out_file, 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    img = cv2.imread(jpg_file)
    h,w,_ = img.shape


    if root.iter('object'):
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls in classes:
                #cls_id = classes.index(cls)
                #cls_id = 0
                if cls == "dz":
                    cls_id = 0
                else:
                    cls_id = 1
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
                bb = convert((w,h), b)
                out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


for node in set_index:
    path = os.path.join('./images',node)
    for root,file,files in os.walk(path):
        cnt = 0
        total = len(files)
        for file in files:
            if file[-4:] == '.xml':
                print(str(cnt)+'/'+str(int(total/2)))
                in_file = os.path.join(root,file)
                jpg_file = in_file[:-4]+'.jpg'
                out_file = os.path.join('./labels/'+node,file[:-4]+'.txt')
                cnt +=1
                convert_annotation(in_file, out_file,file,root,jpg_file)

