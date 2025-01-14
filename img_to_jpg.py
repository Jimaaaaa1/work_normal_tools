import os
from PIL import Image


def convert_images_to_jpg_and_remove_original(folder_path):
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"文件夹 '{folder_path}' 不存在。")
        return

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 获取文件的完整路径
        file_path = os.path.join(folder_path, filename)

        # 检查是否为文件而非文件夹
        if os.path.isfile(file_path):
            try:
                # 打开图像文件
                with Image.open(file_path) as img:
                    # 获取文件名和扩展名
                    name, ext = os.path.splitext(filename)

                    # 只处理 PNG 和 JPEG 文件
                    if ext.lower() in ['.png', '.jpeg', '.jpg']:
                        # 转换为 JPG 格式
                        jpg_file_path = os.path.join(folder_path, f"{name}.jpg")
                        img.convert('RGB').save(jpg_file_path, 'JPEG')
                        print(f"已转换: {file_path} -> {jpg_file_path}")

                        # 删除原文件
                        if ext.lower() == '.jpg':
                            continue
                        else:
                            os.remove(file_path)
                        print(f"已删除原文件: {file_path}")
                    else:
                        print(f"跳过: {file_path} (不支持的格式)")
            except Exception as e:
                print(f"无法转换 '{filename}': {e}")


# 替换为你的文件夹路径
folder_path = '/media/zhd/data/数据/起重检测数据/原始数据集/240715起所有新增数据/20241218/漏报'
convert_images_to_jpg_and_remove_original(folder_path)
