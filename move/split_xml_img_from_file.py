import os
import shutil

def copy_files(source_dir, target_jpg, target_xml):
    # 创建目标文件夹（如果不存在）
    if not os.path.exists(target_jpg):
        os.makedirs(target_jpg)
    if not os.path.exists(target_xml):
        os.makedirs(target_xml)

    # 遍历源文件夹
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # 检查文件扩展名是jpg或xml
            if file.lower().endswith(('.jpg', '.jpeg', '.JPEG', '.JPG')):
                source_file_path = os.path.join(root, file)
                # 构造目标文件路径
                target_file_path = os.path.join(target_jpg, file)
                try:
                    # 复制文件到目标文件夹
                    shutil.move(source_file_path, target_file_path)
                    #print(f"Copied {source_file_path} to {target_file_path}")
                except IOError as e:
                    pass
                    #print(f"Unable to copy file {source_file_path}: {e}")
            elif file.lower().endswith('.xml'):
                source_file_path = os.path.join(root, file)
                # 构造目标文件路径
                target_file_path = os.path.join(target_xml, file)
                try:
                    # 复制文件到目标文件夹
                    shutil.move(source_file_path, target_file_path)
                    #print(f"Copied {source_file_path} to {target_file_path}")
                except IOError as e:
                    pass
                    #print(f"Unable to copy file {source_file_path}: {e}")

# 指定源文件夹和目标文件夹路径
source_folder = '/media/zhd/data/数据/起重检测数据/原始数据集/240715起所有新增数据/20241218/起重吊装'
target_folder_jpg = '/media/zhd/data/数据/起重检测数据/原始数据集/240715起所有新增数据/20241218/images/train'
target_folder_xml = '/media/zhd/data/数据/起重检测数据/原始数据集/240715起所有新增数据/20241218/labels/train'

# 调用函数复制文件
copy_files(source_folder, target_folder_jpg, target_folder_xml)
