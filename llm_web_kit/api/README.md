# LLM Web Kit API

基于 FastAPI 的 LLM Web Kit API 服务，提供 HTML 解析功能。

## 功能特性

- 🚀 基于 FastAPI 的高性能 Web API
- 📄 HTML 内容解析与结构化输出
- 🔗 支持 URL 和 HTML 字符串输入
- 📁 支持 HTML 文件上传
- 📚 自动生成的 API 文档
- 🔧 可配置的解析选项

## 快速开始

配置环境变量

```bash
export MODEL_PATH=""
```

或者配置文件.llm-web-kit.jsonc添加“model_path”

安装依赖

```bash
pip install -r requirements.txt
python llm_web_kit/api/run_server.py
```

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API 端点

### HTML 解析

POST /api/v1/html/parse

请求示例：

```bash
curl -s -X POST "http://127.0.0.1:8000/api/v1/html/parse" \
  -H "Content-Type: application/json" \
  -d '{
    "html_content": "<html><body><h1>Hello World</h1></body></html>",
    "url": "https://helloworld.com/hello",
    "options": {
      "clean_html": true
    }
  }'
```

或直接发送以下 JSON 作为请求体：

```json
{
  "html_content": "<html><body><h1>Hello World</h1></body></html>",
  "options": {
    "clean_html": true
  }
}
```

### 文件上传解析

POST /api/v1/html/upload

```bash
curl -s -X POST "http://127.0.0.1:8000/api/v1/html/upload" \
  -F "file=@/path/to/file.html"
```

### 服务状态

GET /api/v1/html/status

## 返回结构示例（/api/v1/html/parse 与 /api/v1/html/upload 成功返回）

以下示例为 HTML 解析成功时的统一响应结构：

```json
{
  "success": true,
  "message": "HTML 解析成功",
  "timestamp": "2025-08-26T16:45:43.140638",
  "data": {
    "layout_file_list": [],
    "typical_raw_html": "<html><body><h1>Hello World</h1></body></html>",
    "typical_raw_tag_html": "<html><body><h1 _item_id=\"1\">Hello World</h1><h2 _item_id=\"2\">not main content</h2></body></html>\n",
    "llm_response": {
      "item_id 1": 0,
      "item_id 2": 1
    },
    "typical_main_html": "<html><body><h1 _item_id=\"1\">Hello World</h1></body></html>",
    "html_target_list": ["Hello World"]
  },
  "metadata": null
}
```

## 常见问题

- 422 错误：确认请求头 `Content-Type: application/json`，并确保请求体 JSON 合法。
- 依赖缺失：`pip install -r llm_web_kit/api/requirements.txt`。
