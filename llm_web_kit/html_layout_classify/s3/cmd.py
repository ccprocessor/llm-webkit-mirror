import ast
import json
import re
from typing import Union

try:
    import orjson
except Exception:
    orjson = None

_surrogates_re = r'[\ud800-\udfff]'


def json_dumps(d: dict, **kwargs) -> str:
    if not kwargs and orjson:
        try:
            return orjson.dumps(d).decode('utf-8')
        except Exception:
            pass
    return json.dumps(d, ensure_ascii=False, **kwargs)


def json_loads(s: Union[str, bytes], **kwargs) -> dict:
    if not kwargs and orjson:
        try:
            return orjson.loads(s)
        except Exception:
            pass
    try:
        return json.loads(s, **kwargs)
    except Exception as e:
        if 'enclosed in double quotes' not in str(e):
            raise e
        if isinstance(s, bytes):
            s = s.decode('utf-8')
        else:
            s = str(s)
        return ast.literal_eval(s)


def json_encode(d: dict, end='\n', **kwargs) -> bytes:
    return str_encode(json_dumps(d, **kwargs) + end)


def str_encode(s: str) -> bytes:
    # try remote special characters
    s = re.sub(_surrogates_re, '\ufffd', s)

    try:
        return s.encode('utf-8')
    except UnicodeEncodeError as e:
        debug_start = max(0, e.start - 1000)
        debug_end = min(len(s), e.end + 1000)
        print(f'{debug_start=}, {debug_end=}, debug_s={s[debug_start:debug_end]}')
        raise

# def json_print(obj):
#     if isinstance(obj, list) and len(obj):
#         return json_print(obj[0])
#     if isinstance(obj, bytes):
#         return json_print(obj.decode('utf-8'))
#     if isinstance(obj, str):
#         return json_print(json_loads(obj))
#     if isinstance(obj, dict):
#         return print(json_dumps(obj, indent=2))
#
#     from .row_fallback import Row
#
#     if isinstance(obj, Row) and 'value' in obj:
#         return json_print(obj.value)
#
#     print(obj)
#
# def _format_datetime(dt):
#     if not dt:
#         return ''
#     dt = dt.replace(tzinfo=timezone.utc).astimezone(tz=None)  # localtime
#     return dt.strftime('%y-%m-%d %H:%M:%S %Z')
#
#
# def _format_size(size):
#     if size is None:
#         return ''
#     size = str(size)
#     parts = []
#     while len(size):
#         part_size = 3
#         if not parts and len(size) % part_size:
#             part_size = len(size) % part_size
#         parts.append(size[:part_size])
#         size = size[part_size:]
#     return ','.join(parts)
#
#
# def _format_detail(detail):
#     path, obj = detail
#     if path.endswith('/'):
#         return f"{'DIR'.rjust(53)}  {path}"
#     tm = _format_datetime(obj.get('LastModified'))
#     sz = _format_size(obj.get('Size') or obj.get('ContentLength', 0))
#     owner = obj.get('Owner', {}).get('ID', '')
#     return f'{tm} {sz.rjust(15)} {owner.rjust(15)}  {path}'
#
#
# def head(path):
#     obj_head = head_s3_object_with_retry(path)
#     if obj_head is not None:
#         print(json_dumps(obj_head, indent=2, default=str))
#
#
# def cat(path, limit=1, show_loc=False):
#     if '?bytes=' in path:
#         row = read_s3_row(path)
#         if row is not None:
#             if show_loc:
#                 print(row.loc)
#             json_print(row)
#         return
#     for row in read_s3_rows(path, use_stream=True, limit=limit):
#         if show_loc:
#             print(row.loc)
#         json_print(row)
#
#
# def ls(path, limit=100):
#     for obj in list_s3_objects(path, limit=limit):
#         print(obj)
#
#
# def ls_r(path, limit=100):
#     for item in list_s3_objects(path, True, True, limit):
#         print(item)
#
#
# def ll(path, limit=100):
#     for detail in list_s3_objects_detailed(path, limit=limit):
#         print(_format_detail(detail))
#
#
# def ll_r(path, limit=100):
#     for detail in list_s3_objects_detailed(path, True, True, limit):
#         print(_format_detail(detail))
#
#
# def download(path):
#     print(get_s3_presigned_url(path))
