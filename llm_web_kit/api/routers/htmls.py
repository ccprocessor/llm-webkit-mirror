"""HTML 处理路由.

提供 HTML 解析、内容提取等功能的 API 端点。
"""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from ..dependencies import get_logger, get_settings
from ..models.request import HTMLParseRequest
from ..models.response import HTMLParseResponse
from ..services.html_service import HTMLService

logger = get_logger(__name__)
settings = get_settings()

router = APIRouter()


@router.post('/html/parse', response_model=HTMLParseResponse)
async def parse_html(
    request: HTMLParseRequest,
    html_service: HTMLService = Depends(HTMLService)
):
    """解析 HTML 内容.

    接收 HTML 字符串并返回解析后的结构化内容。
    """
    try:
        logger.info(f'开始解析 HTML，内容长度: {len(request.html_content) if request.html_content else 0}')

        result = await html_service.parse_html(
            html_content=request.html_content,
            url=request.url,
            options=request.options
        )

        return HTMLParseResponse(
            success=True,
            data=result,
            message='HTML 解析成功'
        )
    except Exception as e:
        logger.error(f'HTML 解析失败: {str(e)}')
        raise HTTPException(status_code=500, detail=f'HTML 解析失败: {str(e)}')


@router.post('/html/upload')
async def upload_html_file(
    file: UploadFile = File(...),
    html_service: HTMLService = Depends(HTMLService)
):
    """上传 HTML 文件进行解析.

    支持上传 HTML 文件，自动解析并返回结果。
    """
    try:
        if not file.filename.endswith(('.html', '.htm')):
            raise HTTPException(status_code=400, detail='只支持 HTML 文件')

        content = await file.read()
        html_content = content.decode('utf-8')

        logger.info(f'上传 HTML 文件: {file.filename}, 大小: {len(content)} bytes')

        result = await html_service.parse_html(html_content=html_content)

        return HTMLParseResponse(
            success=True,
            data=result,
            message='HTML 文件解析成功',
            filename=file.filename
        )
    except Exception as e:
        logger.error(f'HTML 文件解析失败: {str(e)}')
        raise HTTPException(status_code=500, detail=f'HTML 文件解析失败: {str(e)}')


@router.get('/html/status')
async def get_service_status():
    """获取服务状态.

    返回 HTML 处理服务的当前状态信息。
    """
    return {
        'service': 'HTML Processing Service',
        'status': 'running',
        'version': '1.0.0'
    }
