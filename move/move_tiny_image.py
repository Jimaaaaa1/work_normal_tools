import os
import shutil
from PIL import Image

# 源文件夹和目标文件夹路径
source_folder = '/media/zhd/data/数据/起重检测数据/v2=v1+数据过滤/images/train'  # 替换为你的源文件夹路径
target_folder = '/home/zhd/Downloads/爬取数据/tiny'  # 替换为你的目标文件夹路径

# 确保目标文件夹存在
os.makedirs(target_folder, exist_ok=True)

# 遍历源文件夹中的所有文件
count = 0
for filename in os.listdir(source_folder):
    file_path = os.path.join(source_folder, filename)

    # 检查是否是文件
    if os.path.isfile(file_path):
        try:
            with Image.open(file_path) as img:
                width, height = img.size

                # 检查宽或长是否小于300像素
                if width * height < 700 * 700:
                    # 移动文件到目标文件夹
                    count += 1
                    #shutil.move(file_path, os.path.join(target_folder, filename))
                    #print(f"Moved: {filename}")
                    print(count)
        except Exception as e:
            print(f"Could not process {filename}: {e}")
