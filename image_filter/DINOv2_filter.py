#pip install Transformers Pillow torch

import os
import torch
import torch.nn as nn
from PIL import Image
from transformers import AutoImageProcessor, AutoModel
import time
import shutil
import pickle

# 设置设备
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# 加载模型和处理器
processor = AutoImageProcessor.from_pretrained('./dinov2_base')
model = AutoModel.from_pretrained('./dinov2_base').to(device)

def extract_features(image_path):
    """提取图像特征向量"""
    image = Image.open(image_path)
    with torch.no_grad():
        inputs = processor(images=image, return_tensors="pt").to(device)
        outputs = model(**inputs)
    features = outputs.last_hidden_state.mean(dim=1)
    return features.cpu().numpy().flatten()

def compute_cosine_similarity(features1, features2):
    """计算余弦相似度"""
    cos = nn.CosineSimilarity(dim=0)
    sim = cos(torch.tensor(features1), torch.tensor(features2)).item()
    return (sim + 1) / 2  # 归一化到 [0, 1] 范围

def find_dup(features_dict, threshold):
    duplicate = {}
    image_paths = list(features_dict.keys())
    encodings = list(features_dict.values())
    img_num = len(image_paths)
    for i in range(img_num):
        img_path_A = image_paths[i]
        encoding_A = encodings[i]
        if i % 100 == 0:
            print(f"current search num/total {round((((img_num-i//2)*(i+1) / (img_num*(img_num+1)/2))), 2)}...")
        # 记录 A 与其他图片的相似度
        duplicates_for_A = []
        for j in range(i, len(image_paths)):
            if i == j:
                continue
            img_path_B = image_paths[j]
            encoding_B = encodings[j]
            similarity = compute_cosine_similarity(encoding_A, encoding_B)
            if similarity > threshold:
                duplicates_for_A.append([img_path_B, similarity])

        if duplicates_for_A:
            duplicate[img_path_A] = duplicates_for_A

    return duplicate

def mv_to_copy_path(pairs, out_path):
    os.makedirs(out_path, exist_ok=True)
    for key, value_list in pairs.items():
        for file_path, _ in value_list:
            # 构造目标文件路径
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(out_path, file_name)
            # 复制文件
            if os.path.isfile(file_path):
                shutil.move(file_path, destination_path)
            #print(f'复制 {file_path} 到 {destination_path}')

def process_images(source_dir, output_file, threshold, encoding_exist):
    image_paths = [os.path.join(source_dir, fname) for fname in os.listdir(source_dir)
                   if fname.lower().endswith(('.png', '.jpg', '.jpeg'))]
    length = len(image_paths)
    print(f"img length:{length}")
    features_dict = dict()
    index = 0
    if os.path.isfile('feature_encoding.pkl') and encoding_exist:
        with open('feature_encoding.pkl', 'rb') as f:
            features_dict = pickle.load(f)
            print("Encoding exist")
    else:
        # 提取所有图片的特征向量
        start_time = time.time()
        for image_path in image_paths:
            index += 1
            features = extract_features(image_path)
            features_dict[image_path] = features
            if index % 100 == 0:
                end_time = time.time()
                cost_time = (end_time - start_time)
                print(f"feature extraction:{index}, cost time:{round(cost_time)}")

        with open('feature_encoding.pkl', 'wb') as pickle_file:
            pickle.dump(features_dict, pickle_file)
    print("start to compute cosine similarity...")
    duplicate_pairs = find_dup(features_dict, threshold)
    print("length of duplicate pairs:", len(duplicate_pairs))
    mv_to_copy_path(duplicate_pairs, output_file)
    # 计算并保存相似度

if __name__ == '__main__':
    # 调用示例
    source_directory = '/media/zhd/data/数据/反光背心和反光带数据/反光带分类数据/人员安全带/安全带/'
    copy_to_path = '/media/zhd/data/数据/反光背心和反光带数据/反光带分类数据/人员安全带/dino_960'
    threshold = 0.960
    encoding_exist = False
    process_images(source_directory, copy_to_path, threshold, encoding_exist)
