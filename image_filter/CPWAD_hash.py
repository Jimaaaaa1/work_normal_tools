from imagededup.methods import PHash, CNN, DHash, WHash, AHash
import os
import sys
import shutil

from os.path import isdir, abspath, getsize, join
from os import listdir, system

sys.setrecursionlimit(30000)  # 将默认的递归深度修改为3000


def append_filename(path):
    contents = listdir(abspath(path))
    for content in contents:
        content = join(path, content)
        if isdir(content):
            append_filename(abspath(content))
        else:
            filenames.append(abspath(content))
    return filenames


def del_zero_kb_file(path):
    contents = listdir(abspath(path))
    for content in contents:
        content = join(path, content)
        if isdir(content):
            append_filename(abspath(content))
        else:
            filenames.append(abspath(content))

    for filename in filenames:
        if getsize(filename) == 0:
            system('del %s' % filename)
            print("[-] Deleting %s ..." % filename)


filenames = []

def scan_and_encode(hasher, image_dir, threshold=10):
    """
    :param hasher:
    :param image_dir:
    :param threshold: 阈值越大保留越少
    :return:
    """
    total_encodings = {}
    encodings = hasher.encode_images(image_dir)
    total_encodings.update(encodings)
    duplicates = hasher.find_duplicates(encoding_map=total_encodings, max_distance_threshold=threshold)

    return duplicates

if __name__ == '__main__':
    # 需要去重的文件目录
    image_dir = '/media/zhd/data/数据/反光背心和反光带数据/人员数据过滤/hash_12/hash_12'
    copy_to_path = '/media/zhd/data/数据/反光背心和反光带数据/人员数据过滤'
    # step1 前置检测 将像素大小为0的文件删掉
    del_zero_kb_file(image_dir)

    phasher = PHash()
    # dhasher = DHash()
    # whasher = WHash()
    # ahasher = AHash()

    single_depth = True #文件路径单层深度
    # step2 执行查重
    if single_depth:
        p_duplicates = scan_and_encode(phasher, image_dir, threshold=5)
        # d_duplicates = scan_and_encode(dhasher, image_dir, threshold=8)
        # w_duplicates = scan_and_encode(whasher, image_dir, threshold=4)
        # a_duplicates = scan_and_encode(ahasher, image_dir, threshold=2)

        # 合并所有字典
        # all_keys = set(p_duplicates) | set(d_duplicates) | set(w_duplicates) | set(a_duplicates)1082
        # duplicates = {k: p_duplicates.get(k, []) + d_duplicates.get(k, []) + w_duplicates.get(k, []) + a_duplicates.get(k, []) for k in all_keys}

        for k, v in p_duplicates.items():
            if len(v) > 0:
                # step3执行删除 p5-5618 d4-5822 w3-5320 a2-5223
                for file in v:
                    file_name_with_full_path = os.path.join(image_dir, file)
                    if os.path.exists(file_name_with_full_path):
                        shutil.move(file_name_with_full_path, copy_to_path)
    # else:
    #     image_dir_sub = os.listdir(image_dir)
    #     total_encodings = {}
    #     for sub_dir in image_dir_sub:
    #         full_tmp_dir = os.path.join(image_dir, sub_dir)
    #         print(full_tmp_dir)
    #         encodings = phasher.encode_images(full_tmp_dir)
    #         total_encodings.update(encodings)
    #     duplicates = phasher.find_duplicates(encoding_map=total_encodings)
    #     for k, v in duplicates.items():
    #         image_dir_sub = os.listdir(image_dir)
    #         if len(v) > 0:
    #             for sub_dir in image_dir_sub:
    #                 # step3执行删除
    #                 for file in v:
    #                     file_name_with_full_path = os.path.join(image_dir, sub_dir, file)
    #                     if os.path.exists(file_name_with_full_path):
    #                         os.remove(file_name_with_full_path)

