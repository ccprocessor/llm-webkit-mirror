from setuptools import find_packages, setup


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
        version='3.1.0',
        description='LLM Web Kit for processing web content',
        packages=find_packages(exclude=['tests*']),
        install_requires=parse_requirements('requirements/runtime.txt') + parse_requirements('requirements/dev.txt'),  # 项目依赖的第三方库
        url='https://github.com/ccprocessor/llm_web_kit',
        python_requires='>=3.10, <3.14',
        include_package_data=True,  # 是否包含非代码文件，如数据文件、配置文件等
        zip_safe=False,  # 是否使用 zip 文件格式打包，一般设为 False
    )
