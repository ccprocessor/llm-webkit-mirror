from lxml import html

from llm_web_kit.model.html_lib.base_func import extract_tag_text


def merge_list(root: html.HtmlElement) -> html.HtmlElement:
    # merge ul ol and dl
    list_tag_names = ['ul', 'ol', 'dl']
    for tag in list_tag_names:
        for list_elem in root.findall(f'.//{tag}'):
            list_inner_text = extract_tag_text(list_elem)
            # clean up the list_elem
            for child in list_elem.getchildren():
                if child.getparent() is not None:
                    child.drop_tree()
            list_elem.text = list_inner_text
    return root
