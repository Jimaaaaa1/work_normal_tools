from imagededup.methods import CNN
from imagededup.utils import CustomModel
from imagededup.utils.models import ViT
import os
import shutil
import nmslib
import numpy as np
import json
import pickle

def retrieve_neighbours_one_file(neighbours_onefile, onefile_matrix_row_index, sim_thresh, all_filenames):
    # gets duplicates for one file
    self_retrived_file_pos = np.where(neighbours_onefile[0] == onefile_matrix_row_index)  # Avoid self retrieval
    neighbours_onefile_files = np.delete(neighbours_onefile[0], self_retrived_file_pos)
    neighbours_onefile_sims = np.delete(neighbours_onefile[1], self_retrived_file_pos)

    sim_neighbors = 1 - neighbours_onefile_sims  # convert distance to similarity
    thresh_sims = sim_neighbors[np.where(sim_neighbors >= sim_thresh)]
    thresh_neighbours = neighbours_onefile_files[np.where(sim_neighbors >= sim_thresh)]
    thresh_neighbours_filenames = [all_filenames[i] for i in thresh_neighbours]
    dups = list(zip(thresh_neighbours_filenames, thresh_sims))
    return dups

def mv_dupl(duplicates, image_limit, image_dir, copy_to_path):
    os.makedirs(copy_to_path, exist_ok=True)
    poped_keys = []
    if image_limit:
        for k, v in duplicates.items():
            if k in poped_keys:
                continue
            else:
                if len(v) > 0:
                    # step3执行删除
                    for file in v:
                        file_name_with_full_path = os.path.join(image_dir, file[0])
                        if os.path.exists(file_name_with_full_path):
                            shutil.move(file_name_with_full_path, copy_to_path)
                            poped_keys.append(file[0])
                            # shutil.copy(file_name_with_full_path, copy_to_path)
    else:
        for k, v in duplicates.items():
            if k in poped_keys:
                continue
            else:
                if len(v) > 0:
                    # step3执行删除
                    for file in v:
                        file_name_with_full_path = os.path.join(image_dir, file)
                        if os.path.exists(file_name_with_full_path):
                            shutil.move(file_name_with_full_path, copy_to_path)
                            poped_keys.append(file)
                            # shutil.copy(file_name_with_full_path, copy_to_path)

def find_dupl(encodings, image_limit, min_sim_threshold):
    if image_limit:
        data = np.array(list(encodings.values()))
        index = nmslib.init(method='hnsw', space='cosinesimil')
        index.addDataPointBatch(data)
        # Set index parameters
        M = 40  # Max links per node
        efConstruction = 40  # Size of the dynamic list used during construction. A larger value means a better quality index, but increases build time. Should be an integer value between 1 and the size of the dataset.
        num_threads = 4
        index_time_params = {'M': M, 'indexThreadQty': num_threads, 'efConstruction': efConstruction,
                             'post': 0}  # 'post': postprocessing
        index.createIndex(index_time_params, print_progress=True)
        K = data.shape[
            0]  # number of neigbours (setting to the size of dataset, usual practice is to specify a value such as 100 or so)
        efSearch = 50  # Size of the dynamic list used during search. Higher values lead to improved recall at the expense of longer search time. Can take values between k and the size of the dataset and may be greater or smaller than ef_construction. Typical values are 100 - 2000.
        query_time_params = {'efSearch': efSearch}
        print('Setting query-time parameters', query_time_params)
        index.setQueryTimeParams(query_time_params)
        neighbours = index.knnQueryBatch(data, k=K)
        filenames = list(encodings.keys())
        file_matrix_inds = range(data.shape[0])
        min_sim_threshold = min_sim_threshold
        res = list(map(retrieve_neighbours_one_file, neighbours, file_matrix_inds, [min_sim_threshold] * data.shape[0],
                       [filenames] * data.shape[0]))
        duplicates = dict(zip(filenames, res))
    else:
        duplicates = cnn_encoder.find_duplicates(encoding_map=encodings,
                                                 min_similarity_threshold=min_sim_threshold,
                                                 scores=False)
    return duplicates
if __name__ == '__main__':

    image_dir = '/media/zhd/data/数据/起重检测数据/原始数据集/240715起所有新增数据/原始数据/20240904/吊装'
    #重复的挪出至copy_to_path
    copy_to_path = '/media/zhd/data/数据/起重检测数据/原始数据集/240715起所有新增数据/原始数据/20240904/vit960'

    custom_config = CustomModel(name=ViT.name,
                                model=ViT(),
                                transform=ViT.transform)
    cnn_encoder = CNN(model_config=custom_config)

    if os.path.isfile('encodings_vit960.pkl'):
        with open('encodings_vit960.pkl', 'rb') as file:
            encodings = pickle.load(file)
            print("Encoding exist")
    else:
        encodings = cnn_encoder.encode_images(image_dir, recursive=True)
        # 保存字典到 JSON 文件
        with open('encodings_vit960.pkl', 'wb') as file:
            pickle.dump(encodings, file)

    image_limit = False #超过5W张图片会有bug，设置为True可以处理更大批的数据，但是分块处理以后感觉还是有点bug
    threshold = 0.950
    duplicates = find_dupl(encodings, image_limit, threshold)
    mv_dupl(duplicates, image_limit, image_dir, copy_to_path)


