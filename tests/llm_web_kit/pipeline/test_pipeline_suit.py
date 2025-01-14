"""
测试pipeline_suit.py， 集成测试：
测试方法是：
1. 设定一个场景：从一些散落的html中提取content_list
2. 定义test_pipline_suit_html.jsonc，定义pipeline的执行顺序和模块，数据路径
3. 准备一些html文件，按照零散html的输入标准组织成jsonl数据
4. 执行解析，得到content_list，并比对期望结果

测试需要涵盖：
1. 正确提取时候的content_list是否符合期望
2. 各类异常的抛出是否符合期望
"""
