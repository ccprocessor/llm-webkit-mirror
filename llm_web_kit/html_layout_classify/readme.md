# html layout classify layout分类

## 环境

配置 .xinghe.yaml

配置 .llm_web_kit.jsonc

## 入参

layout_sample_dir: 一个本地的目录，内含多个jsonl文件，每个文件的结构如下：

| 字段      | 类型   | 描述                         | 是否必须 |
| --------- | ------ | ---------------------------- | -------- |
| layout_id | string | layout id                    | 是       |
| url       | string | 数据url                      | 是       |
| simp_html | string | html原数据经过简化处理的html | 是       |

layout_classify_dir：分类结果的保存目录。输出的jsonl文件，每个文件的结构如下：

| 字段          | 类型   | 描述                                                            | 是否必须 |
| ------------- | ------ | --------------------------------------------------------------- | -------- |
| url_list      | list   | layout id 对应的url                                             | 是       |
| layout_id     | string | layout id                                                       | 是       |
| page_type     | string | layout_id 经过分类之后的分类结果（'other', 'article', 'forum'） | 是       |
| max_pred_prod | float  | 分类模型的分类可靠度                                            | 是       |
| version       | string | 模型版本                                                        | 是       |

## 执行步骤

1. 执行server.py，启动服务，此服务提供2个接口：

   - /get_file：获取待分类的文件路径，每次一个，如果队列中没有文件，则返回空
   - /update_status：更新文件分类状态
   - /index：一个简单的web界面，可以查看当前的分类进度
   - 启动参数为：
     - --layout_sample_dir：layout样本的保存目录，这里面每个文件会被server分发出去。
     - --port：服务端口
     - --host：服务地址
     - --timeout：客户端处理一个文件的超时时间，如果超时会被重新分配。
     - --reset：是否重置。会清空当前的分类状态，不保存重启前的任务状态。

2. 执行classify.sh，此脚本会向slurm集群提交任务。这些任务常驻GPU，每个任务调用server.py的/get_file接口获取待分类的文件，然后进行分类，并调用server.py的/update_status接口更新文件分类状态。

   - --partation：slurm的partation，例如：xinghe-gpu
   - --max-job：最大提交任务数
   - --tag：slurm的tag，例如：html_layout_classify，用于同一个管理节点启动区分不同的任务隔离开日志的输出
   - --task-num：每个GPU上开启多少个任务实例，为了充分提高GPU的利用率
   - --debug：是否开启debug模式
   - --result-save-dir：分类结果的保存目录
   - --server-addr：server的地址，例如：http://127.0.0.1:5000

3. 执行classify-spot.sh ，可以利用spot资源。
