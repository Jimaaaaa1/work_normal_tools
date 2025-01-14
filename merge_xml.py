import os
import xml.etree.ElementTree as ET

def merge_xml(file1, file2, output_file):
    """合并两个 XML 文件的内容"""
    # 解析第一个 XML 文件
    tree1 = ET.parse(file1)
    root1 = tree1.getroot()

    # 解析第二个 XML 文件
    tree2 = ET.parse(file2)
    root2 = tree2.getroot()

    # 合并两个 XML 文件的 <object> 元素
    objects2 = root2.findall('object')
    for obj in objects2:
        root1.append(obj)

    # 保存合并后的 XML 文件
    tree1.write(output_file, encoding='utf-8', xml_declaration=True)

def merge_xml_folders(folder1, folder2, output_folder):
    """合并两个文件夹中的同名 XML 文件"""
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历第一个文件夹中的文件
    for filename in os.listdir(folder1):
        if filename.endswith('.xml'):
            file1 = os.path.join(folder1, filename)
            file2 = os.path.join(folder2, filename)
            output_file = os.path.join(output_folder, filename)

            # 检查第二个文件夹中是否存在同名文件
            if os.path.exists(file2):
                print(f'Merging {filename}')
                merge_xml(file1, file2, output_file)
            else:
                # 如果第二个文件夹中没有同名文件，则将第一个文件夹中的文件复制到输出文件夹
                with open(file1, 'r', encoding='utf-8') as f:
                    content = f.read()
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)

    # 遍历第二个文件夹中的文件，处理那些第一个文件夹中没有的 XML 文件
    for filename in os.listdir(folder2):
        if filename.endswith('.xml') and not os.path.exists(os.path.join(folder1, filename)):
            file2 = os.path.join(folder2, filename)
            output_file = os.path.join(output_folder, filename)
            # 直接复制文件到输出文件夹
            with open(file2, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)



folder1 = '/media/zhd/data/数据/起重检测数据/数据过滤/images/infer_xml'
folder2 = '/media/zhd/data/数据/起重检测数据/数据过滤/labels/train'
output_folder = '/media/zhd/data/数据/起重检测数据/数据过滤/labels/merged_xml'
merge_xml_folders(folder1, folder2, output_folder)
