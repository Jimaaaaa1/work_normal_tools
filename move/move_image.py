import os
import shutil


def move_files(source_folder, destination_folder):
    # 确保目标文件夹存在，如果不存在则创建它
    os.makedirs(destination_folder, exist_ok=True)

    # 获取源文件夹中的所有文件和子文件夹
    files = os.listdir(source_folder)

    for file_name in files:
        # 构建文件的完整路径
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)

        # 判断是否是文件
        if os.path.isfile(source_path):
            # 移动文件到目标文件夹
            shutil.move(source_path, destination_path)
            #print(f"Moved {source_path} to {destination_path}")
        #else:
            #print(f"Skipping {source_path} as it is not a file")


IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
def move_all_files(source_folder, destination_folder):
    # 确保目标文件夹存在，如果不存在则创建它
    os.makedirs(destination_folder, exist_ok=True)

    # 遍历源文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            # 获取文件的扩展名
            _, ext = os.path.splitext(file_name)
            if ext.lower() in IMAGE_EXTENSIONS:
                # 构建文件的完整路径
                source_path = os.path.join(root, file_name)
                destination_path = os.path.join(destination_folder, file_name)
                shutil.move(source_path, destination_path)

# 设置源文件夹A和目标文件夹B的路径
source_folder = '/media/zhd/data/其它/每轮提测结果/项目提测/20241119/叶巴滩监理算法测试/AI/2024-11-13/work_clothes/'
destination_folder = '/media/zhd/data/其它/每轮提测结果/项目提测/20241119/叶巴滩监理算法测试/AI/2024-11-13/1/'

# 调用函数移动文件
move_all_files(source_folder, destination_folder)
#move_files(source_folder, destination_folder)
