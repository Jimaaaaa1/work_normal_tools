import os
import shutil

# 文件夹路径
folder_A = '/media/zhd/data/数据/起重检测数据/v6/images/val'
folder_B = '/media/zhd/data/数据/起重检测数据/v6/labels/val'
folder_C = '/media/zhd/data/数据/起重检测数据/v6/labels/xml'

# 确保C文件夹存在
os.makedirs(folder_C, exist_ok=True)

# 获取A文件夹中的所有图片文件名
images_A = set(os.listdir(folder_A))

# 遍历B文件夹中的图片
for filename in os.listdir(folder_B):
    if filename in images_A:
        # 如果B文件夹中有和A文件夹相同名称的图片，将其复制到C文件夹
        shutil.move(os.path.join(folder_B, filename), os.path.join(folder_C, filename))

print("复制完成")
