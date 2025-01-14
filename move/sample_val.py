import os
import random
import shutil


def randomly_select_files(source_folder, dest_folder, file_type, percentage):
    # 获取源文件夹中指定类型的文件列表
    files_all = os.listdir(source_folder)
    files = []
    for f in files_all:
        if f.lower().endswith(file_type):
            files.append(f)
    #files = [f for f in files_all if f.lower().endswith(file_type.lower())]

    # 计算要选择的文件数量
    num_files_to_select = int(len(files) * (percentage / 100.0))

    # 随机选择文件
    selected_files = random.sample(files, num_files_to_select)

    # 复制选中的文件到目标文件夹
    for file in selected_files:
        source_path = os.path.join(source_folder, file)
        dest_path = os.path.join(dest_folder, file)
        shutil.move(source_path, dest_path)
        print(f"Copied {source_path} to {dest_path}")


def copy_corresponding_xml(source_folder, xml_folder, dest_folder):
    # 获取已选择的文件列表
    selected_files = os.listdir(source_folder)

    # 遍历XML文件夹及其子文件夹，查找对应的XML文件
    for root, _, files in os.walk(xml_folder):
        for file in files:
            if file.lower().endswith('.xml'):
                xml_name = os.path.splitext(file)[0] + '.jpg'
                if xml_name in selected_files:
                    xml_path = os.path.join(root, file)
                    dest_path = os.path.join(dest_folder, file)
                    shutil.move(xml_path, dest_path)
                    print(f"Copied {xml_path} to {dest_path}")


# 设置A、B、C、D文件夹的路径和抽取百分比
a_folder = '/media/zhd/data/数据/反光背心和反光带数据/v3=v2+0826-09/images/train/'
b_folder = '/media/zhd/data/数据/反光背心和反光带数据/v3=v2+0826-09/labels/train/'
c_folder = '/media/zhd/data/数据/反光背心和反光带数据/v3=v2+0826-09/images/val/'
d_folder = '/media/zhd/data/数据/反光背心和反光带数据/v3=v2+0826-09/labels/val/'
percentage_to_select = 10  # 选择百分之10的文件

# 抽取百分之10的图片到C文件夹
randomly_select_files(a_folder, c_folder, ('.png', '.jpg', '.jpeg'), percentage_to_select)

# 将C对应的XML文件从B文件夹抽出到D文件夹
copy_corresponding_xml(c_folder, b_folder, d_folder)
