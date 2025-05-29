"""
实现一个flask的server,实现：
1. 启动的时候，接受一个命令行参数 --layout_sample_dir，表示layout_sample_dir路径。扫描这个路径下所有.jsonl文件，保存他们的绝对路径。把这些路径放到一个队列里。
2. 实现一个http get接口，每次返回队列里的一个路径，并从队列里删除该路径。被删除的路径保存到另外一个dict里，value是个当时的时间start_tm。用来记录未来处理是否成功。
3. 实现一个http post接口，接受一个路径，和对这个路径的处理结果SUCC|FAIL, 和一条msg。把这3条信息存到dict的vlaue里,加上end_tm。
4. 实现一个http get，返还一个html表格。 显示queue里总路径，dict里的路径，和处理结果。显示处理总进度=dict里处理成功的路径/queue里总路径+dict里总的路径。

"""
import json
import os
import queue
import sys
from datetime import datetime
from pathlib import Path
from queue import Queue
from threading import Lock

import click
from flask import Flask, jsonify, render_template_string, request
from loguru import logger

app = Flask(__name__)

# Global variables

file_queue = Queue()
processed_files = {}
total_files = 0
processed_files_lock = Lock()
succ_count = 0  # 处理成功的计数


# Queue persistence file path
QUEUE_FILE = os.path.expanduser('~/.page_classify_queue')

# HTML template for status page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Processing Status</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid black; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .pagination { margin: 20px 0; }
        .pagination a {
            padding: 8px 16px;
            text-decoration: none;
            border: 1px solid #ddd;
            margin: 0 4px;
        }
        .pagination a.active {
            background-color: #4CAF50;
            color: white;
        }
        .pagination a:hover:not(.active) {background-color: #ddd;}
    </style>
</head>
<body>
    <h2>Processing Status</h2>
    <p>Progress: {{ progress }}%</p>
    <h3>Queue Status:</h3>
    <p>Files succ processing: {{ succ_count }}</p>
    <p>Files remaining in queue: {{ queue_length }}</p>
    <p>Files currently processing: {{ processing_count }}</p>
    <h3>Processed Files:</h3>
    <table>
        <tr>
            <th>File Path</th>
            <th>Status</th>
            <th>Message</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Duration</th>
        </tr>
        {% for path, info in processed_files.items() %}
        <tr>
            <td>{{ path }}</td>
            <td>{{ info.get('status', '') }}</td>
            <td>{{ info.get('msg', '') }}</td>
            <td>{{ info.get('start_tm', '') }}</td>
            <td>{{ info.get('end_tm', '') }}</td>
            <td>{{ info.get('duration', '') }}</td>
        </tr>
        {% endfor %}
    </table>
    <div class="pagination">
        {% if page > 1 %}
            <a href="?page={{ page-1 }}">&laquo; Previous</a>
        {% endif %}
        {% for p in range(1, total_pages + 1) %}
            <a href="?page={{ p }}" {% if p == page %}class="active"{% endif %}>{{ p }}</a>
        {% endfor %}
        {% if page < total_pages %}
            <a href="?page={{ page+1 }}">Next &raquo;</a>
        {% endif %}
    </div>
</body>
</html>
"""


def load_processed_files():
    """Load processing files from persistence file."""
    global processed_files, succ_count
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, 'r') as f:
            saved_files = json.load(f)
            # Only load files that are still in PROCESSING status
            processed_files = {
                path: info for path, info in saved_files.items()
                if info.get('status') == 'PROCESSING'
            }
            for _, info in saved_files.items():
                if info.get('status') == 'SUCC':
                    succ_count += 1


def clear_processed_files():
    """Clear processed files from persistence file."""
    if os.path.exists(QUEUE_FILE):
        os.remove(QUEUE_FILE)


def save_processed_files():
    """Save processed files to persistence file."""
    with open(QUEUE_FILE, 'w') as f:
        json.dump(processed_files, f)


def __init_queue(layout_sample_dir, reset):
    """Initialize queue with .jsonl files from the given directory."""
    global file_queue, total_files

    layout_dir = Path(layout_sample_dir)
    if not layout_dir.exists():
        print(f'Error: Directory {layout_sample_dir} does not exist')
        sys.exit(1)

    # Load processed files first to exclude processing files
    if reset:
        clear_processed_files()
    load_processed_files()

    # Get set of files currently being processed
    processing_files = {path for path, info in processed_files.items()
                       if info.get('status') == 'PROCESSING'}

    layout_dir = Path(layout_sample_dir)
    for file_path in layout_dir.rglob('*.jsonl'):
        file_path_str = str(file_path.resolve())  # 使用resolve()获取文件的绝对路径
        # Only add files that are not currently being processed
        if file_path_str not in processing_files:
            file_queue.put(file_path_str)

    total_files = file_queue.qsize()


# Add lock as a global variable at module level


@app.route('/get_file', methods=['GET'])
def get_file():
    global file_queue, processed_files, processed_files_lock

    with processed_files_lock:
        # Check for timed out files before getting next file
        current_time = datetime.now()
        timed_out_files = []
        for file_path, info in processed_files.items():
            if info['status'] == 'PROCESSING':
                start_time = datetime.strptime(info['start_tm'], '%Y-%m-%d %H:%M:%S')
                duration = (current_time - start_time).total_seconds()
                if duration > app.config['TIMEOUT']:
                    logger.info(f'File {file_path} timed out, adding back to queue')
                    timed_out_files.append(file_path)  # 超时的文件，重新加入队列
                    file_queue.put(file_path)

        # Remove timed out files from processed_files
        for file_path in timed_out_files:
            del processed_files[file_path]

        try:
            file_path = file_queue.get(block=False)
        except queue.Empty:  # queue.get() raises queue.Empty when empty, not IndexError
            logger.error('No more files in queue')
            return jsonify({'file_path': ''})

        processed_files[file_path] = {
            'start_tm': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'PROCESSING'
        }

        # Save updated processed files
        save_processed_files()

        logger.info(f'get layout classify file: {file_path}')
        return jsonify({'file_path': file_path})


@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.get_json()
    file_path = data['file_path']
    status = data['status']
    msg = data.get('msg', '')  # Optional message parameter
    """Update processing status for a file."""
    if file_path not in processed_files:
        return jsonify({'error': 'File not found in processed list'})

    end_time = datetime.now()
    start_time = datetime.strptime(processed_files[file_path]['start_tm'], '%Y-%m-%d %H:%M:%S')
    duration = end_time - start_time

    processed_files[file_path].update({
        'status': status,
        'msg': msg,
        'end_tm': end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'duration': str(duration)
    })

    # Save updated processed files
    save_processed_files()
    logger.info(f'update layout classify status: {file_path} {status} {msg}')
    return jsonify({'status': 'success'})


@app.route('/index', methods=['GET'])
def index():
    """Get processing status page."""
    global succ_count
    success_count = sum(1 for info in processed_files.values()
                       if info.get('status') == 'SUCC')
    processing_count = sum(1 for info in processed_files.values()
                         if info.get('status') == 'PROCESSING')
    error_count = sum(1 for info in processed_files.values()
                    if info.get('status') == 'FAIL')
    _succ_count = succ_count + sum(1 for info in processed_files.values()
                                 if info.get('status') == 'SUCC')
    total = total_files
    progress = (success_count / total * 100) if total > 0 else 0

    # Get page parameter from request, default to 1
    page = request.args.get('page', 1, type=int)
    per_page = 50

    # Get paginated list of processed files
    items = list(processed_files.items())
    total_pages = (len(items) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    current_items = dict(items[start:end])

    return render_template_string(
        HTML_TEMPLATE,
        queue_length=file_queue.qsize(),
        processed_files=current_items,
        progress=round(progress, 2),
        page=page,
        total_pages=total_pages,
        processing_count=processing_count,
        error_count=error_count,
        succ_count=_succ_count
    )


@click.command()
@click.option('--layout_sample_dir', required=True, help='Directory containing layout sample files')
@click.option('--port', default=5000, help='Port to run the server on')
@click.option('--host', default='0.0.0.0', help='Host IP to run the server on')
@click.option('--timeout', default=10, help='timeout to process one file')
@click.option('--reset', is_flag=True, default=False, help='Reset cached files')
def run_server(layout_sample_dir, port, host, timeout, reset):
    """Initialize and run the server."""
    __init_queue(layout_sample_dir, reset)
    app.config['TIMEOUT'] = timeout
    app.run(host=host, port=port)


if __name__ == '__main__':
    run_server()
