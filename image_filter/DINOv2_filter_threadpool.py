import os

import cv2
import torch
import torch.nn as nn
from PIL import Image
from transformers import AutoImageProcessor, AutoModel
import time
import shutil
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_features(image_path, resize=-1):
    if resize != -1:
        image = cv2.imread(image_path)
        image = cv2.resize(image, (resize, resize))
        with torch.no_grad():
            inputs = processor(images=image, return_tensors="pt").to(device)
            outputs = model(**inputs)
        features = outputs.last_hidden_state.mean(dim=1)
        return features.cpu().numpy().flatten()
    try:
        """提取图像特征向量"""
        image = Image.open(image_path)
        with torch.no_grad():
            inputs = processor(images=image, return_tensors="pt").to(device)
            outputs = model(**inputs)
        features = outputs.last_hidden_state.mean(dim=1)
        return features.cpu().numpy().flatten()
    except Exception as e:
        image = cv2.imread(image_path)
        cv2.imwrite(image_path, image)
        with torch.no_grad():
            inputs = processor(images=image, return_tensors="pt").to(device)
            outputs = model(**inputs)
        features = outputs.last_hidden_state.mean(dim=1)
        print(f"Error processing image {image_path}: {e}")
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


def cos_similarity_chunk(features_dict, batch_size=2560, threshold=0.96, target_dir='filepath'):
    os.makedirs(target_dir, exist_ok=True)
    image_paths = list(features_dict.keys())
    encodings = list(features_dict.values())
    N = len(encodings)
    moved_images = torch.zeros(N, dtype=torch.bool)

    # 分块计算余弦相似度
    for i in range(0, N, batch_size):
        # 处理从 i 到 i+batch_size 块
        i_end = min(i + batch_size, N)
        chunk1 = torch.tensor(encodings[i:i_end], dtype=torch.float32) # 当前块 (i, i_end)
        norms = chunk1.norm(p=2, dim=1, keepdim=True)
        chunk1 = chunk1 / norms

        for j in range(i, N, batch_size):
            j_end = min(j + batch_size, N)
            chunk2 = torch.tensor(encodings[j:j_end], dtype=torch.float32) # 当前块 (j, j_end)
            norms = chunk2.norm(p=2, dim=1, keepdim=True)
            chunk2 = chunk2 / norms

            # 计算当前两个块之间的余弦相似度
            cosine_sim_chunk = torch.mm(chunk1, chunk2.t())
            cosine_sim_chunk = (cosine_sim_chunk + 1) / 2

            base_i_index = i
            base_j_index = j
            mask = cosine_sim_chunk > threshold
            indices = torch.nonzero(mask)
            for k, v in indices:
                k = k.item()
                v = v.item()
                if i == j:
                    if k >= v:
                        continue
                else:
                    if k > v:
                        continue
                if moved_images[k + base_i_index] == True:
                    continue
                if moved_images[v + base_j_index] == False:
                    img_v_path = image_paths[v + base_j_index]
                    try:
                        #找相同
                        # if os.path.basename(img_v_path) == '图片1.png':
                        #     print(img_v_path, image_paths[k + base_i_index])
                        shutil.move(img_v_path, os.path.join(target_dir, os.path.basename(img_v_path)))
                    except Exception as e:
                        print(f"Error processing image {img_v_path}: {e}")
                    moved_images[v + base_j_index] = True

    # 这种计算余弦相似度的方式太占内存，暂时不用
    # cosine_sim_matrix = torch.mm(encodings, encodings.t())
    # cosine_sim_matrix = (cosine_sim_matrix + 1) / 2

    print("Length of duplicate_pairs:", int(moved_images.sum()))
    return 0

def move_similar_images(cosine_sim_matrix, image_paths, threshold=0.96, target_dir='filepath'):
    # 确保目标文件夹存在
    os.makedirs(target_dir, exist_ok=True)
    # 遍历相似度矩阵中的每对图片
    N = cosine_sim_matrix.size(0)
    moved_images = set()  # 用于记录已经移动的图片

    for i in range(N):
        if i in moved_images:
            continue
        for j in range(i + 1, N):
            if cosine_sim_matrix[i, j] > threshold:
                img_i_path = image_paths[i]
                img_j_path = image_paths[j]

                if img_j_path not in moved_images:
                    shutil.move(img_j_path, os.path.join(target_dir, os.path.basename(img_j_path)))
                    moved_images.add(j)
                    #print(f"Moved {img_j_path} to {target_dir}")
    print("Length of duplicate_pairs:", len(moved_images))

def mv_to_copy_path(pairs, out_path):
    os.makedirs(out_path, exist_ok=True)
    for key, value_list in pairs.items():
        for file_path, _ in value_list:
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(out_path, file_name)
            if os.path.isfile(file_path):
                shutil.move(file_path, destination_path)


def process_images(source_dir, output_file, threshold, encoding_exist, batch_size=2560, in_chunk=True, only_extract_features=False, resize=-1):
    image_paths = [os.path.join(source_dir, fname) for fname in os.listdir(source_dir)
                   if fname.lower().endswith(('.png', '.jpg', '.jpeg'))]

    print(f"img length: {len(image_paths)}")
    features_dict = dict()

    if os.path.isfile('feature_encoding.pkl') and encoding_exist:
        with open('feature_encoding.pkl', 'rb') as f:
            features_dict = pickle.load(f)
            print("Encoding exists")
    else:
        # 提取所有图片的特征向量
        with ThreadPoolExecutor(max_workers=8) as executor:
            start_time = time.time()
            index = 0
            future_to_image = {executor.submit(extract_features, image_path, resize): image_path for image_path in image_paths}
            for future in as_completed(future_to_image):
                index += 1
                features = future.result()
                image_path = future_to_image[future]
                features_dict[image_path] = features
                if index % 100 == 0:
                    end_time = time.time()
                    cost_time = (end_time - start_time)
                    print(f"feature extraction:{index}, cost time:{round(cost_time)}")
                # print(f"Extracted features for {image_path}")

        with open('feature_encoding.pkl', 'wb') as pickle_file:
            pickle.dump(features_dict, pickle_file)
        with open('ex_blue.pkl', 'wb') as pickle_file:
            pickle.dump(features_dict, pickle_file)

    if only_extract_features:
        return 0

    print("Start to compute cosine similarity...")
    if in_chunk:
        Finished = cos_similarity_chunk(features_dict, batch_size, threshold, output_file)
        print("Finished status:", Finished)
    else:
        duplicate_pairs = find_dup(features_dict, threshold)
        print("Length of duplicate_pairs:", len(duplicate_pairs))
        mv_to_copy_path(duplicate_pairs, output_file)


# 设置设备
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# 加载模型和处理器
processor = AutoImageProcessor.from_pretrained('./dinov2_base')
model = AutoModel.from_pretrained('./dinov2_base').to(device)

if __name__ == '__main__':
    # 调用示例
    source_directory = '/media/zhd/data/数据/反光背心和反光带数据/反光带分类数据/反光带分类数据_v2/train/3/nofgbx'
    dst_path = source_directory.split('/')
    copy_to_path = "/".join(dst_path[:-1])
    threshold = 0.90
    copy_to_path += '/dino' + str(threshold)

    encoding_exist = True
    only_extract_features = False
    process_images(source_directory, copy_to_path, threshold, encoding_exist, batch_size=12800, in_chunk=True, only_extract_features=only_extract_features, resize=-1)

    print("done")
