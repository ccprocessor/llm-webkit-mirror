import json
import os
import sys
from pathlib import Path

import click
from loguru import logger

from llm_web_kit.extractor.extractor_chain import ExtractSimpleFactory
from llm_web_kit.extractor.html.extractor import HTMLFileFormatExtractor
from llm_web_kit.input.datajson import DataJson
from llm_web_kit.config.cfg_reader import load_pipe_tpl

@click.command()
@click.option(
    '-i',
    '--input',
    'input_path',
    type=click.Path(exists=True),
    required=True,
    help='Input JSON file path containing HTML data',
)
@click.option(
    '-o',
    '--output',
    'output_path',
    type=click.Path(),
    help='Output file path (optional, defaults to stdout)',
)
@click.option(
    '-d',
    '--debug',
    'debug_mode',
    is_flag=True,
    help='Enable debug mode for detailed logging',
)

def main_cli(input_path, output_path, debug_mode):
    # 遍历input_path
    file_list = os.listdir(input_path)
    file_path = ''
    for filename in file_list:
        file_path = os.path.join(input_path, filename)
        cli(file_path, output_path, debug_mode)

def cli(input_path, output_path, debug_mode):
    """Process HTML content from JSON input using magic-html."""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            input_data = json.load(f)

        if 'html' not in input_data:
            if 'path' in input_data:
                html_path = Path(input_data['path'])

                if not html_path.exists():
                    raise FileNotFoundError(f'HTML file not found: {html_path}')

                try:
                    with open(html_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    input_data = {'html': html_content, **{k: v for k, v in input_data.items() if k != 'path'}}
                    logger.debug(f'Successfully read HTML from: {html_path}')
                except Exception as e:
                    raise Exception(f'Failed to read HTML file at {html_path}: {str(e)}')
            else:
                raise ValueError('Input JSON must contain either html or path field')
        
        # jsonl
        # config = load_pipe_tpl('html')
        # extractor = ExtractSimpleFactory.create(config)
        extractor = HTMLFileFormatExtractor({})
        data_e = extractor.extract(DataJson(input_data))
        # main_html = data_e.get_magic_html()
        # cur_path = os.path.join(output_path, 'main_html', input_path.split('/')[-1].split('.')[0]+'.html')
        # with open(cur_path, 'w', encoding="utf-8") as f:
        #     f.write(main_html)
        output_json = data_e.to_json()
        
        
        if len(data_e.to_dict()['content_list'][0]) == 0:
            return
        # md
        output_md = data_e.get_content_list().to_nlp_md()
        
        # md_data_e = md_extractor.extract(DataJson(input_data))
        # output_md = md_data_e.get_content_list().to_mm_md()
        if output_path:
            # jsonl
            jsonl_output_path = os.path.join(output_path, 'jsonl', input_path.split('/')[-1])
            jsonl_output_path = Path(jsonl_output_path)
            jsonl_output_path.parent.mkdir(parents=True, exist_ok=True)

            print('jsonl: ', jsonl_output_path)
            with open(jsonl_output_path, 'w', encoding='utf-8') as f:
                f.write(output_json)
           
            # markdown
            md_output_path = os.path.join(output_path, 'md', input_path.split('/')[-1].split('.')[0]+'.md')
            md_output_path = Path(md_output_path)
            md_output_path.parent.mkdir(parents=True, exist_ok=True)
            print('md: ', md_output_path)
            with open(md_output_path, 'w', encoding='utf-8') as f:
                f.write(output_md)
            logger.info(f'Results written to {output_path}')
        else:
            print(output_json)

    except Exception as e:
        logger.error(f'Error processing file: {str(e)}')
        if debug_mode:
            logger.exception(e)
        sys.exit(1)


if __name__ == '__main__':
    # input_path = r'/home/douxiaofeng/Desktop/CC/benchmark_data/output_jsonl'
    # output_path = r'/home/douxiaofeng/Desktop/CC/benchmark_data/out_content_list'
    main_cli()

