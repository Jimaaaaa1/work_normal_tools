import os
import xml.etree.ElementTree as ET
import shutil


def modify_xml_label(file_path, old_label, new_label):
    # 解析 XML 文件
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 遍历所有 <object> 标签
    for obj in root.findall('object'):
        name = obj.find('name')
        if name is not None and name.text == old_label:
            shutil.copy(file_path, "/media/zhd/data/数据/反光背心和反光带数据/人员数据/人员数据_dl/xml/fgbx_unique_xml")
            name.text = new_label

    # 保存修改后的 XML 文件
    tree.write(file_path, encoding='utf-8', xml_declaration=True)


def process_folder(folder_path, old_label, new_label):
    # 遍历文件夹中的所有 XML 文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xml'):
            file_path = os.path.join(folder_path, file_name)
            modify_xml_label(file_path, old_label, new_label)


if __name__ == '__main__':
    # 替换下面的路径为你自己的文件夹路径
    folder_path = '/media/zhd/data/数据/反光背心和反光带数据/人员数据/人员数据_dl/xml/labels_xml'
    old_label = 'fgbx_unique'
    new_label = 'fgbx'

    process_folder(folder_path, old_label, new_label)
