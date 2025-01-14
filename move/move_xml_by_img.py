import os
import shutil

def copy_matching_jpg(a_folder, b_folder, c_folder):
    # 获取A文件夹中所有的图片文件名
    os.makedirs(c_folder, exist_ok=True)
    a_files = os.listdir(b_folder)
    jpg_names = [os.path.splitext(file)[0] for file in a_files if file.lower().endswith(('.xml'))]

    # 遍历B文件夹及其子文件夹，查找匹配的XML文件
    for root, _, files in os.walk(a_folder):
        for file in files:
            if file.lower().endswith('.jpg'):
                jpg_path = os.path.join(root, file)
                jpg_name = os.path.splitext(file)[0]
                # 检查XML文件名是否匹配A文件夹中的图片文件名
                if jpg_name in jpg_names:
                    # 如果匹配，则复制该XML文件到C文件夹
                    try:
                        shutil.copy(jpg_path, c_folder)
                    except:
                        pass
                    # print(f"Copied {xml_path} to {c_folder}")

def copy_matching_xml(a_folder, b_folder, c_folder):
    # 获取A文件夹中所有的图片文件名
    os.makedirs(c_folder, exist_ok=True)
    a_files = os.listdir(a_folder)
    image_names = [os.path.splitext(file)[0] for file in a_files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # 遍历B文件夹及其子文件夹，查找匹配的XML文件
    for root, _, files in os.walk(b_folder):
        for file in files:
            if file.lower().endswith('.xml'):
                xml_path = os.path.join(root, file)
                xml_name = os.path.splitext(file)[0]
                #xml_name += '.jpg'
                # 检查XML文件名是否匹配A文件夹中的图片文件名
                if xml_name in image_names:
                    # 如果匹配，则复制该XML文件到C文件夹
                    try:
                        shutil.move(xml_path, c_folder)
                    except:
                        pass
                    # print(f"Copied {xml_path} to {c_folder}")

# 设置A、B、C文件夹的路径
img_folder = '/media/zhd/data/数据/反光背心和反光带数据/反光背心数据/反光背心数据过滤_v5(v2+new))(完整)/images/val'
xml_folder = '/media/zhd/data/数据/反光背心和反光带数据/反光背心数据/反光背心数据过滤_v5(v2+new))(完整)/labels_fgd/val'
copyto_folder = '/media/zhd/data/数据/反光背心和反光带数据/反光背心数据/反光背心数据过滤_v5(v2+new))(完整)/images_fgd/val'

# 调用复制匹配XML文件的函数
copy_matching_xml(img_folder, xml_folder, copyto_folder)
# copy_matching_jpg(img_folder, xml_folder, copyto_folder)
