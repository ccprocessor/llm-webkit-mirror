import os
import subprocess


def get_version():
    command = ['git', 'describe', '--tags']
    try:
        version = subprocess.check_output(command).decode().strip()
        version_parts = version.split('-')
        if len(version_parts) > 1 and version_parts[0].startswith('llm-web-kit'):
            return version_parts[1]
        else:
            raise ValueError(f'Invalid version tag {version}. Expected format is llm-web-kit-<version>-released.')
    except Exception as e:
        print(e)
        return '0.0.0'


def write_version_to_commons(version):
    commons_path = os.path.join(os.path.dirname(__file__), 'llm_web_kit', 'libs', 'version.py')
    with open(commons_path, 'w') as f:
        f.write(f'__version__ = "{version}"\n')


if __name__ == '__main__':
    version_name = get_version()
    write_version_to_commons(version_name)
