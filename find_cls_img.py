import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import shutil
import cv2
from ultralytics import YOLO
from inference_and_savexml import generate_xml

def find_annotation(in_file, copy_to_path):
    in_file_path = in_file
    in_file = open(in_file_path)
    tree=ET.parse(in_file)
    root = tree.getroot()

    #size = root.find('size')
    #img = cv2.imread(jpg_file)
    #h,w,_ = img.shape


    if root.iter('object'):
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls in classes:
                #cls_id = classes.index(cls)
                #cls_id = 0
                if cls == classes[0]:
                    cls_id = 0
                elif cls == classes[1]:
                    cls_id = 1
                elif cls == classes[2]:
                    cls_id = 2
                    try:
                        shutil.copy(in_file_path, copy_to_path)
                    except Exception as e:
                        print(e)
                elif cls == classes[3]:
                    cls_id = 0


#set_index = ['train_xml','val_xml']


if __name__ == '__main__':
    set_index = ['']
    classes = ["fgbx", "nofgbx", "fgd", "fgbx_unique"]
    # classes = ["fgbx", "nowear", "wear", "none"]
    # classes = ["head", "person", "helmet", "none"]


    path = '/media/zhd/data/数据/反光背心和反光带数据/反光背心数据/反光背心数据过滤_v5(v2+new))(完整)/labels/val'
    copy_to_path = '/media/zhd/data/数据/反光背心和反光带数据/反光背心数据/反光背心数据过滤_v5(v2+new))(完整)/labels_fgd/val'
    model_path = '/media/zhd/data/组件/反光背心检测组件-20240710/yolov8_local/runs/detect/train2/weights/best.pt'

    find_in_xml = True
    if find_in_xml:
        for node in set_index:
            #path = os.path.join('./labels',node)
            for root,file,files in os.walk(path):
                cnt = 0
                total = len(files)
                for file in files:
                    if file[-4:] == '.xml':
                        print(str(cnt)+'/'+str(int(total/2)))
                        in_file = os.path.join(root,file)
                        cnt += 1
                        find_annotation(in_file, copy_to_path)
    else:
        model = YOLO(model_path)
        for root,file,files in os.walk(path):
            for file in files:
                if file.endswith('.jpg'):
                    img = cv2.imread(os.path.join(root,file))
                    results = model(os.path.join(root,file), save=False, conf=0.1, iou=0.5, imgsz=(1280,1280), show_labels=False, show_conf=False, show=False)  # predict on an image
                    res = []
                    for result in results:
                        boxes = result.boxes
                        cls_names = result.names
                        # print(len(boxes))
                        if len(boxes) == 0:
                            continue
                        for box in boxes:
                            # print(box)
                            cls = int(box.cls)
                            cls_name = cls_names[cls]
                            xyxy = box.xyxy
                            # print(xyxy,cls)
                            x1 = int(xyxy[0][0])
                            y1 = int(xyxy[0][1])
                            x2 = int(xyxy[0][2])
                            y2 = int(xyxy[0][3])
                            res.append([x1, y1, x2, y2, cls_name])
                        shutil.copy(os.path.join(root, file), os.path.join(copy_to_path, file))
                        generate_xml(file, res, img.shape, copy_to_path)
