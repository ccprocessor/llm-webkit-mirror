# CC 数据输入格式标准

此输入格式的用途是定义CC标准处理流程的输入数据格式。
在CC进入到提取之前，输入流水线的数据格式必顋符合此标准。

此处的数据格式的使用方在：[pipeline_html_tpl.jsonc](../../../llm-web-kit/pipeline/pipe_tpl/pipeline_html_tpl.jsonc)
其中 `formatted_raw_input_data_output_path` 字段中制定的路径中数据需要满足本标准。

## 流水线输入数据格式

样例：

```jsonl
{}
{}
```

字段说明：

| 字段 | 类型   | 描述               | 是否必须 |
| ---- | ------ | ------------------ | -------- |
| xx   | string | 值固定为code       | 是       |
| yy   | array  | \[x1, y1, x2, y2\] | 可选     |
