import shutil

from PIL import Image
import os
import time

# 源文件夹路径
source_folder = '/home/zhd/Pictures/1'  # 替换为你的文件夹路径
target_folder = '/home/zhd/Pictures/jpg'
tmp_folder = '/home/zhd/Pictures/tmp'

# 确保目标文件夹存在
os.makedirs(target_folder, exist_ok=True)

# 遍历源文件夹中的所有文件
for filename in os.listdir(source_folder):
    if filename.lower().endswith('.webp'):
        source_file = os.path.join(source_folder, filename)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        new_filename = f"{os.path.splitext(filename)[0]}_{timestamp}.jpg"
        target_file = os.path.join(target_folder, new_filename)

        try:
            with Image.open(source_file) as img:
                rgb_img = img.convert('RGB')  # 转换为RGB模式
                rgb_img.save(target_file, 'JPEG')  # 保存为JPG格式
                print(f"Converted: {filename} to {target_file}")
                os.remove(source_file)
        except Exception as e:
            print(f"Error converting {filename}: {e}")
