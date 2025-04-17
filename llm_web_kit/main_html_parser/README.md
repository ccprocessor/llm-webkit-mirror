本文档是对main html解析流程的说明

- 模块代码：llm_web_kit/main_html_parser 路径是模块相关代码，其中processor.py和processor_chain.py是链式处理脚本，processor.py是抽象类，main_html_processor.py是实现类。
- 流程解析代码：llm_web_kit/main_html_parser/parser路径下是9个解析步骤代码，基类是parse.py，每个步骤继承BaseMainHtmlParser基类，实现其中的parse抽象方法
- 流程处理对象：整个流程通过llm_web_kit/input/pre_data_json.py中的PreDataJson结构进行数据传递（部分流程有接口调用），每个步骤依赖上一个流程的输出，并在对象中通过\_\_setitem\_\_设置自己的输出，对象的key在PreDataJsonKey中定义，只能获取和设置定义的key，避免字段混乱。如果需要增加、修改key，请在PreDataJsonKey中进行操作，并补充对应的测试用例。
- 异常处理：在脚本llm_web_kit/exception/exception.jsonc中定义了异常code和message，main html相关的异常在Processor 和 Parser模块。

```python
#异常处理示例：
# 1. try except处理
try:
    ...
except DomainClusteringParserException as e1:
    raise e1
except Exception as e2:
    raise e2

# 2. 直接raise异常
if ...:
    pass
else:
    raise DomainClusteringParserException

```

- 测试用例：tests/llm_web_kit/main_html_parser/processor/parser中编写每个步骤的对应的测试用例，提交github时要求codecov通过基准线。

- 每个步骤相关信息说明

| 步骤 | 模块                   | 对应脚本                 | 异常类                             | 功能                                                                                                   |
| ---- | ---------------------- | ------------------------ | ---------------------------------- | ------------------------------------------------------------------------------------------------------ |
| 1    | domain处理模块         | domain_clustering.py     | DomainClusteringParserException    | 将原始的CC数据按域名domain进行聚类，保证相同domain的html数据在一个或多个文件中                         |
| 2    | layout聚类模块         | layout_clustering.py     | LayoutClusteringParserException    | 将域名domain进一步细分，对同一个domain下layout结构相同的html进行聚类                                   |
| 3    | html代表选择策略       | typical_html_selector.py | TypicalHtmlSelectorParserException | 以layout粒度，找出当前批次layout中1个具有代表性的网页（内容区域深度、宽度最大的最优等）                |
| 4    | html精简策略           | tag_simplifier.py        | TagSimplifiedProcessorException    | 对代表性的html网页进行精简，保证数据大小在大模型的输入token范围内                                      |
| 5    | 大模型正文识别         | llm_main_identifier.py   | LlmMainIdentifierParserException   | 结合prompt提示词，对精简后的html网页进行正文内容（即main_html）进行框定，输出item_id结构的页面判定结果 |
| 6    | item_id到原网页tag映射 | tag_mapping.py           | TagMappingParserException          | 将item_id与原html网页tag进行映射                                                                       |
| 7    | layout子树提取         | layout_subtree_parser.py | LayoutSubtreeParserException       | 根据上一步映射html的tag，抽取layout代表网页的子树                                                      |
| 8    | 同批次layout网页处理   | layout_batch_parser.py   | LayoutBatchParserException         | 根据上一步子树结构，推理同批次layout上的所有网页，输出main_html                                        |
| 9    | dom内容过滤            | dom_content_filter.py    | DomContentFilterParserException    | 根据头尾、重复率，删除头尾的导航、广告等节点                                                           |
