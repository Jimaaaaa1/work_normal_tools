import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import shutil
import cv2

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

def convert_annotation(in_file, out_file, xml_file,src_path):
    in_file = open(in_file)
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    out_file = open(out_file, 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()

    #size = root.find('size')
    #img = cv2.imread(jpg_file)
    #h,w,_ = img.shape


    if root.iter('object'):
        for obj in root.iter('object'):
            cls = obj.find('name').text
            #dz
            try:
                if cls in classes[0]:
                    if cls == classes[0][0]:
                        cls_id = 0
                    elif cls == classes[0][1]:
                        cls_id = 0
                    elif cls == classes[0][2]:
                        cls_id = 1
                    elif cls == classes[0][3]:
                        cls_id = 1
                    elif cls == classes[0][4]:
                        cls_id = 1
                    elif cls == classes[0][5]:
                        cls_id = 1
                    elif cls == classes[0][6]:
                        cls_id = 1
                #fgbx
                elif cls in classes[1]:
                    if cls == classes[1][0]:
                        cls_id = 0
                    elif cls == classes[1][1]:
                        cls_id = 1
                    elif cls == classes[1][2]:
                        cls_id = 1
                    elif cls == classes[1][3]:
                        cls_id = 0
                #xftd
                elif cls in classes[2]:
                    if cls == classes[2][0]:
                        cls_id = 0
                    elif cls == classes[2][1]:
                        cls_id = 1
                    elif cls == classes[2][2]:
                        cls_id = 2
                #phone
                elif cls in classes[3]:
                    if cls == classes[3][0]:
                        cls_id = 0

                xmlbox = obj.find('bndbox')
                size = root.find('size')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
                h = int(size.find('height').text)
                w = int(size.find('width').text)
                bb = convert((w,h), b)
                out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
            except Exception as e:
                print("This class is not belong to this task: ", cls)


#set_index = ['train_xml','val_xml']
set_index = ['']
classes_dz = ["dz","dz_2","dz_3","dg_normal","dg_roller","dg_sector","dg"] #起重吊装
classes_fgbx = ["fgbx","nofgbx","fgd","fgbx_unique"] #反光背心
classes_xftd = ['zx', 'cylinder', 'unnormal'] #消防通道
classes_phone = ['phone']
classes = [classes_dz, classes_fgbx, classes_xftd, classes_phone]

for node in set_index:
    #path = os.path.join('./labels',node)
    path = '/media/zhd/data/数据/反光背心和反光带数据/反光背心数据/反光背心数据过滤_v5(v2+new))(完整)/labels_fgbx_nofgbx/val/' + node
    for root,file,files in os.walk(path):
        cnt = 0
        total = len(files)
        for file in files:
            if file[-4:] == '.xml':
                print(str(cnt)+'/'+str(int(total/2)))
                in_file = os.path.join(root,file)
                #jpg_file = in_file[:-4]+'.jpg'
                out_file = os.path.join(path, file[:-4]+'.txt')
                cnt += 1
                convert_annotation(in_file, out_file, file, root)

