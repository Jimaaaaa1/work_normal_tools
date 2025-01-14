import cv2
import numpy as np
import os
import shutil

def find_duplicate_images(folder_path, threshold=0.4):
    duplicate_pairs = []
    index = 0
    for root, _, files in os.walk(folder_path):
        files.sort()
        for i in range(len(files)//2):
            index += 1
            img1_path = os.path.join(root, files[2*i])
            img2_path = os.path.join(root, files[2*i+1])

            img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

            # 使用ORB特征提取器
            orb = cv2.ORB_create()
            kp1, des1 = orb.detectAndCompute(img1, None)
            kp2, des2 = orb.detectAndCompute(img2, None)

            # 使用暴力匹配器
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)

            # 根据匹配数判断是否相似
            similarity = len(matches) / len(kp1)
            if similarity > threshold:
                duplicate_pairs.append((img1_path, img2_path))
                shutil.move(img1_path, os.path.join('/media/zhd/data/数据/反光背心和反光带数据/反光背心数据过滤/一级过滤'))
            if index % 200 == 0:
                print("index: ", index)
                print("len_dup: ", len(duplicate_pairs))
    return duplicate_pairs

folder_path = '/media/zhd/data/数据/反光背心和反光带数据/反光背心数据过滤/images/'
duplicates = find_duplicate_images(folder_path)
#
# for dup in duplicates:
#     print(f"Duplicate pair: {dup[0]} - {dup[1]}")

