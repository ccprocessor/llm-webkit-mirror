import json
import os
import sys
import unittest
import uuid
from pathlib import Path


class TestST(unittest.TestCase):
    """基于bench/data/origin目录下的数据进行抽取集成测试."""

    def setUp(self):
        """设置测试环境."""
        # 获取项目根目录的绝对路径
        self.root = Path(__file__).parent.parent.parent.absolute()

        # 将项目根目录添加到Python路径
        if str(self.root) not in sys.path:
            sys.path.insert(0, str(self.root))

        self.sourcePath = os.path.join(self.root, 'bench/data/all.json')
        self.outputPath = os.path.join(self.root, 'bench/output')
        # self.pipelineConfigPath = os.path.join(self.root, 'bench/config/ours_config.jsonc')
        self.pipeline_data_path = os.path.join(self.root, 'bench/config/ours_data_config.jsonl')
        self.chainConfig = {
            'extractor_pipe': {
                'enable': True,
                'validate_input_format': False,
                'pre_extractor': [
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.html.pre_extractor.TestHTMLFileFormatFilterPreExtractor',
                        'class_init_kwargs': {
                            'html_parent_dir': 'bench/data/'
                        }
                    },
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.html.pre_extractor.HTMLFileFormatCleanTagsPreExtractor',
                        'class_init_kwargs': {}
                    }
                ],
                'extractor': [
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.html.extractor.HTMLFileFormatExtractor',
                        'class_init_kwargs': {}
                    }
                ],
                'post_extractor': [
                    {
                        'enable': True,
                        'python_class': 'llm_web_kit.extractor.html.post_extractor.ContentListStaticsPostExtractor'
                    }
                ]
            },
        }

    def test_st_bench(self):
        """测试run.py."""
        from bench.common.result import (Error_Item, Result_Detail,
                                         Result_Summary)
        from bench.eval.ours import eval_ours_extract_html

        task_id = str(uuid.uuid1())
        output_path = os.path.join(self.outputPath, f'{task_id}')

        summary = Result_Summary.create(
            task_id=task_id,
            output_path=output_path,
            total=0,
            result_summary={},
            error_count=0
        )

        # 创建评测结果详情
        detail = Result_Detail.create(
            task_id=summary.task_id,  # 使用相同的task_id
            output_path=output_path,
        )

        with open(self.sourcePath, 'r') as f:
            files = json.load(f)
            # files结构是{'filename': {'url': '', 'filepath': ''}}，获取filepath
            for fileName in files:
                filepath = files[fileName]['origin_filepath']
                groundtruth_filepath = os.path.join(self.root, 'bench/data/', files[fileName]['groundtruth_filepath'])
                page_layout_type = files[fileName]['layout_type']
                summary.total += 1
                print(f'开始抽取:{filepath}...')
                try:
                    output, content_list, main_html, statics = eval_ours_extract_html(self.chainConfig, self.pipeline_data_path, f'{self.root}/bench/data/{filepath}', page_layout_type)
                    # 断言statics中的元素数量和groundtruth_filepath中的元素数量一致
                    with open(groundtruth_filepath, 'r') as f:
                        groundtruth = json.loads(f.readline().strip())
                    # 断言equation-interline, paragraph.equation-inline和list.equation-inline元素数一致
                    self.assertEqual(statics.get('equation-interline'), groundtruth.get('statics', {}).get('equation-interline'), msg=f'{filepath}抽取equation-interline数量和groundtruth:{groundtruth_filepath}不一致')
                    self.assertEqual(statics.get('paragraph.equation-inline'), groundtruth.get('statics', {}).get('paragraph.equation-inline'), msg=f'{filepath}抽取paragraph.equation-inline数量和groundtruth:{groundtruth_filepath}不一致')
                    self.assertEqual(statics.get('list.equation-inline'), groundtruth.get('statics', {}).get('list.equation-inline'), msg=f'{filepath}抽取list.equation-inline数量和groundtruth:{groundtruth_filepath}不一致')
                except Exception as e:
                    summary.error_summary['count'] += 1
                    detail.result_detail['error_result'].append(Error_Item(
                        file_path=filepath,
                        error_detail=str(e)
                    ))
        summary.finish()
        detail.finish()
        self.assertIsNotNone(summary)
        self.assertIsNotNone(detail)
        self.assertEqual(summary.error_summary['count'], 0, msg=f'测试数据抽取有失败, 抽取失败的数据详情: {detail.to_dict()}')


if __name__ == '__main__':
    r = TestST()
    r.setUp()
    r.test_st_bench()
