import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from llm_web_kit.tools.cli import cli

# 获取测试资源文件的根目录
ASSETS_DIR = Path(__file__).parent / 'assets'


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def json_with_html_path():
    return ASSETS_DIR / 'input_with_html.json'


@pytest.fixture
def json_with_file_path():
    return ASSETS_DIR / 'input_with_path.json'


@pytest.fixture
def json_with_non_exist_path():
    return ASSETS_DIR / 'nonexistent.json'


@pytest.fixture
def invalid_json_path():
    return ASSETS_DIR / 'invalid.json'


@pytest.fixture
def empty_json_path():
    return ASSETS_DIR / 'empty.json'


class TestCliSDK:
    def test_process_direct_html_input(self, runner, json_with_html_path, tmp_path):
        """测试处理直接包含HTML的JSON输入."""
        output_file = tmp_path / 'output.json'
        result = runner.invoke(cli, ['-i', str(json_with_html_path), '-o', str(output_file)])

        assert result.exit_code == 0
        assert output_file.exists()

        with open(output_file, 'r', encoding='utf-8') as f:
            output_data = json.load(f)

        assert 'content_list' in output_data
        assert isinstance(output_data['content_list'], list)
        assert len(output_data['content_list']) > 0

    def test_process_html_file_path(self, runner, json_with_file_path, tmp_path):
        """测试处理包含HTML文件路径的JSON输入."""
        output_file = tmp_path / 'output.json'
        result = runner.invoke(cli, ['-i', str(json_with_file_path), '-o', str(output_file)])

        assert result.exit_code == 0
        assert output_file.exists()

        with open(output_file, 'r', encoding='utf-8') as f:
            output_data = json.load(f)

        assert 'content_list' in output_data
        assert isinstance(output_data['content_list'], list)
        assert len(output_data['content_list']) > 0

    def test_stdout_output(self, runner, json_with_html_path):
        """测试输出到标准输出."""
        result = runner.invoke(cli, ['-i', str(json_with_html_path)])

        assert result.exit_code == 0
        assert result.output

        output_data = json.loads(result.output)
        assert 'content_list' in output_data
        assert isinstance(output_data['content_list'], list)

    def test_debug_mode(self, runner, json_with_html_path):
        """测试调试模式."""
        result = runner.invoke(cli, ['-i', str(json_with_html_path), '-d'])
        assert result.exit_code == 0

    def test_invalid_input_path(self, runner, json_with_non_exist_path):
        """测试无效的输入文件路径."""
        result = runner.invoke(cli, ['-i', str(json_with_non_exist_path)])
        assert result.exit_code == 2
        assert "Error: Invalid value for '-i'" in result.output

    def test_invalid_json_format(self, runner, invalid_json_path):
        """测试无效的JSON格式."""
        result = runner.invoke(cli, ['-i', str(invalid_json_path)])
        assert result.exit_code == 1

    def test_missing_required_fields(self, runner, empty_json_path):
        """测试缺少必需字段的JSON."""
        result = runner.invoke(cli, ['-i', str(empty_json_path)], catch_exceptions=False)
        assert result.exit_code == 1

    def test_nonexistent_html_path(self, runner, tmp_path):
        """测试JSON中包含不存在的HTML文件路径."""
        data = {'path': str(tmp_path / 'nonexistent.html')}
        json_file = tmp_path / 'invalid_path.json'
        json_file.write_text(json.dumps(data), encoding='utf-8')

        result = runner.invoke(cli, ['-i', str(json_file)], catch_exceptions=False)
        assert result.exit_code == 1

    def test_invalid_output_path(self, runner, json_with_html_path, tmp_path):
        """测试无效的输出路径."""
        invalid_output = tmp_path / 'nonexistent' / 'output.json'
        result = runner.invoke(cli, ['-i', str(json_with_html_path), '-o', str(invalid_output)])

        assert result.exit_code == 0
        assert invalid_output.exists()


if __name__ == '__main__':
    pytest.main()
