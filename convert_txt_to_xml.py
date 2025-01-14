import os
import xml.etree.ElementTree as ET
from PIL import Image

# 假设txt标注文件和图片都在这个文件夹内
image_folder = "/media/zhd/data/数据/打电话数据/网络数据集1/大尺寸图片/images"
label_folder = "/media/zhd/data/数据/打电话数据/网络数据集1/大尺寸图片/labels"

# 准备转换的类别
class_names = ["phone"]

def convert_to_pixel_coordinates(bb, w, h):
    """
    将归一化的边界框坐标转换为像素坐标。
    bb: (xmin, ymin, xmax, ymax) (归一化)
    w: 图像的宽度
    h: 图像的高度
    返回： (xmin_pixel, ymin_pixel, xmax_pixel, ymax_pixel)
    """
    xmin, ymin, xmax, ymax = bb
    xmin_pixel = int(xmin * w)
    ymin_pixel = int(ymin * h)
    xmax_pixel = int(xmax * w)
    ymax_pixel = int(ymax * h)
    return xmin_pixel, ymin_pixel, xmax_pixel, ymax_pixel


import xml.etree.ElementTree as ET


def convert_to_pixel_coordinates(bb, w, h):
    """
    将归一化的边界框坐标转换为像素坐标。
    bb: (xmin, ymin, xmax, ymax) (归一化)
    w: 图像的宽度
    h: 图像的高度
    返回： (xmin_pixel, ymin_pixel, xmax_pixel, ymax_pixel)
    """
    xmin, ymin, xmax, ymax = bb
    xmin_pixel = int(xmin * w)
    ymin_pixel = int(ymin * h)
    xmax_pixel = int(xmax * w)
    ymax_pixel = int(ymax * h)
    return xmin_pixel, ymin_pixel, xmax_pixel, ymax_pixel


def convert_yolo_to_xml(txt_file, image_width, image_height, output_xml):
    """
    从 YOLO 格式的 txt 文件转换为 XML 格式。
    txt_file: YOLO 格式的标签文件路径
    image_width: 图像的宽度
    image_height: 图像的高度
    output_xml: 输出的 XML 文件路径
    """
    # 创建 XML 的根元素
    annotation = ET.Element("annotation")

    # 创建 XML 中的 `size` 元素
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(image_width)
    ET.SubElement(size, "height").text = str(image_height)
    ET.SubElement(size, "depth").text = "3"  # 假设是 RGB 彩色图像

    # 打开 YOLO 格式的 txt 文件进行读取
    with open(txt_file, 'r') as f:
        for line in f:
            parts = line.strip().split()

            class_id = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])

            # 转换归一化坐标为像素坐标
            xmin = int((x_center - width / 2) * image_width)
            ymin = int((y_center - height / 2) * image_height)
            xmax = int((x_center + width / 2) * image_width)
            ymax = int((y_center + height / 2) * image_height)

            # 创建 <folder> 和 <filename> 元素
            folder = ET.SubElement(annotation, "folder")
            folder.text = "filename"  # 获取文件夹名
            filename = ET.SubElement(annotation, "filename")
            filename.text = "image_name"
            path = ET.SubElement(annotation, "path")
            path.text = "image_path"

            # 创建 <source> 元素
            source = ET.SubElement(annotation, "source")
            database = ET.SubElement(source, "database")
            database.text = "Unknown"


            # 创建 XML 中的 `object` 元素
            obj = ET.SubElement(annotation, "object")
            ET.SubElement(obj, "name").text = class_names[class_id]  # 假设类别 ID 即为类别名称
            ET.SubElement(obj, "pose").text = "Unspecified"
            ET.SubElement(obj, "truncated").text = "0"
            ET.SubElement(obj, "difficult").text = "0"

            # 创建边界框元素 `bndbox`
            bndbox = ET.SubElement(obj, "bndbox")
            ET.SubElement(bndbox, "xmin").text = str(xmin)
            ET.SubElement(bndbox, "ymin").text = str(ymin)
            ET.SubElement(bndbox, "xmax").text = str(xmax)
            ET.SubElement(bndbox, "ymax").text = str(ymax)

    # 将 XML 树写入文件
    tree = ET.ElementTree(annotation)
    tree.write(output_xml)

def convert_all_txt_to_xml():
    # 遍历所有txt文件并转换
    for txt_file in os.listdir(label_folder):
        if txt_file.endswith(".txt"):
            # 获取对应的图片文件
            # img_file = os.path.join(image_folder, txt_file.replace(".txt", ".jpeg"))
            # image = Image.open(img_file)
            try:
                img_file = os.path.join(image_folder, txt_file.replace(".txt", ".jpeg"))
                image = Image.open(img_file)
            except Exception as e:
                img_file = os.path.join(image_folder, txt_file.replace(".txt", ".png"))
                image = Image.open(img_file)

            txt_file_path = os.path.join(label_folder, txt_file)
            output_xml = txt_file.replace(label_folder, "").replace(".txt", ".xml")
            output_xml = os.path.join(label_folder, output_xml)
            width, height = image.size
            convert_yolo_to_xml(txt_file_path, width, height, output_xml)


# 调用函数开始转换
convert_all_txt_to_xml()
