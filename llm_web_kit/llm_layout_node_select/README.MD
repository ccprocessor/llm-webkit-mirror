# select main html node by LLM

## 环境

1. 创建conda 环境，python 3.10-3.13
2. 安装llm-web-kit,执行 `pip install -v -e .`或者安装pypi上的 `pip install llm-web-kit`

## 启动

1. 首先启动 llm_web_kit/html_layout_classify/server.py
2. 配置cfg.template.jsonc文件，写上server的服务地址，以及模型服务地址
3. 启动llm_web_kit/llm_layout_node_select/main.sh
