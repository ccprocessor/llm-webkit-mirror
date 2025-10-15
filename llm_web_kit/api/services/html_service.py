"""HTML 处理服务.

桥接原有项目的 HTML 解析和内容提取功能，提供统一的 API 接口。
"""

from typing import Any, Dict, Optional

import httpx

from llm_web_kit.api.dependencies import (get_inference_service, get_logger,
                                          get_settings)
from llm_web_kit.simple import extract_content_from_main_html

logger = get_logger(__name__)
settings = get_settings()


class HTMLService:
    """HTML 处理服务类."""

    def __init__(self):
        """初始化 HTML 服务."""
        # 目前使用简化管线；使用全局单例的 InferenceService，避免重复初始化模型
        try:
            self._inference_service = get_inference_service()
        except Exception as e:
            logger.warning(f'InferenceService 获取失败（将在首次调用时再尝试）：{e}')
            self._inference_service = None

    def _init_components(self):
        """兼容保留（当前未使用）"""
        return None

    async def parse_html(
        self,
        html_content: Optional[str] = None,
        url: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """解析 HTML 内容."""
        try:
            if not html_content and url:
                logger.info(f'HTML 内容为空，尝试从 URL 爬取: {url}')
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.post(settings.crawl_url, json={'url': url}, timeout=60)
                        response.raise_for_status()
                        data = response.json()
                        html_content = data.get('html')
                        if not html_content:
                            raise ValueError('爬取成功，但未返回 HTML 内容')
                        logger.info(f'URL 爬取成功，内容长度: {len(html_content)}')
                except httpx.RequestError as exc:
                    logger.error(f"调用爬虫服务失败: {exc}")
                    raise ValueError(f"无法从 URL 爬取内容: {exc}")
                except Exception as e:
                    logger.error(f'爬取或解析爬取内容失败: {e}')
                    raise ValueError(f'处理爬取内容时发生错误: {e}')

            if not html_content:
                raise ValueError('必须提供 HTML 内容或有效的 URL')

            # 延迟导入，避免模块导入期异常导致服务类不可用
            try:
                from llm_web_kit.input.pre_data_json import (PreDataJson,
                                                             PreDataJsonKey)
                from llm_web_kit.main_html_parser.parser.tag_mapping import \
                    MapItemToHtmlTagsParser
                from llm_web_kit.main_html_parser.simplify_html.simplify_html import \
                    simplify_html
            except Exception as import_err:
                logger.error(f'依赖导入失败: {import_err}')
                raise

            # 简化网页
            try:
                simplified_html, typical_raw_tag_html = simplify_html(html_content)
            except Exception as e:
                logger.error(f'简化网页失败: {e}')
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
            main_html = pre_data[PreDataJsonKey.TYPICAL_MAIN_HTML]
            mm_nlp_md = extract_content_from_main_html(url, main_html, 'mm_md', use_raw_image_url=True)
            pre_data['markdown'] = mm_nlp_md
            # 将 PreDataJson 转为标准 dict，避免响应模型校验错误
            return dict(pre_data.items())

        except Exception as e:
            logger.error(f'HTML解析失败: {e}')
            raise

    async def _parse_with_model(self, html_content: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if self._inference_service is None:
            self._inference_service = get_inference_service()
        return await self._inference_service.inference(html_content, options or {})


if __name__ == '__main__':
    import asyncio

    # 重新导入以确保加载最新的代码，绕过缓存问题
    from llm_web_kit.api.dependencies import get_settings
    settings = get_settings()

    async def main():
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.crawl_url, json={'url': 'https://aws.amazon.com/what-is/retrieval-augmented-generation/'}, timeout=60)
            response.raise_for_status()
            data = response.json()
            html_content = data.get('html')
            print(html_content)

    asyncio.run(main())
