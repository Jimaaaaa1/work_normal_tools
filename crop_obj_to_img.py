import cv2
import torch
from ultralytics import YOLO
import os
import time
import xml.etree.ElementTree as ET

def crop_raw_img(img, locations, ratio=1.0, resize_fix=-1):
    croppped_imgs = []
    for location in locations:
        x1, y1, x2, y2, _, _ = location
        if img is not None:
            cropped_image = img[y1:y2, x1:x2]
            if resize_fix != -1:
                dsize = (resize_fix, resize_fix)
            else:
                dsize = (int(cropped_image.shape[1]*ratio), int(cropped_image.shape[0]*ratio))
            resized_image = cv2.resize(cropped_image, dsize, interpolation=cv2.INTER_LINEAR)
            croppped_imgs.append(resized_image)
        #croppped_imgs.append(cropped_image)
    return croppped_imgs

def crop_save_img(img_path, out_path, xml_paths, need_xml=False, resize_fix=-1):
    os.makedirs(out_path, exist_ok=True)
    for root, file, files in os.walk(img_path):
        for file in files:
            if file.endswith('.jpg'):
                abs_img_path = os.path.join(root, file)
                img = cv2.imread(abs_img_path)
                if not need_xml:
                    infer_results = model(img, save=False, conf=0.1, iou=0.4, imgsz=(1280, 1280),
                                    show_labels=False, show_conf=False, show=False,
                                    agnostic_nms=True)  # predict on an image
                    results = []
                    for i, prediction in enumerate(infer_results):
                        boxes_data = prediction.boxes.data.cpu().numpy()
                        cls_name = model.names
                        for row in boxes_data:
                            cls_index = row[-1]
                            box_name = cls_name[cls_index]
                            box = [int(row[0]), int(row[1]), int(row[2]), int(row[3]), round(float(row[4]), 2), box_name]
                            results.append(box)
                else:
                    xml_path = os.path.join(xml_paths, file[:-4] + '.xml')
                    results = []
                    try:
                        tree = ET.parse(xml_path)
                        xml_root = tree.getroot()
                        # 遍历所有对象
                        for obj in xml_root.findall('object'):
                            name = obj.find('name').text
                            bndbox = obj.find('bndbox')
                            xmin = int(bndbox.find('xmin').text)
                            ymin = int(bndbox.find('ymin').text)
                            xmax = int(bndbox.find('xmax').text)
                            ymax = int(bndbox.find('ymax').text)
                            results.append([xmin, ymin, xmax, ymax, 1, name])
                    except Exception as e:
                        continue
                if results:
                    try:
                        crop_images = crop_raw_img(img, results, ratio=1.0, resize_fix=-1)
                        for i, (crop_image, crop_location) in enumerate(zip(crop_images, results)):
                            cls_name = crop_location[5]
                            cls_out_path = os.path.join(out_path, cls_name)
                            os.makedirs(cls_out_path, exist_ok=True)
                            save_path = os.path.join(cls_out_path, f"{file}_{i}.jpg")
                            cv2.imwrite(save_path, crop_image)
                    except Exception as e:
                        print(file)

#有没有xml
with_xml = True
if not with_xml:
    model = YOLO('/media/zhd/data/组件/反光背心检测组件-20240710/weights/vest_39000_11000_v4/changtaihua_fgbx_yolov8_20240925_39000_v1_6.pt')
    xml_path = None
else:
    #如果有，给出xmlpath
    xml_path = '/media/zhd/data/数据/反光背心和反光带数据/反光背心数据/反光背心数据过滤_v5(v2+new))(完整)/labels(20250102保留备份)/val'
img_path = '/media/zhd/data/数据/反光背心和反光带数据/反光背心数据/反光背心数据过滤_v5(v2+new))(完整)/images/val'
out_path = '/media/zhd/data/数据/反光背心和反光带数据/反光带分类数据/反光带分类数据_v2/val'

crop_save_img(img_path=img_path, out_path=out_path, xml_paths=xml_path, need_xml=with_xml, resize_fix=-1)

