import re


def convert_to_standard_latex(text):
    # 创建替换规则字典
    replacements = {
        # 向量表示
        r'\\vc{([^}]*)}': r'\\mathbf{\1}',
        # 雅可比矩阵
        r'\\jacm{([^}]*)}': r'D\1',
        # 其他常见宏的替换
        r'\\diff{([^}]*)}{([^}]*)}': r'\\frac{\\mathrm{d} \1}{\\mathrm{d} \2}',
        r'\\pdiff{([^}]*)}{([^}]*)}': r'\\frac{\\partial \1}{\\partial \2}',
        r'\\norm{([^}]*)}': r'\\|\1\\|',
        # 积分宏替换 (简化版，根据需要可以扩展)
        r'\\lint{([^}]*)}{([^}]*)}': r'\\int_{\1} \2 \\cdot d\\mathbf{s}',
        r'\\slint{([^}]*)}{([^}]*)}': r'\\int_{\1} \2 \\,ds',
        # 默认字母替换
        r'\\dlvf': r'\\mathbf{F}',
        r'\\dlc': r'C',
        r'\\dlsi': r'f',
        # 实数集合符号
        r'\\R': r'\\mathbb{R}',
    }
    # 应用所有替换规则
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)
    return text
