import shutil
from PIL import Image
import imagehash
import os
import numpy as np

def find_most_similar_array(target_array, array_list):
    min_diff = float('inf')
    most_similar = None
    target_array = target_array.hash
    for array in array_list:
        array = array.hash
        diff = np.sum(target_array != array)
        if diff < min_diff:
            min_diff = diff
            most_similar = array

    return most_similar, min_diff

def find_duplicate_images(folder_path, copy_to_path, hash_size=5, diff_threshold=2):
    if not os.path.exists(copy_to_path):
        os.makedirs(copy_to_path)
    hash_dict = {}
    hash_list = []
    duplicates = []
    index = 0
    diff_num = 0
    for root, _, files in os.walk(folder_path):
        #files.sort()
        for file_name in files:
            if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                continue
            file_path = os.path.join(root, file_name)
            index = index + 1
            try:
                with Image.open(file_path) as img:
                    # 计算图像的哈希值
                    img_hash = imagehash.average_hash(img, hash_size=hash_size)
                    # 如果哈希值已经存在，则说明是重复图片
                    if img_hash in hash_dict:
                        duplicates.append((file_path, hash_dict[img_hash]))
                        #shutil.move(file_path, os.path.join('/media/zhd/data/数据/反光背心和反光带数据/人员数据过滤/一级过滤/'))
                    else:
                        hash_dict[img_hash] = file_path
                        _, diff = find_most_similar_array(img_hash, hash_list)
                        hash_list.append(img_hash)
                        if not diff < diff_threshold:
                            diff_num += 1
                            shutil.copy(file_path, os.path.join(copy_to_path))
            except Exception as e:
                #print(f"Error processing {file_path}: {str(e)}")
                pass
            if index % 1000 == 0:
                print("current: ", index)
                print("duplicate pare:", len(duplicates))
                print("diff num:", diff_num)
                print("-----------------------------------------")
    return duplicates

def find_duplicate_images_onlyhash(folder_path, copy_to_path, hash_size=5):
    if not os.path.exists(copy_to_path):
        os.makedirs(copy_to_path)
    hash_dict = {}
    duplicates = []
    index = 0
    for root, _, files in os.walk(folder_path):
        #files.sort()
        for file_name in files:
            if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                continue
            file_path = os.path.join(root, file_name)
            index = index + 1
            try:
                with Image.open(file_path) as img:
                    # 计算图像的哈希值
                    img_hash = imagehash.average_hash(img, hash_size=hash_size)
                    # 如果哈希值已经存在，则说明是重复图片
                    if img_hash in hash_dict:
                        duplicates.append((file_path, hash_dict[img_hash]))
                        #shutil.move(file_path, os.path.join('/media/zhd/data/数据/反光背心和反光带数据/人员数据过滤/一级过滤/'))
                    else:
                        hash_dict[img_hash] = file_path
                        shutil.move(file_path, os.path.join(copy_to_path))
            except Exception as e:
                #print(f"Error processing {file_path}: {str(e)}")
                pass
            if index % 1000 == 0:
                print("current: ", index)
                print("duplicate pare:", len(duplicates))
                print("-----------------------------------------")
    return duplicates

if __name__ == '__main__':
    # hash_size=5, diff_num=4,3 --->  49000-40081 = 9000 --> 776, 1962
    # hash_size=6, diff_num=4,5 --->  2890, 1944
    # hash_size=7 diff_num=9 --->  1191
    # hash_size=8 diff_num=9,6 --->  2652, 4465
    img_path = '/media/zhd/data/数据/反光背心和反光带数据/反光背心原始数据/images'
    root_copy_to_path = '/media/zhd/data/数据/反光背心和反光带数据/反光背心原始数据/'

    fine_grained_hash_1st = 8
    copy_to_path_1st = root_copy_to_path + f"hash_{fine_grained_hash_1st}"
    if not os.path.exists(copy_to_path_1st):
        duplicates = find_duplicate_images_onlyhash(img_path, copy_to_path_1st, hash_size=fine_grained_hash_1st)
        # with open(f'/media/zhd/data/数据/起重检测数据/数据过滤/duplicates_hash{fine_grained_hash_1st}.txt', 'w') as file:
        #     for item in duplicates:
        #         file.write(f"{item}\n")
    img_path = copy_to_path_1st
    print("fine-grained-1st filted finished")

    # for i in range(1):
    #     copy_to_path = root_copy_to_path + f"hash_3_" + f"diff_0"
    #     duplicates = find_duplicate_images_onlyhash(img_path, copy_to_path, hash_size=3)
    #     #duplicates = find_duplicate_images(img_path, copy_to_path, hash_size=4, diff_threshold=2)

    # fine_grained_hash_2nd = 6
    # copy_to_path_2nd = root_copy_to_path + f"hash_{fine_grained_hash_2nd}"
    # if not os.path.exists(copy_to_path_2nd):
    #     duplicates = find_duplicate_images_onlyhash(img_path, copy_to_path_2nd, hash_size=fine_grained_hash_2nd)
    #     with open(f'/media/zhd/data/数据/起重检测数据/数据过滤/duplicates_hash{fine_grained_hash_2nd}.txt', 'w') as file:
    #         for item in duplicates:
    #             file.write(f"{item}\n")
    # img_path = copy_to_path_2nd
    # print("fine-grained-2nd filted finished")
    #
    # fine_grained_hash_3rd = 4
    # copy_to_path_3rd = root_copy_to_path + f"hash_{fine_grained_hash_3rd}"
    # if not os.path.exists(copy_to_path_3rd):
    #     duplicates = find_duplicate_images_onlyhash(img_path, copy_to_path_3rd, hash_size=fine_grained_hash_3rd)
    #     with open(f'/media/zhd/data/数据/起重检测数据/数据过滤/duplicates_hash{fine_grained_hash_3rd}.txt', 'w') as file:
    #         for item in duplicates:
    #             file.write(f"{item}\n")
    # img_path = copy_to_path_3rd
    # print("fine-grained-3rd filted finished")1013

    # for i in range(12, 13):
    #     #j_range = (i-4)**2
    #     for j in range(20, 21):
    #         print("#############################################################")
    #         print(f"hash:{i}, diff:{j}")
    #         copy_to_path = root_copy_to_path + f"hash_{i}_" + f"diff_{j}"
    #         duplicates = find_duplicate_images(img_path, copy_to_path, hash_size=i, diff_threshold=j)





