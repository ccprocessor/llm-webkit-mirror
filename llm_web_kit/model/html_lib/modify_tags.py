from lxml import html


def wrap_bare_text(root: html.HtmlElement) -> html.HtmlElement:
    for elem in root.iter():
        # continue if the element has no child
        if len(elem) == 0:
            continue
        else:
            # check if the element has text and tail
            if elem.text and elem.text.strip():
                # wrap the text in a span tag
                span = html.Element('span')
                span.text = elem.text
                elem.text = ''
                elem.insert(0, span)
            for child in elem:
                if child.tail and child.tail.strip():
                    # wrap the tail in a span tag
                    span = html.Element('span')
                    span.text = child.tail
                    child.tail = ''
                    child.addnext(span)
    return root


def unwrap_single_child_tag(root: html.HtmlElement) -> html.HtmlElement:

    def merge_class(A_elem: html.HtmlElement, B_elem: html.HtmlElement) -> str:
        A_str = A_elem.get('class', '').strip()
        B_str = B_elem.get('class', '').strip()
        if A_str and B_str:
            return f'{A_str}|{B_str}'
        if A_str:
            return A_str
        if B_str:
            return B_str
        return ''

    for tag in root.iter():
        children = list(tag.getchildren())
        if len(children) == 1 and tag.getparent() is not None:
            child = children[0]
            child.set('class', merge_class(tag, child))
            tag.drop_tag()
    return root
