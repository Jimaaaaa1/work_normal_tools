from PIL import Image
import os

# 图片文件夹路径
folder_path = '/media/zhd/data/数据/起重检测数据/原始数据集/240715起所有新增数据/20241213/images/tmp'

# 遍历文件夹中的所有图片文件
for filename in os.listdir(folder_path):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
        file_path = os.path.join(folder_path, filename)

        # 打开图片
        with Image.open(file_path) as img:
            # 旋转图片90度
            rotated_img = img.rotate(270, expand=True)  # expand=True 保证旋转后图片的尺寸能够自动调整

            # 保存旋转后的图片（覆盖原文件）
            rotated_img.save(file_path)

print("所有图片已旋转并保存！")
