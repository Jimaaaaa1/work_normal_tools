import os
import xml.etree.ElementTree as ET

# 文件夹路径
folder = '/media/zhd/data/数据/反光背心和反光带数据/反光背心数据/反光背心数据过滤_v5(v2+new))(完整)/labels_fgd_nofgd/val'

# 遍历文件夹中的所有XML文件
for filename in os.listdir(folder):
    if filename.endswith('.xml'):
        file_path = os.path.join(folder, filename)

        # 解析XML文件
        tree = ET.parse(file_path)
        root = tree.getroot()

        # 遍历所有object标签，修改name标签
        for obj in root.findall('object'):
            name_elem = obj.find('name')
            if name_elem is not None:
                if name_elem.text == 'fgd':
                    name_elem.text = 'fgd'
                elif name_elem.text == 'fgbx':
                    name_elem.text = 'nofgd'
                elif name_elem.text == 'nofgbx':
                    name_elem.text = 'nofgd'
                elif name_elem.text == 'fgbx_unique':
                    name_elem.text == 'nofgd'

        # 保存修改后的XML文件
        tree.write(file_path)

print("所有XML文件已修改完成")
