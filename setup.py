from setuptools import find_packages, setup

from llm_web_kit.libs.version import __version__


def parse_requirements(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    requires = []

    for line in lines:
        if line and line.startswith('#'):
            continue
        if 'http' in line:
            pkg_name_without_url = line.split('@')[0].strip()
            requires.append(pkg_name_without_url)
        else:
            requires.append(line)

    return requires


if __name__ == '__main__':
    setup(
        name='llm_web_kit',
        version=__version__,
        description='LLM Web Kit for processing web content',
        packages=find_packages(exclude=['tests*']),
        install_requires=parse_requirements('requirements/runtime.txt'),
        extras_require={
            'dev': parse_requirements('requirements/dev.txt'),
        },
        url='https://github.com/ccprocessor/llm_web_kit',
        python_requires='>=3.10, <3.14',
        entry_points={
            'console_scripts': [
                'magic-html = llm_web_kit.tools.cli:cli'
            ],
        },
        include_package_data=True,
        package_data={
            'llm_web_kit': ['**/*.*'],
        },
        zip_safe=False,
    )
