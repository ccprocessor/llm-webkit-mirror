import uuid
from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel

from .metrics import MetricsResult


class ResultBase(BaseModel):
    """评测结果基类."""
    task_id: str
    output_path: str
    create_time: str
    finish_time: str

    def to_dict(self) -> dict:
        """转换为字典格式."""
        return self.model_dump()

    # 更新finish_time
    def finish(self):
        self.finish_time = datetime.now().strftime('%Y%m%d_%H%M%S')


class Result_Summary(ResultBase):
    """评测结果概览
        {
            "task_id": "5bbf7c8c-e8f2-11ef-a5a8-acde48001122",  # 评测任务唯一id
            "output_path": "outputs/20250212_113509_5bbf75c0",  # 评测结果保存路径
            "create_time": "20250212_113509",  # 评测任务创建时间
            "finish_time": "20250212_113632",  # 评测任务完成时间
            "total": 52002,  # 总评测文件数量
            "result_summary": { # 评测结果
                "Overall": {
                    "count": 52000, # 元素数量
                    "type_acc": 0.9997, # 元素类型识别准确性
                    "content_acc": 0.9997 # 元素内容识别准确性
                },
                "equation-interline": {
                    "count": 52, # 元素数量
                    "type_acc": 0.9997, # 元素类型识别准确性
                    "content_acc": 0.9997 # 元素内容识别准确性
                },
                "code": {
                    "count": 5, # 元素数量
                    "type_acc": 0.9997, # 元素类型识别准确性
                    "content_acc": 0.9997 # 元素内容识别准确性
                },
                ...
            },
            "error_summary": {
                    "count": 2, # 错误数量
                }
        }
    """
    total: int
    result_summary: Dict[str, Dict[str, float]]
    error_summary: Dict[str, int]

    @classmethod
    def create(cls, task_id: str, output_path: str, total: int, result_summary: MetricsResult, error_count: int = 0):
        """创建评测结果概览.

        Args:
            output_path: 输出路径
            total: 总评测文件数量
            result_summary: 评测结果
            error_count: 错误数量
        """
        now = datetime.now()
        return cls(
            task_id=task_id if task_id else str(uuid.uuid1()),
            output_path=output_path,
            create_time=now.strftime('%Y%m%d_%H%M%S'),
            finish_time=now.strftime('%Y%m%d_%H%M%S'),
            total=total,
            result_summary=result_summary,
            error_summary={'count': error_count}
        )


class Result_Item(BaseModel):
    """评测结果项."""
    file_path: str
    result_summary: MetricsResult


class Error_Item(BaseModel):
    """错误结果项."""
    file_path: str
    error_detail: str


class Result_Detail(ResultBase):
    """评测结果详情
    {
        "task_id": "5bbf7c8c-e8f2-11ef-a5a8-acde48001122",  # 评测任务唯一id
        "output_path": "outputs/20250212_113509_5bbf75c0",  # 评测结果保存路径
        "create_time": "20250212_113509",  # 评测任务创建时间
        "finish_time": "20250212_113632",  # 评测任务完成时间
        "result_detail": {
            "success_result": [
                {
                    "file_path": "html/ccmath/1.html",  # 评测文件路径
                    "result_summry": { # 评测结果
                        "Overall": {
                            "count": 52000, # 元素数量
                            "type_acc": 0.9997, # 元素类型识别准确性
                            "content_acc": 0.9997 # 元素内容识别准确性
                        },
                        "equation-interline": {
                            "count": 52, # 元素数量
                            "type_acc": 0.9997, # 元素类型识别准确性
                            "content_acc": 0.9997 # 元素内容识别准确性
                        },
                        "code": {
                            "count": 5, # 元素数量
                            "type_acc": 0.9997, # 元素类型识别准确性
                            "content_acc": 0.9997 # 元素内容识别准确性
                        },
                        ...
                    }
                },
                ...
            ],
            "error_result": [ # 抽取失败的网页
                {
                    "file_path": "html/ccmath/1.html", # 评测文件路径
                    "error_detail": "type_error" # 错误详情
                },
                ...
            ]
        }
    }
    """
    result_detail: Dict[str, List]

    @classmethod
    def create(cls, task_id: str, output_path: str,
               success_results: List[Result_Item] = None,
               error_results: List[Error_Item] = None):
        """创建评测结果详情.

        Args:
            task_id: 与 Result_Summary 共享的任务ID
            output_path: 输出路径
            success_results: 成功的评测结果列表
            error_results: 失败的评测结果列表
        """
        now = datetime.now()
        return cls(
            task_id=task_id if task_id else str(uuid.uuid1()),
            output_path=output_path,
            create_time=now.strftime('%Y%m%d_%H%M%S'),
            finish_time=now.strftime('%Y%m%d_%H%M%S'),
            result_detail={
                'success_result': success_results or [],
                'error_result': error_results or []
            }
        )
