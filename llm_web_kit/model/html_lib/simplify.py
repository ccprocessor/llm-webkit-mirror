from lxml import html

from llm_web_kit.model.html_lib.base_func import document_fromstring, get_title
from llm_web_kit.model.html_lib.merge_tags import merge_list
from llm_web_kit.model.html_lib.modify_tags import (unwrap_single_child_tag,
                                                    wrap_bare_text)
from llm_web_kit.model.html_lib.remove_tags import (
    remove_all_tags, remove_blank_tags_recursive, remove_invisible_tags)
from llm_web_kit.model.html_lib.unwrap_tags import unwrap_all_tags


def general_simplify(root: html.HtmlElement) -> tuple[str, html.HtmlElement]:
    # get the title of the html page
    title = get_title(root)

    # remove all invisible tags
    root = remove_invisible_tags(root)

    # unwrap all tags we consider can directly unwrap
    # unwrap means remove the tag and keep the children
    root = unwrap_all_tags(root)

    # wrap all bare text in span tags
    # the bare text means the tag.text and tag.child.tail is not blank and len(tag) > 0
    # <tag>
    #    tag.text <!-- this is bare text -->
    #    <child>
    #        text <!-- this is not bare text -->
    #    </child>
    #    child.tail <!-- this is bare text -->
    # </tag>
    root = wrap_bare_text(root)

    # remove all tags (and it's children) we consider can directly remove
    root = remove_all_tags(root)

    # extract text from all children of list tags and set the text as the text of the list tags
    root = merge_list(root)

    # remove all tags
    root = remove_blank_tags_recursive(root)

    # unwrap all tags have only one child
    root = unwrap_single_child_tag(root)

    return title, root


def general_simplify_html_str(html_str: str) -> str:
    root = document_fromstring(html_str)
    _, simplified_root = general_simplify(root)
    simplified_html_str = html.tostring(simplified_root)
    return simplified_html_str.decode('utf-8')
