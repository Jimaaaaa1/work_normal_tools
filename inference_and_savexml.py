from hashlib import sha1
from operator import le
from random import shuffle
import cv2
from ultralytics import YOLO
import os
# Load a model
import xml.dom.minidom as DOC

#import matplotlib.pyplot as plt

def Bbox_area(bbox):
    """计算边界框的面积."""
    return (bbox[2] - bbox[0] + 1) * (bbox[3] - bbox[1] + 1)

def Bbox_intersection(bbox1, bbox2):
    """计算两个边界框的交集面积."""
    inter_xmin = max(bbox1[0], bbox2[0])
    inter_ymin = max(bbox1[1], bbox2[1])
    inter_xmax = min(bbox1[2], bbox2[2])
    inter_ymax = min(bbox1[3], bbox2[3])
    if inter_xmin < inter_xmax and inter_ymin < inter_ymax:
        inter_area = (inter_xmax - inter_xmin + 1) * (inter_ymax - inter_ymin + 1)
    else:
        inter_area = 0
    return inter_area

def Bbox_iou(bbox1, bbox2):
    """计算两个边界框的 IOU."""
    area1 = Bbox_area(bbox1)
    area2 = Bbox_area(bbox2)
    inter_area = Bbox_intersection(bbox1, bbox2)
    iou = inter_area / float(area1 + area2 - inter_area) if area1 + area2 - inter_area > 0 else 0.0
    return iou

def nms(boxes, threshold):
    """应用非极大值抑制来去除重叠的框。"""
    # 如果没有框，直接返回空列表
    if len(boxes) == 0:
        return []
    # 按照得分降序排序
    boxes.sort(key=lambda x: x[4], reverse=True)
    # 用于存放保留的框
    picked_boxes = []
    # 遍历排序后的框
    while len(boxes) > 0:
        # 保留当前得分最高的框
        best_box = boxes.pop(0)
        picked_boxes.append(best_box)
        # 计算当前框与其余框的IoU，并移除重叠度高于阈值的框
        boxes = [box for box in boxes if Bbox_iou(best_box, box) < threshold]
    return picked_boxes

def generate_xml(img_name, coords, img_size, out_root_path):
    '''
    输入：
        img_name：图片名称，如a.jpg
        coords:坐标list，格式为[[, y_min, x_max, y_max, name]]，name为概况的标注
        img_size：图像的大小,格式为[h,w,c]
        out_root_path: xml文件输出的根路径
    '''
    os.makedirs(out_root_path, exist_ok=True)
    doc = DOC.Document()  # 创建DOM文档对象

    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)

    title = doc.createElement('folder')
    title_text = doc.createTextNode('Tianchi')
    title.appendChild(title_text)
    annotation.appendChild(title)

    title = doc.createElement('filename')
    title_text = doc.createTextNode(img_name)
    title.appendChild(title_text)
    annotation.appendChild(title)

    source = doc.createElement('source')
    annotation.appendChild(source)

    title = doc.createElement('database')
    title_text = doc.createTextNode('The Tianchi Database')
    title.appendChild(title_text)
    source.appendChild(title)

    title = doc.createElement('annotation')
    title_text = doc.createTextNode('Tianchi')
    title.appendChild(title_text)
    source.appendChild(title)

    size = doc.createElement('size')
    annotation.appendChild(size)

    title = doc.createElement('width')
    title_text = doc.createTextNode(str(img_size[1]))
    title.appendChild(title_text)
    size.appendChild(title)

    title = doc.createElement('height')
    title_text = doc.createTextNode(str(img_size[0]))
    title.appendChild(title_text)
    size.appendChild(title)

    title = doc.createElement('depth')
    title_text = doc.createTextNode(str(img_size[2]))
    title.appendChild(title_text)
    size.appendChild(title)

    for coord in coords:
        object = doc.createElement('object')
        annotation.appendChild(object)

        title = doc.createElement('name')
        title_text = doc.createTextNode(coord[4])
        title_text = doc.createTextNode(title_text._data)
        title.appendChild(title_text)
        object.appendChild(title)

        pose = doc.createElement('pose')
        pose.appendChild(doc.createTextNode('Unspecified'))
        object.appendChild(pose)
        truncated = doc.createElement('truncated')
        truncated.appendChild(doc.createTextNode('1'))
        object.appendChild(truncated)
        difficult = doc.createElement('difficult')
        difficult.appendChild(doc.createTextNode('0'))
        object.appendChild(difficult)

        bndbox = doc.createElement('bndbox')
        object.appendChild(bndbox)
        title = doc.createElement('xmin')
        title_text = doc.createTextNode(str(int(float(coord[0]))))
        title.appendChild(title_text)
        bndbox.appendChild(title)
        title = doc.createElement('ymin')
        title_text = doc.createTextNode(str(int(float(coord[1]))))
        title.appendChild(title_text)
        bndbox.appendChild(title)
        title = doc.createElement('xmax')
        title_text = doc.createTextNode(str(int(float(coord[2]))))
        title.appendChild(title_text)
        bndbox.appendChild(title)
        title = doc.createElement('ymax')
        title_text = doc.createTextNode(str(int(float(coord[3]))))
        title.appendChild(title_text)
        bndbox.appendChild(title)

    # 将DOM对象doc写入文件
    f = open(os.path.join(out_root_path, img_name[:-4] + '.xml'), 'w')
    f.write(doc.toprettyxml(indent=''))
    f.close()



if __name__ == '__main__':
    import shutil

    model = YOLO('/media/zhd/data/组件/反光背心检测组件-20240710/weights/20250106_fgbx_100e_32000_v7/检测权重/changtaihua_fgbx_yolov8_20250106_32000_v1_8.pt')  # load an official model
    #fgbx = /media/zhd/data/组件/反光背心检测组件-20240710/weights/20241212_fgbx_100e_40000_v6/weights/changtaihua_fgbx_yolov8_20241212_40000_v1_7.pt
    #dz = /media/zhd/data/组件/起重检测组件-20240704/weights/v55_100e_24000_20241207/weights/crane_lifting_yolov11_20241207_24000_v1_8.pt
    #       /media/zhd/data/组件/起重检测组件-20240704/weights/v52_100e_22500_20241009/yolo11/weights/best.pt
    #/media/zhd/data/工具/yolo11m.pt

    for root,file,files in os.walk('/media/zhd/data/数据/安全帽数据/ori_train/ori_helmet_images'):
        files.sort()
        for file in files:
            if file.endswith('.jpg'):
                img = cv2.imread(os.path.join(root,file))
                #results = model(os.path.join(root,file), save=True, conf=0.1, iou=0.4, imgsz=(1280,1280), show_labels=True, show_conf=True, show=False, agnostic_nms=True)  # predict on an image
                results = model(os.path.join(root, file), save=False, conf=0.1, iou=0.4, imgsz=(1280, 1280), show_labels=False, show_conf=False, show=False, agnostic_nms=True)
                res = [] #,
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
                        # if cls != 67: #phone
                        #     continue
                        xyxy = box.xyxy
                        #print(xyxy,cls)
                        x1 = int(xyxy[0][0])
                        y1 = int(xyxy[0][1])
                        x2 = int(xyxy[0][2])
                        y2 = int(xyxy[0][3])
                        res.append([x1, y1, x2, y2, cls_name])

                #shutil.copy(os.path.join(root, file), os.path.join('/media/zhd/data/数据/反光背心和反光带数据/人员数据/fgd数据_dl/tmp', file))
                generate_xml(file, res, img.shape, '/media/zhd/data/数据/安全帽数据/ori_train/fgbx_labels')


                # for result in results:
                #     boxes = result.boxes  # Boxes object for bounding box outputs
                #     masks = result.masks  # Masks object for segmentation masks outputs
                #     keypoints = result.keypoints  # Keypoints object for pose outputs
                #     probs = result.probs  # Probs object for classification outputs
                #     obb = result.obb  # Oriented boxes object for OBB outputs
                #     result.plot(show=False, save=True, filename=save_res_path + file)
                #     #result.display(show=True, labels=True, save_dir=save_res_path + file)
                #     #result.show()  # display to screen

                # if len(res) ==0:
                #     shutil.move(os.path.join(root,file),os.path.join('/media/zhd/data/组件/玩手机_检测_20240809/训练代码/测试数据和结果',file))
                # else:
                #     shutil.move(os.path.join(root,file),os.path.join('/media/zhd/data/组件/玩手机_检测_20240809/训练代码/测试数据和结果',file))
                #     generate_xml(file, res, img.shape, '/media/zhd/data/组件/玩手机_检测_20240809/训练代码/测试数据和结果')

