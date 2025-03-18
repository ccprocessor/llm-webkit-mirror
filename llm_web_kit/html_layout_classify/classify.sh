#! /bin/bash

command -v proxyoff >/dev/null 2>&1 && proxyoff
command -v proxy_off >/dev/null 2>&1 && proxy_off

function count_used_gpus(){
    all_jobs=`squeue --me -p $1`

    gpu_num=0
    for name in $all_jobs
    do
        if [ "$(echo $name | grep "gpu:")" != "" ];then
            num="${name//gpu:/}"
            gpu_num=$((($gpu_num+$num)))
        fi
    done
    echo $gpu_num
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --partation)
            PARTATION="$2"
            shift 2
            ;;
        --max-job)
            MAX_JOB_TOTAL="$2"
            shift 2
            ;;
        --tag)
            TAG="$2"
            shift 2
            ;;
        --task-num)
            TASK_NUM="$2"
            shift 2
            ;;
        --debug)
            DEBUG=1
            shift 1
            ;;
        --result-save-dir)
            RESULT_SAVE_DIR="$2"
            shift 2
            ;;
        --server-addr)
            SERVER_ADDR="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done


MY_HOME=$(echo $HOME)
MY_NAME="${USER}" # 用户名
SLURM_LOG_DIR=${MY_HOME}/slum-logs/${TAG}
# 创建日志目录（如果不存在）
mkdir -p ${SLURM_LOG_DIR}/logs
mkdir -p ${SLURM_LOG_DIR}/error
export SLURM_SUBMIT_DIR=${SLURM_LOG_DIR}
export LLM_WEB_KIT_CFG_PATH=/share/${MY_NAME}/.llm-web-kit-pageclassify.jsonc
TASK_NUM="${TASK_NUM:-1}"  # Default to 1 if not provided
DEBUG="${DEBUG:-0}"
SERVER_ADDR="${SERVER_ADDR:-http://127.0.0.1:5000}"
PYTHON=/share/${MY_NAME}/.conda/envs/webkitdev/bin/python


# Check required arguments
if [ -z "$PARTATION" ] || [ -z "$MAX_JOB_TOTAL" ] || [ -z "$TAG" ]; then
    echo "Usage: $0 --partation <partition_name> --max-job <max_job_count> --tag <tag_name> --debug <debug_mode>"
    exit 1
fi


submited_job_num=0 # 成功提交的任务数

while [ $submited_job_num -lt $MAX_JOB_TOTAL ]
do
    used_gpu=($(count_used_gpus $PARTATION))  # 分区中自己已使用的GPU数
    avai_gpu=$(svp list -p $PARTATION|grep $PARTATION | awk '{print $5}')  # 分区中可用的GPU数
    echo -e "check partation $PARTATION \n used_gpu: $used_gpu\n avai_gpu: $avai_gpu"

    if [ $avai_gpu -gt 0 ]; then
        # 提交一个任务，睡眠
        if [ $DEBUG -eq 1 ]; then
            LOG_LEVEL=INFO  srun -p ${PARTATION} --output=${SLURM_LOG_DIR}/logs/output_%j.out --export=ALL  --error=${SLURM_LOG_DIR}/error/error_%j.err  --gres=gpu:1 -N 1 -n ${TASK_NUM}  ${PYTHON} main.py --server-addr ${SERVER_ADDR} --result-save-dir ${RESULT_SAVE_DIR}
        else

            LOG_LEVEL=ERROR  srun -p ${PARTATION} --output=${SLURM_LOG_DIR}/logs/output_%j.out --export=ALL --error=${SLURM_LOG_DIR}/error/error_%j.err  --gres=gpu:1 --async -N 1 -n ${TASK_NUM}  ${PYTHON}  main.py --server-addr ${SERVER_ADDR} --result-save-dir ${RESULT_SAVE_DIR}
        fi
        # TODO 判断任务是否提交成功
        submited_job_num=$((submited_job_num+1))
        sleep 2
        echo "use ${PARTATION} submit job succ, submit next job now..."
        rm batchscript* 2>/dev/null
    else
        echo "skip ${PARTATION}, used_GPU = ${used_gpu}, no available GPU"
        sleep 2
    fi

done # while

echo "任务提交完成"
