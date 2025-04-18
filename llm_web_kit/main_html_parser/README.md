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

| 步骤 | 模块                   | 对应脚本                 | 关键输入                               | 关键输出                                | 异常类                             | 功能描述                                |
| ---- | ---------------------- | ------------------------ | -------------------------------------- | --------------------------------------- | ---------------------------------- | --------------------------------------- |
| 1    | domain处理模块         | domain_clustering.py     | domain_name/domain_id/domain_file_list | -                                       | DomainClusteringParserException    | 将原始CC数据按域名聚类，保证相同domain的html数据在一个或多个文件中 |
| 2    | layout聚类模块         | layout_clustering.py     | layout_name/layout_file_list           | -                                       | LayoutClusteringParserException    | 将域名进一步细分，对同domain下layout结构相同的html进行聚类 |
| 3    | html代表选择策略       | typical_html_selector.py | -                                      | typical_raw_html                        | TypicalHtmlSelectorParserException | 以layout粒度找出当前批次中1个代表性网页（基于内容区域深度/宽度等最优选择） |
| 4    | html精简策略           | tag_simplifier.py        | typical_raw_html                       | typical_raw_tag_html/typical_simplified_html | TagSimplifiedProcessorException    | 对代表性html进行精简，确保数据大小符合大模型输入token限制 |
| 5    | 大模型正文识别         | llm_main_identifier.py   | typical_simplified_html                | llm_response                            | LlmMainIdentifierParserException   | 结合prompt提示词框定正文内容（main_html），输出item_id结构的页面判定结果 |
| 6    | item_id到原网页tag映射 | tag_mapping.py           | llm_response                           | html_element_list                       | TagMappingParserException          | 建立item_id与原html网页tag的映射关系    |
| 7    | layout子树提取         | layout_subtree_parser.py | html_element_list                      | html_target_list                        | LayoutSubtreeParserException       | 根据映射的html tag抽取layout代表网页的子树 |
| 8    | 同批次layout网页处理   | layout_batch_parser.py   | html_target_list                       | main_html                               | LayoutBatchParserException         | 根据子树结构推理同批次layout的所有网页，输出main_html |
| 9    | dom内容过滤            | dom_content_filter.py    | main_html                              | filtered_main_html                      | DomContentFilterParserException    | 基于头尾重复率删除导航、广告等非正文节点 |
