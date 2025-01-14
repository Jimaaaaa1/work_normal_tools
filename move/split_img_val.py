import os
import random
import shutil


def create_validation_set(data_folder, validation_folder, validation_percent=10):
    # 创建验证集目标文件夹，如果不存在的话
    if not os.path.exists(validation_folder):
        os.makedirs(validation_folder)

    # 获取数据文件夹中所有文件列表
    files = os.listdir(data_folder)

    # 计算需要选择的文件数量
    num_validation_files = int(len(files) * validation_percent / 100)

    # 随机选择验证集文件
    validation_files = random.sample(files, num_validation_files)

    # 移动验证集文件到验证集目标文件夹
    for file in validation_files:
        src_file = os.path.join(data_folder, file)
        dst_file = os.path.join(validation_folder, file)
        shutil.move(src_file, dst_file)
        #print(f'Moved {file} to {validation_folder}')


# 示例用法
data_folder = '/media/zhd/data/数据/反光背心和反光带数据/反光带分类数据/nofgbx_留着下次用'
validation_folder = '/media/zhd/data/数据/反光背心和反光带数据/反光带分类数据/3'
validation_percent = 10

create_validation_set(data_folder, validation_folder, validation_percent)
