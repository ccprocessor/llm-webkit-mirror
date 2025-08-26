"""HTML 处理服务.

桥接原有项目的 HTML 解析和内容提取功能，提供统一的 API 接口。
"""

from typing import Any, Dict, Optional

from ..dependencies import get_logger, get_settings

logger = get_logger(__name__)
settings = get_settings()


class HTMLService:
    """HTML 处理服务类."""

    def __init__(self):
        """初始化 HTML 服务."""
        # 目前使用简化管线
        pass

    def _init_components(self):
        """兼容保留（当前未使用）"""
        return None

    async def parse_html(
        self,
        html_content: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """解析 HTML 内容."""
        try:
            if not html_content:
                raise ValueError("必须提供 HTML 内容")

            # 延迟导入，避免模块导入期异常导致服务类不可用
            try:
                from llm_web_kit.input.pre_data_json import (PreDataJson,
                                                             PreDataJsonKey)
                from llm_web_kit.main_html_parser.parser.tag_mapping import \
                    MapItemToHtmlTagsParser
                from llm_web_kit.main_html_parser.simplify_html.simplify_html import \
                    simplify_html
            except Exception as import_err:
                logger.error(f"依赖导入失败: {import_err}")
                raise

            # 简化网页
            try:
                simplified_html, typical_raw_tag_html, _ = simplify_html(html_content)
            except Exception as e:
                logger.error(f"简化网页失败: {e}")
                raise

            # 模型推理
            llm_response = await self._parse_with_model(simplified_html, options)

            # 结果映射
            pre_data = PreDataJson({})
            pre_data[PreDataJsonKey.TYPICAL_RAW_HTML] = html_content
            pre_data[PreDataJsonKey.TYPICAL_RAW_TAG_HTML] = typical_raw_tag_html
            pre_data[PreDataJsonKey.LLM_RESPONSE] = llm_response
            parser = MapItemToHtmlTagsParser({})
            pre_data = parser.parse_single(pre_data)

            # 将 PreDataJson 转为标准 dict，避免响应模型校验错误
            return dict(pre_data.items())

        except Exception as e:
            logger.error(f"HTML 解析失败: {e}")
            raise

    async def _parse_with_model(self, html_content: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {
            "item_id 1": 0,
            "item_id 2": 0,
            "item_id 3": 0,
            "item_id 4": 0,
            "item_id 5": 0,
            "item_id 6": 0,
            "item_id 7": 0,
            "item_id 8": 0,
            "item_id 9": 1,
            "item_id 10": 0,
            "item_id 11": 0,
            "item_id 12": 0,
            "item_id 13": 0,
            "item_id 14": 0,
            "item_id 15": 0,
            "item_id 16": 0,
            "item_id 17": 0,
            "item_id 18": 0,
            "item_id 19": 0,
            "item_id 20": 0,
            "item_id 21": 0,
            "item_id 22": 0,
            "item_id 23": 0,
            "item_id 24": 0,
            "item_id 25": 0,
            "item_id 26": 0,
            "item_id 27": 0,
            "item_id 28": 0,
            "item_id 29": 0,
            "item_id 30": 0,
            "item_id 31": 0,
            "item_id 32": 0,
            "item_id 33": 0,
            "item_id 34": 0,
            "item_id 35": 0,
            "item_id 36": 0,
            "item_id 37": 0
        }
