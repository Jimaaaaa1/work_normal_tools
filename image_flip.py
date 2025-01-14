import os
from PIL import Image
import shutil

# 指定图像文件夹路径
folder_path = '/media/zhd/data/数据/反光背心和反光带数据/20240826起所有数据/20240913/tmp'

# 遍历文件夹内的所有文件
for filename in os.listdir(folder_path):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # 支持的图像格式
        image_path = os.path.join(folder_path, filename)

        # 打开图像并进行翻转
        with Image.open(image_path) as img:
            flipped_image = img.transpose(Image.FLIP_TOP_BOTTOM)  # 左右翻转
            shutil.move(image_path, "/media/zhd/data/数据/反光背心和反光带数据/20240826起所有数据/20240913/tmp1")
            # 保存翻转后的图像
            flipped_image.save(os.path.join(folder_path, f'{filename}'))

print("图像翻转完成！")
