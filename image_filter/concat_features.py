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


with open('/media/zhd/data/工具/image_filter/ex_blue.pkl', 'rb') as f:
    features_dict_1 = pickle.load(f)

with open('/media/zhd/data/项目/其他项目/工装-关键点匹配/sam_and_cluster/sam2/features_encoding/helmets/helmets_blue.pkl', 'rb') as f:
    features_dict_2 = pickle.load(f)


merged_dict = {**features_dict_1, **features_dict_2}

with open('helmets_blue.pkl', 'wb') as pickle_file:
    pickle.dump(merged_dict, pickle_file)

