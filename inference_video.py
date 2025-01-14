import cv2
from ultralytics import YOLO
import os

# 初始化YOLO模型
model = YOLO('/media/zhd/data/组件/反光背心检测组件-20240710/yolov8_local/runs/detect/train/weights/items_occupied_yolov8_20241012_v1_0.pt')

# 指定视频文件夹路径
video_folder_path = '/media/zhd/data/数据/消防通道占用数据/现场视频/ori_vedios'
output_folder_path = '/media/zhd/data/数据/消防通道占用数据/现场视频/infer_results'

# 确保输出文件夹存在
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 遍历文件夹中的所有视频文件
for video_file in os.listdir(video_folder_path):
    if video_file.endswith('.mp4'):
        video_path = os.path.join(video_folder_path, video_file)
        output_video_path = os.path.join(output_folder_path, video_file)

        # 读取视频文件
        cap = cv2.VideoCapture(video_path)

        # 获取视频的帧率和分辨率
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 创建视频写入对象
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

        count = -1
        save_results = None
        while cap.isOpened():
            ret, frame = cap.read()
            count += 1
            if count % 1 == 0:
                if not ret:
                    break
                # 使用YOLO模型进行目标检测
                results = model(frame)
                save_results = results
                # 遍历检测结果并绘制到帧上
                for result in results:
                    boxes = result.boxes
                    cls_names = result.names
                    for box in boxes:
                        cls = int(box.cls)
                        label = cls_names[cls]
                        xyxy = box.xyxy
                        x1 = int(xyxy[0][0])
                        y1 = int(xyxy[0][1])
                        x2 = int(xyxy[0][2])
                        y2 = int(xyxy[0][3])
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                # 将处理后的帧写入视频文件
                out.write(frame)
            else:
                for result in save_results:
                    boxes = result.boxes
                    cls_names = result.names
                    for box in boxes:
                        cls = int(box.cls)
                        label = cls_names[cls]
                        xyxy = box.xyxy
                        x1 = int(xyxy[0][0])
                        y1 = int(xyxy[0][1])
                        x2 = int(xyxy[0][2])
                        y2 = int(xyxy[0][3])
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                out.write(frame)

        # 释放视频文件资源
        cap.release()
        out.release()

# 关闭所有窗口
cv2.destroyAllWindows()

