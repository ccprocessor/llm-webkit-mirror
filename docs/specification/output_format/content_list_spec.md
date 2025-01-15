# 流水线content_list格式数据输出标准

## 目的

定义content_list的目的是为了统一流水线输出的数据格式，无论是网页、电子书、富文本pdf,word，ppt等，都可以转化到这个格式。
使得不同的下游任务可以快速根据content_list导出所需要的数据格式。

> 目的不是用户最终使用的格式，而是为了快速转化为下游任务需要的格式，例如大语言模型不需要图和音视频而多模态模型需要用。

## 样例

<b>遵循原则</b>

- content_list 是被分解的文档，每个元素是文章中的一段内容，可以使文本、图片、代码、音视频等。
- 每个元素的表达方式是不一样的，受制于其`type`类型，逐层深入。
- 为了调试找问题方便，留下了`raw_content`字段，用于存储原始的文本内容。
- 整体结构是一个二维数组，每个元素是一个数组，表示一页内容。如果页面为空，则需要填充一个空数组进行占位，默认二维数组下标即为**页码**。

```json
[
    [
        {
            "type": "code",
            "bbox": [0, 0, 50, 50],
            "raw_content": "<code>def add(a, b):\n    return a + b</code>",
            "content": {
                "code_content": "def add(a, b):\n    return a + b",
                "language": "python"
            }
        },
        {
            "type": "equation-interline",
            "bbox": [0, 0, 50, 50],
            "raw_content": "a^2 + b^2 = c^2",
            "content": {
                "math_content": "a^2 + b^2 = c^2",
                "math_type": "kelatex|mathml|asciimath"
            }
        },
        {
            "type": "image",
            "bbox": [0, 0, 50, 50],
            "raw_content": null,
            "content": {
                "url": "https://www.example.com/image.jpg",
                "path": "s3://llm-media/image.jpg",
                "data": "如果是base64形式的图片，则用这个字段，忽略url和path ",
                "alt": "example image",
                "title": "example image",
                "caption": "text from somewhere",
                "image_style": "qrcode|table|chart"
            }
        }
    ],
    [
        {
            "type": "audio",
            "bbox": [0, 0, 50, 50],
            "raw_content": null,
            "content": {
                "sources": ["https://www.example.com/audio.mp3"],
                "path": "s3://llm-media/audio.mp3",
                "title": "example audio",
                "caption": "text from somewhere"
            }
        },
        {
            "type": "video",
            "bbox": [0, 0, 50, 50],
            "raw_content": null,
            "content": {
                "sources": ["https://www.example.com/video.avi"],
                "path": "s3://llm-media/video.mp4",
                "title": "example video",
                "caption": "text from somewhere"
            }
        },
        {
            "type": "table",
            "bbox": [0, 0, 50, 50],
            "raw_content": null,
            "content": {
                "html": "<table><tr><td>1</td><td>2</td></tr></table>",
                "title": "example table",
                "note": "数据来源于...",
                "is_complex": false // 是否是复杂表格(跨行、跨列的, 默认为false
            }
        },
        {
            "type": "list",
            "bbox": [0, 0, 50, 50],
            "raw_content": null,
            "content": {
                "items": [ //列表里只考虑文本和公式，如果有其他类型元素，列表就转为若干个段落，否则结构太复杂了
                    [
                        {"c": "爱因斯坦的质量方差公式是", "t": "text", "bbox": [0, 0, 10, 10]},
                        {"c": "E=mc^2", "t": "equation-inline", "bbox": [10, 0, 10, 10]},
                        {"c": "，其中E是能量，m是质量，c是光速 ", "t": "text", "bbox": [20, 0, 10, 10]}
                    ],
                    [
                        {"c": "爱因斯坦的质量方差公式是", "t": "text", "bbox": [0, 0, 10, 10]},
                        {"c": "E=mc^2", "t": "equation-inline", "bbox": [10, 0, 10, 10]},
                        {"c": "，其中E是能量，m是质量，c是光速 ", "t": "text", "bbox": [20, 0, 10, 10]}
                    ]
                ],
                "ordered": true
            }
        }
    ],
    [
        {
            "type": "title",
            "bbox": [0, 0, 50, 50],
            "raw_content": null,
            "content": {
                "title_content": "大模型好，大模型棒",
                "level": 1 // 标题级别，1-N, 1最大
            }
        },
        {
            "type": "paragraph",
            "bbox": [0, 0, 50, 50],
            "raw_content": null,
            "content": [
                {"c": "爱因斯坦的质量方差公式是", "t": "text", "bbox": [0, 0, 10, 10]},
                {"c": "E=mc^2", "t": "equation-inline", "bbox": [10, 0, 10, 10]},
                {"c": "，其中E是能量，m是质量，c是光速 ", "t": "text", "bbox": [20, 0, 10, 10]}
            ]
        }
    ]

]
```

## 字段定义

### 代码段

```json
{
    "type": "code",
    "bbox": [0, 0, 50, 50],
    "raw_content": "<code>def add(a, b):\n    return a + b</code>"
    "content": {
          "code_content": "def add(a, b):\n    return a + b",
          "language": "python",
          "by": "hilightjs"
    }
}
```

| 字段                 | 类型   | 描述                          | 是否必须 |
| -------------------- | ------ | ----------------------------- | -------- |
| type                 | string | 值固定为code                  | 是       |
| bbox                 | array  | \[x1, y1, x2, y2\]            | 可选     |
| raw_content          | string | 原始文本内容                  | 可选     |
| content.code_content | string | 干净的，格式化过的代码内容    | 是       |
| content.language     | string | 代码语言，python\\cpp\\php... | 可选     |
| content.by           | string | 哪种代码高亮工具 、自定义规则 | 是       |

### 公式段

```json
{
    "type": "equation-interline",
    "bbox": [0, 0, 50, 50],
    "raw_content": "a^2 + b^2 = c^2",
    "content": {
          "math_content": "a^2 + b^2 = c^2",
          "math_type": "kelatex",
          "by": "mathjax"
    }
}
```

| 字段                 | 类型   | 描述                                                            | 是否必须 |
| -------------------- | ------ | --------------------------------------------------------------- | -------- |
| type                 | string | 值固定为equation-interline                                      | 是       |
| bbox                 | array  | \[x1, y1, x2, y2\]                                              | 可选     |
| raw_content          | string | 原始文本内容                                                    | 可选     |
| content.math_content | string | 干净的，格式化过的公式内容。无论是行内还是行间公式两边都不能有$ | 是       |
| content.math_type    | string | 公式语言类型，kelatex\\mathml\\asciimath                        | 可选     |
| content.by           | string | 原html中使用公式渲染器                                          | 可选     |

### 图片段

```json
{
    "type": "image",
    "bbox": [0, 0, 50, 50],
    "raw_content": null,
    "content": {
        "url": "https://www.example.com/image.jpg",
        "path": "s3://llm-media/image.jpg",
        "data": "如果是base64形式的图片，则用这个字段，忽略url和path ",
        "alt": "example image",
        "title": "example image",
        "caption": "text from somewhere",
        "image_style": "qrcode|table|chart"
    }
}
```

| 字段                | 类型   | 描述                             | 是否必须 |
| ------------------- | ------ | -------------------------------- | -------- |
| type                | string | 值固定为image                    | 是       |
| bbox                | array  | \[x1, y1, x2, y2\]               | 可选     |
| raw_content         | string | 原始文本内容                     | 可选     |
| content.url         | string | 图片的url地址                    | 可选     |
| content.path        | string | 图片的存储路径                   | 可选     |
| content.data        | string | base64形式的图片数据             | 可选     |
| content.alt         | string | 图片的alt属性                    | 可选     |
| content.title       | string | 图片的title属性                  | 可选     |
| content.caption     | string | 图片的caption属性                | 可选     |
| content.image_style | string | 图片的类型，qrcode\\table\\chart | 可选     |

### 音频段

```json
{
    "type": "audio",
    "bbox": [0, 0, 50, 50],
    "raw_content": null,
    "content": {
        "sources": ["https://www.example.com/audio.mp3"],
        "path": "s3://llm-media/audio.mp3",
        "title": "example audio",
        "caption": "text from somewhere"
    }
}
```

| 字段            | 类型   | 描述               | 是否必须 |
| --------------- | ------ | ------------------ | -------- |
| type            | string | 值固定为audio      | 是       |
| bbox            | array  | \[x1, y1, x2, y2\] | 可选     |
| raw_content     | string | 原始文本内容       | 可选     |
| content.sources | array  | 音频的url地址      | 可选     |
| content.path    | string | 音频的存储路径     | 可选     |
| content.title   | string | 音频的title属性    | 可选     |
| content.caption | string | 音频的caption属性  | 可选     |

### 视频段

```json
{
        "type": "video",
        "bbox": [0, 0, 50, 50],
        "raw_content": null,
        "content": {
            "sources": ["https://www.example.com/video.avi"],
            "path": "s3://llm-media/video.mp4",
            "title": "example video",
            "caption": "text from somewhere"
        }
    }
```

| 字段            | 类型   | 描述               | 是否必须 |
| --------------- | ------ | ------------------ | -------- |
| type            | string | 值固定为video      | 是       |
| bbox            | array  | \[x1, y1, x2, y2\] | 可选     |
| raw_content     | string | 原始文本内容       | 可选     |
| content.sources | array  | 视频的url地址      | 可选     |
| content.path    | string | 视频的存储路径     | 可选     |
| content.title   | string | 视频的title属性    | 可选     |
| content.caption | string | 视频的caption属性  | 可选     |

### 表格段

```json
{
    "type": "table",
    "bbox": [0, 0, 50, 50],
    "raw_content": null,
    "content": {
        "html": "<table><tr><td>1</td><td>2</td></tr></table>",
        "title": "example table",
        "note": "数据来源于...",
        "is_complex": false // 是否是复杂表格(跨行、跨列的, 默认为false
    }
}
```

| 字段               | 类型    | 描述                                     | 是否必须 |
| ------------------ | ------- | ---------------------------------------- | -------- |
| type               | string  | 值固定为table                            | 是       |
| bbox               | array   | \[x1, y1, x2, y2\]                       | 可选     |
| raw_content        | string  | 原始文本内容                             | 可选     |
| content.html       | string  | 表格的html内容                           | 是       |
| content.title      | string  | 表格的title属性                          | 可选     |
| content.note       | string  | 表格的note属性                           | 可选     |
| content.is_complex | boolean | 是否是复杂表格(跨行、跨列的, 默认为false | 可选     |

### 列表段

```json
{
    "type": "list",
    "bbox": [0, 0, 50, 50],
    "raw_content": null,
    "content": {
        "items": [ //列表里只考虑文本和公式，如果有其他类型元素，列表就转为若干个段落，否则结构太复杂了
            [
                {"c": "爱因斯坦的质量方差公式是", "t": "text", "bbox": [0,0,10,10]},
                {"c": "E=mc^2", "t": "equation-inline", "bbox": [10,0,10,10]},
                {"c": "，其中E是能量，m是质量，c是光速 ","t": "text", "bbox": [20,0,10,10]}
           ],
           [
                {"c": "爱因斯坦的质量方差公式是", "t": "text", "bbox": [0,0,10,10]},
                {"c": "E=mc^2", "t": "equation-inline", "bbox": [10,0,10,10]},
                {"c": "，其中E是能量，m是质量，c是光速 ","t": "text", "bbox": [20,0,10,10]}
           ]
        ],
        "ordered": true
    }
}
```

| 字段            | 类型    | 描述                                                 | 是否必须 |
| --------------- | ------- | ---------------------------------------------------- | -------- |
| type            | string  | 值固定为list                                         | 是       |
| bbox            | array   | \[x1, y1, x2, y2\]                                   | 可选     |
| raw_content     | string  | 原始文本内容                                         | 可选     |
| content.items   | array   | 列表项，每个元素是一个段落，段落里的元素是文本或公式 | 是       |
| content.ordered | boolean | 是否是有序列表                                       | 可选     |

<b>items字段说明</b>

- `items`是一个二维数组，每个元素是一个段落，段落里的元素是文本或公式。
- 每个元素是一个对象，包含3个字段，c和t,bbox。 c是内容，t是类型，bbox是坐标。
- t的取值有3种，`text`和`equation-inline`和`md`，分别表示纯文本和行内公式和markdown。

### 标题段

```json
{
    "type": "title",
    "bbox": [0, 0, 50, 50],
    "raw_content": null,
    "content": {
        "title_content": "大模型好，大模型棒",
        "level": 1 // 标题级别，1-N, 1最大
    }
}
```

| 字段                  | 类型   | 描述                 | 是否必须 |
| --------------------- | ------ | -------------------- | -------- |
| type                  | string | 值固定为title        | 是       |
| bbox                  | array  | \[x1, y1, x2, y2\]   | 可选     |
| raw_content           | string | 原始文本内容         | 可选     |
| content.title_content | string | 标题内容             | 是       |
| content.level         | int    | 标题级别，1-N, 1最大 | 可选     |

### 段落

```json
{
    "type": "paragraph",
    "bbox": [0, 0, 50, 50],
    "raw_content": null,
    "content": [
        {"c": "爱因斯坦的质量方差公式是", "t": "text", "bbox": [0,0,10,10]},
        {"c": "E=mc^2", "t": "equation-inline", "bbox": [10,0,10,10]},
        {"c": "，其中E是能量，m是质量，c是光速 ","t": "text", "bbox": [20,0,10,10]}
      ]
}
```

| 字段        | 类型   | 描述                                                                                  | 是否必须 |
| ----------- | ------ | ------------------------------------------------------------------------------------- | -------- |
| type        | string | 值固定为paragraph                                                                     | 是       |
| bbox        | array  | \[x1, y1, x2, y2\]                                                                    | 可选     |
| raw_content | string | 原始文本内容                                                                          | 可选     |
| content     | array  | 段落内容，每个元素是一个对象，包含3个字段，c和t,bbox。 c是内容，t是类型，bbox是坐标。 | 是       |

<b>content字段说明</b>

- content是一个数组，每个元素是一个对象，包含3个字段，`c`和`t`,`bbox`。 c是内容，t是类型，bbox是坐标。
- t的取值有3种，`text`和`equation-inline`和`md`，分别表示纯文本和行内公式和markdown。
- `bbox`是一个数组，表示元素的坐标，\[x1, y1, x2, y2\]。 (x1, y1)左上角坐标，(x2, y2)右下角坐标。

## 参考

- [图文交错数据标准格式（2.1）](https://aicarrier.feishu.cn/wiki/L1vUwB0Ozi9vZBkdrzycaHwAn0e)
