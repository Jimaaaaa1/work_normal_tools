#!/bin/bash

# 设置显存占用阈值，单位为 MB
MEM_THRESHOLD=1000
# 设置检查间隔时间（秒）
CHECK_INTERVAL=30
# 训练命令
TRAIN_COMMAND="nohup python3 train_yolo11.py >train_11.log 2>&1 &"

check_gpus(){
    # 获取所有显卡的显存使用情况
    gpu_mem_usage=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
    
    # 遍历所有显卡的显存使用情况
    for used_mem in $gpu_mem_usage; do
        echo $used_mem
        if [ $used_mem -gt $MEM_THRESHOLD ]; then
            # 如果有任何一张显卡的显存使用超过阈值，返回非空闲状态
            return 1
        fi
    done
    
    # 所有显卡显存占用都低于阈值，返回空闲状态
    return 0
}

while true; do
    # 检查显卡是否空闲
    check_gpus
    # echo $?
    if [ $? -eq 0 ]; then
        echo "GPUs are idle. Starting training..."
        # 执行训练命令
        #
        sleep $CHECK_INTERVAL
        $TRAIN_COMMAND
        echo "GPUs are free."
        break
    else
        echo "GPUs are busy. Checking again in $CHECK_INTERVAL seconds..."
        sleep $CHECK_INTERVAL
    fi
done
