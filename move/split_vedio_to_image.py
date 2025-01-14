import cv2
import os

# 输入文件夹路径和输出图片文件夹路径
input_folder = '/home/zhd/Downloads/1/室外大屏3_20241224170413'
output_folder = '/home/zhd/Downloads/1/image'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for video_file in os.listdir(input_folder):
    if video_file.endswith('.mp4'):  # 只处理mp4格式的视频
        video_path = os.path.join(input_folder, video_file)
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = 2 * int(fps)  # 每N秒抽取一帧

        count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if count % frame_interval == 0:
                output_image_path = os.path.join(output_folder, f"{video_file[:-4]}_frame{count}.jpg")
                cv2.imwrite(output_image_path, frame)
            count += 1

        cap.release()
