# 检查文件夹内jpg文件与xml文件是否一一对应
# 没有对应xml文件的jpg文件或者
# 没有对应jpg文件的xml文件
# 都将会被删除

import os
import shutil

# ------------- 改这里 -------------
# 待检查的文件夹
# 子文件夹

jpg_path = "/media/zhd/data/数据/反光背心和反光带数据/人员数据/images/val"
copy_to_path = '/media/zhd/data/数据/反光背心和反光带数据/人员数据/fgd数据/'
xml_path = "/media/zhd/data/数据/反光背心和反光带数据/人员数据/fgd数据"
for root, dirs, files in os.walk(xml_path):
    for file in files:
        if file[-4:] == '.xml':
            xml = os.path.join(root, file)
            jpg = os.path.join(jpg_path, file[:-4]+'.jpg')
            if os.path.exists(jpg):
                shutil.copy(jpg, copy_to_path)
    #     if file[-4:] == '.jpg':
    #         jpg = os.path.join(root, file)
    #         xml = os.path.join("/media/zhd/data/数据/起重检测数据/dz/images/train_labels", file[:-4]+'.xml')
    #         if not os.path.exists(xml):
    #             print(jpg)
    #             os.remove(jpg)
