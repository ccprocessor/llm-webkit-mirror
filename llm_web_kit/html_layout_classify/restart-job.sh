#!/bin/bash

# 循环执行scancel命令直到其返回值为0
while true; do
    scancel -u $USER
    # 检查scancel命令的返回值
    if [ $? -eq 0 ]; then
        echo "所有作业已被取消或没有作业需要取消。"
        break
    else
        echo "继续尝试取消作业..."
    fi
    # 等待一段时间再次尝试，避免无限快速循环
    sleep 2
done

# 循环等到squeue --me 为0
# 初始化行数
line_count=1

# 循环执行，直到没有找到包含 'batchscript' 的作业
while [ "$line_count" -ne 0 ]; do
    # 执行squeue命令并通过grep过滤，然后计算行数
    line_count=$(squeue --me | grep -c batchscript)

    if [ "$line_count" -ne 0 ]; then
        echo "当前作业总数为: $line_count， 等待完全停止..."
        # 等待一段时间后再次检查，比如等待30秒
        sleep 30
    fi

done

echo "所有作业均已经停止"
