from typing import Dict

from llm_web_kit.libs.statics import Statics

MetricsResult = Dict[str, Dict[str, float]]


class Metrics:
    def __init__(self):
        pass

    def eval_type_acc(self, base, pre: Statics) -> MetricsResult:
        """评估类型准确率.
        Args:
            base: 基础数据（Ground Truth）
            pre: 预测数据
        Returns:
            MetricsResult: 包含每种类型准确率的字典
                格式: {
                    "type_name": {
                        "count": float,
                        "type_acc": float,
                        "content_acc": float
                    }
                }
        """
        result: MetricsResult = {}
        total_count = 0.0

        # 获取 statics 字段
        base_stats = base.__getall__()
        pre_stats = pre.__getall__()

        # 获取所有唯一的类型
        all_types = set(base_stats.keys()) | set(pre_stats.keys())

        for type_name in all_types:
            # 直接从 statics 字典中获取数值
            count_gt = float(base_stats.get(type_name, 0))
            count_pre = float(pre_stats.get(type_name, 0))

            if count_gt == 0:
                # 如果GT中没有这个类型，但预测出现了，准确率为0
                type_acc = 0.0
            else:
                # 计算准确率
                diff_ratio = abs(count_gt - count_pre) / count_gt
                # 归一化处理：如果差异比率大于1，则准确率为0；否则准确率为1-差异比率
                type_acc = max(0.0, 1.0 - diff_ratio)

            result[type_name] = {
                'count': count_gt,  # 使用GT的数量作为基准
                'type_acc': type_acc
            }
            total_count += count_gt

        # 计算整体准确率（加权平均）
        overall_acc = (sum(
            res['type_acc'] * res['count']
            for res in result.values()
        ) / total_count) if total_count > 0 else 0.0

        # 添加Overall统计
        result['Overall'] = {
            'count': total_count,
            'type_acc': overall_acc
        }

        return result

    def eval_content_acc(self, base, pre: str) -> MetricsResult:
        """评估内容准确率.

        base: 基础数据
        pre: 预测数据
        """
        pass


if __name__ == '__main__':
    metrics = Metrics()
    base = Statics({'table': 10, 'list': 5, 'list.text': 10})
    pre = Statics({'table': 9, 'list': 5, 'list.text': 11})
    result = metrics.eval_type_acc(base, pre)
    print(result)
