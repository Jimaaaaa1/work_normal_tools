import os
import time

# 设定图片文件夹路径
folder_path = r"/home/zhd/Pictures/jpg"  # 替换成你自己的文件夹路径

# 获取文件夹中的所有文件
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    # 确保是文件（不是文件夹）
    if os.path.isfile(file_path):
        # 获取文件的修改时间
        timestamp = os.path.getmtime(file_path)
        # 格式化时间，转为 YYYY-MM-DD_HH-MM-SS
        date_str = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(timestamp))

        # 获取文件扩展名
        file_extension = os.path.splitext(filename)[1]

        # 新的文件名
        new_filename = f"{date_str}_i{file_extension}"
        new_file_path = os.path.join(folder_path, new_filename)

        # 重命名文件
        os.rename(file_path, new_file_path)

        print(f"文件 '{filename}' 已重命名为 '{new_filename}'")
