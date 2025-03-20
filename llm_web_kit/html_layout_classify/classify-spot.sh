#!/bin/bash

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


# 函数：获取当前用户所有处于PD状态的任务数量
get_pd_count() {
    squeue -u "$USER" -t PD -h |grep spot | wc -l
}

# 定义一个函数来计算 SPOT_USED 的总和
calculate_total_spot_used() {
    # 执行 svp list 并获取输出
    local svp_output=$(svp list)

    # 使用 awk 解析并计算 SPOT_USED 列的总和
    local total_spot_used=$(echo "$svp_output" | awk '
    NR == 1 {next} # 跳过标题行
    {
        sum += $6  # 假设 SPOT_USED 是第6列
    }
    END {
        print sum
    }')

    # 返回结果
    echo $total_spot_used
}

calculate_total_reserved_idle() {
    # 执行 svp list 并获取输出
    local svp_output=$(svp list)

    #总和
    local total_reserved_idle=$(echo "$svp_output" | awk '
    NR == 1 {next}
    {
        sum += $5
    }
    END {
        print sum
    }')
    # 返回结果
    echo $total_reserved_idle
}

#######################################################################################
# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --partation)
            PARTATION="$2"
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
        --server-addr)
            SERVER_ADDR="$2"
            shift 2
            ;;
        --result-save-dir)
            RESULT_SAVE_DIR="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

MAX_PENDING_JOBS=10 # 用户pending任务数量，不能超过这个值
MAX_JOBS=1000 # 用户最大提交任务数量
MY_NAME="${USER}" # 用户名

MY_HOME=$(echo $HOME)
SLURM_LOG_DIR=${MY_HOME}/slum-logs/${TAG}
# 创建日志目录（如果不存在）
mkdir -p ${SLURM_LOG_DIR}/logs
mkdir -p ${SLURM_LOG_DIR}/error
export SLURM_SUBMIT_DIR=${SLURM_LOG_DIR}
export LLM_WEB_KIT_CFG_PATH=/share/xuchao/.llm-web-kit-pageclassify.jsonc
TASK_NUM="${TASK_NUM:-1}"  # Default to 1 if not provided
DEBUG="${DEBUG:-0}"

# Check required arguments
if [ -z "$PARTATION" ] || [ -z "$TAG" ]; then
    echo "Usage: $0 --partation <partition_name> --tag <tag_name>"
    exit 1
fi

# 核心思路是只要不超过最大的pending任务数量，就一直提交任务
while true
do
    for partation in "${PARTATION[@]}"; do
        PD_COUNT=$(get_pd_count)
        spot_count=$(squeue -u ${MY_NAME}  | grep -i spot |wc -l)

        if [ "$PD_COUNT" -lt "$MAX_PENDING_JOBS" ] && [ $spot_count -lt $MAX_JOBS ]; then
            # 如果PD任务数小于最大限制，则提交新任务
            if [ $DEBUG -eq 1 ]; then
                LOG_LEVEL=ERROR srun -p ${partation} --quotatype=spot --output=${SLURM_LOG_DIR}/logs/output_%j.out --export=ALL  --error=${SLURM_LOG_DIR}/error/error_%j.err -N 1 -n${TASK_NUM} --gres=gpu:1   python main.py  ${SERVER_ADDR} --result-save-dir ${RESULT_SAVE_DIR}
            else
                LOG_LEVEL=ERROR srun -p ${partation} --quotatype=spot --output=${SLURM_LOG_DIR}/logs/output_%j.out --export=ALL  --error=${SLURM_LOG_DIR}/error/error_%j.err -N 1 -n ${TASK_NUM} --gres=gpu:1 --async  python main.py  ${SERVER_ADDR} --result-save-dir ${RESULT_SAVE_DIR}
            fi
            echo "use ${partation} submit job succ, submit next job now..."
            rm batchscript* 2>/dev/null
        fi
        break
    done # for
    sleep 20
done # while
