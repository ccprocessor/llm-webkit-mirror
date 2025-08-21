import json
import sys
from pathlib import Path

import click
from loguru import logger

from llm_web_kit.simple import extract_content_from_html_with_magic_html


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

        output_json = extract_content_from_html_with_magic_html(input_data['url'], input_data['html'], 'json')
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_json)
            logger.info(f'Results written to {output_path}')
        else:
            print(output_json)

    except Exception as e:
        logger.error(f'Error processing file: {str(e)}')
        if debug_mode:
            logger.exception(e)
        sys.exit(1)


if __name__ == '__main__':
    cli()
