import os
import xml.etree.ElementTree as ET
import shutil


def get_bbox_size(box):
    xmin = int(box.find('xmin').text)
    ymin = int(box.find('ymin').text)
    xmax = int(box.find('xmax').text)
    ymax = int(box.find('ymax').text)
    width = xmax - xmin
    height = ymax - ymin
    return width, height


def count_bbox_sizes(folder_path):
    size_counts = {
        '0-100': 0,
        '0-400': 0,
        '0-900': 0,
        '0-1600': 0,
        '0-2500': 0,
        '0-3600': 0,
    }
    tiny_obj_path = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)
            tree = ET.parse(file_path)
            root = tree.getroot()
            img_size = root.findall('size')
            img_w, img_h = int(img_size[0].find('width').text), int(img_size[0].find('height').text)
            area_limit = img_w * img_h * target_limit
            for obj in root.findall('object'):
                bbox = obj.find('bndbox')
                if bbox is not None:
                    width, height = get_bbox_size(bbox)
                    bbox_area = width * height
                    if bbox_area < 100:
                        size_counts['0-100'] += 1
                    elif bbox_area < 400:
                        size_counts['0-400'] += 1
                    elif bbox_area < 900:
                        size_counts['0-900'] += 1
                    elif bbox_area < 1600:
                        size_counts['0-1600'] += 1
                    elif bbox_area < 2500:
                        size_counts['0-2500'] += 1
                    elif bbox_area < 3600:
                        size_counts['0-3600'] += 1

                    if bbox_area < area_limit:
                        tiny_obj_path.append(file_path)

    return size_counts, tiny_obj_path


def mv_tiny_obj_img(xml_paths, img_path, mv_to_path):
    for xml_path in xml_paths:
        # 获取文件名和目录
        dir_name, file_name = os.path.split(xml_path)
        # 将后缀改为 jpg
        new_file_name = os.path.splitext(file_name)[0] + '.jpg'
        # 拼接新的相对路径
        new_abs_path = os.path.join(img_path, new_file_name)

        # 移动文件
        try:
            shutil.copy(new_abs_path, mv_to_path)
            shutil.copy(xml_path, mv_to_path)
            print(f"Moved: {new_abs_path} to {mv_to_path}")
        except FileNotFoundError:
            print(f"File not found: {new_abs_path}")
        except Exception as e:
            print(f"Error moving file: {e}")

def statistic_image_label_size(size_statistics):
    count = 0
    total_count = len(size_statistics)
    last_key = None
    for i in size_statistics:
        if count == 0:
            count = 1
            last_key = i
            continue
        size_statistics[i] = size_statistics[i] + size_statistics[last_key]
        last_key = i
    print(size_statistics)


def rewrite_bbox(xml_folder_path):
    # 遍历文件夹中的所有 XML 文件
    for filename in os.listdir(xml_folder_path):
        if filename.endswith('.xml'):
            # 构建 XML 文件的完整路径
            xml_file_path = os.path.join(xml_folder_path, filename)
            # 解析 XML 文件
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            img_size = root.findall('size')
            img_w, img_h = int(img_size[0].find('width').text), int(img_size[0].find('height').text)
            # 遍历所有对象
            for obj in root.findall('object'):
                # 获取边界框坐标
                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)

                # 计算面积
                area = (xmax - xmin) * (ymax - ymin)

                # 如果面积小于 900，修改名称
                if area < img_w * img_h * target_limit:
                    name = obj.find('name').text
                    obj.find('name').text = f'tiny_{name}'

            # 保存修改后的 XML 文件
            tree.write(xml_file_path)

# 使用示例
# xml路径
xml_path = '/media/zhd/data/数据/反光背心和反光带数据/反光背心数据过滤_v2_33000_10700/labels/train'
# 图像路径
img_path = '/media/zhd/data/数据/反光背心和反光带数据/反光背心数据过滤_v2_33000_10700/images/train'
#图像临时移动路径
img_mv_to_path = '/media/zhd/data/数据/反光背心和反光带数据/反光背心数据过滤_v2_33000_10700/images/tmp'
os.makedirs(img_mv_to_path, exist_ok=True)

#基于1440p图像，给出限制比例为：像素面积小于900的目标不需要标注。其余尺寸图像依据此比例变化调整。
target_limit = 900 / (2560 * 1440)

size_statistics, tiny_obj_path = count_bbox_sizes(xml_path)
mv_tiny_obj_img(tiny_obj_path, img_path, img_mv_to_path)
rewrite_bbox(img_mv_to_path)


