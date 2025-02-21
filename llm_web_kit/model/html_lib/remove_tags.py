from lxml import html


def build_tags_to_remove_map() -> dict[str, list[str]]:
    return {
        'document_metadata': ['base', 'head', 'link', 'meta', 'style', 'title'],
        'content_sectioning': ['aside', 'footer', 'header', 'nav'],
        'text_content': ['menu', 'hr'],
        'demarcating_edits': ['del'],
        # "image_and_multimedia": ["audio", "map", "track", "video", "svg"],
        'image_and_multimedia': ['audio', 'map', 'track', 'svg'],
        'interactive': ['dialog'],
        'embed': [
            'embed',
            'fencedframe',
            'iframe',
            'object',
            'picture',
            'portal',
            'source',
        ],
        'script': ['canvas', 'noscript', 'script'],
        'form': [
            'button',
            'datalist',
            'fieldset',
            'form',
            'input',
            'label',
            'legend',
            'meter',
            'optgroup',
            'option',
            'output',
            'progress',
            'select',
            'textarea',
        ],
    }


def all_tag_list_to_remove() -> list[str]:
    all_tag_list = []
    for tag_list in build_tags_to_remove_map().values():
        all_tag_list.extend(tag_list)
    return all_tag_list


def remove_tags(root: html.HtmlElement, tag_type_list: list[str]) -> html.HtmlElement:
    """Remove all tags of a certain type from the html page.

    Args:
        root (etree.ElementTree): The root of the html page
        tag_type (str): The type of tag to remove

    Returns:
        etree.ElementTree: The root of the html page with the tags removed
    """
    tags_to_remove = []
    for tag in tag_type_list:
        for element in root.findall(f'.//{tag}'):
            tags_to_remove.append(element)
    for element in tags_to_remove:
        if element.getparent() is not None:
            element.drop_tree()
    return root


def remove_all_tags(root: html.HtmlElement) -> html.HtmlElement:
    """Remove all tags from the html page.

    Args:
        root (etree.ElementTree): The root of the html page

    Returns:
        etree.ElementTree: The root of the html page with the tags removed
    """
    all_tag_list = all_tag_list_to_remove()
    return remove_tags(root, all_tag_list)


def is_diplay_none(element: html.HtmlElement) -> bool:
    style = element.get('style', '').replace(' ', '').lower()
    if 'display:none' in style:
        return True


def remove_invisible_tags(root: html.HtmlElement) -> html.HtmlElement:
    tags_to_remove = []
    for element in root.iter():
        if is_diplay_none(element):
            tags_to_remove.append(element)
    for element in tags_to_remove:
        if element.getparent() is not None:
            element.drop_tree()
    return root


def is_blank_tag(root: html.HtmlElement) -> bool:
    """Check if a tag is nonblank None blank tags if this is an image or if it
    has text or if it has children with tail text.

    Args:
        tag (html.HtmlElement): The tag to check

    Returns:
        bool: True if the tag is nonblank, False otherwise
    """
    if root.tag == 'img':
        return False
    if root.text and root.text.strip():
        return False
    # check children's tail
    childern_tail = [child.tail for child in root.iterchildren()]
    if any([tail and tail.strip() for tail in childern_tail]):
        return False
    for child in root.iterchildren():
        if not is_blank_tag(child):
            return False
    return True


def remove_blank_tags_recursive(
    root: html.HtmlElement,
) -> tuple[bool, html.HtmlElement]:
    tags_to_remove = []
    for tag in root.iter():
        if is_blank_tag(tag) and tag.getparent() is not None:
            tags_to_remove.append(tag)
    for tag in tags_to_remove:
        if tag.getparent() is not None:
            tag.drop_tree()
    return root
