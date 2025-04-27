#!/bin/bash

source /opt/conda/etc/profile.d/conda.sh
conda config --add envs_dirs /share/xuchao/.conda/envs
conda activate /share/xuchao/.conda/envs/qwen2572b-py12


PORT=11434
GPU_PER_MODEL_INSTANCE=${GPU_CNT}
MODEL_PATH=${MODEL_PATH}
LOG_LEVEL=${LOG_LEVEL}
DEBUG=${DEBUG}

WINDOW_SIZE_32K=32768
WINDOW_SIZE_128K=131072
echo "start vllm serve at $HOSTNAME, port: ${PORT}"
echo "http://${HOSTNAME}:${PORT}" >> qwen_server.log

export VLLM_ALLOW_LONG_MAX_MODEL_LEN=1  # 强制覆盖默认上下文长度配置
export USE_FLASH_ATTENTION=1   # 使用flash attention,节省显存

export VLLM_LOGGING_LEVEL=${LOG_LEVEL}  # https://docs.vllm.ai/en/latest/getting_started/examples/logging_configuration.html

if [ ${DEBUG} -eq 1 ]; then
    add_params="--no-enable-prefix-caching"
else
    add_params=""
fi

vllm serve  ${MODEL_PATH}  --tensor-parallel-size ${GPU_PER_MODEL_INSTANCE}  --gpu-memory-utilization 0.85  --max-model-len ${WINDOW_SIZE_128K} --enable-chunked-prefill  ${add_params}  --host 0.0.0.0 --port ${PORT}
echo "vllm serve started at $HOSTNAME, port: ${PORT}"
