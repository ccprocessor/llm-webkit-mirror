from lxml import html


def build_tags_to_unwrap_map():
    return {
        'inline_text_semantics': [
            'a',
            'abbr',
            'b',
            'bdi',
            'bdo',
            'br',
            'cite',
            'code',
            'data',
            'dfn',
            'em',
            'i',
            'kbd',
            'mark',
            'q',
            'rp',
            'rt',
            'ruby',
            's',
            'samp',
            'small',
            'span',
            'strong',
            'sub',
            'sup',
            'time',
            'u',
            'var',
            'wbr',
        ],
        'demarcating_edits:': ['ins'],
    }


def get_all_tags_to_unwrap():
    all_tags = []
    for tag_list in build_tags_to_unwrap_map().values():
        all_tags.extend(tag_list)
    return all_tags


def unwrap_all_tags(root: html.HtmlElement) -> html.HtmlElement:
    all_tags = get_all_tags_to_unwrap()
    for tag in all_tags:
        for element in root.findall(f'.//{tag}'):
            element.drop_tag()
    return root
