#!/bin/bash
#SBATCH --job-name=bigdata-qwen72b
#SBATCH --gres=gpu:8
#SBATCH --partition=bigdata-html
MODEL_PATH="Qwen2.5-72b"

set -euo pipefail
if [ ! -d "/share" ]; then
    echo "/share is not exist"
    exit 1
fi


# 从本文件的#SBATCH --gres=gpu:<number> 获取GPU数量
GPU_CNT=$(grep -oP '#SBATCH --gres=gpu:\K\d+' $0)
GPU_CNT=$(echo "$GPU_CNT" | xargs)
GPU_CNT=$GPU_CNT LOG_LEVEL="WARN" MODEL_PATH=$MODEL_PATH DEBUG=0  apptainer exec --nv --bind /share:/share /share/share/images/ubuntu.sif  bash  do_start_72b.sh
