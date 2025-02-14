from lxml import html


def wrap_bare_text(root: html.HtmlElement) -> html.HtmlElement:
    """Wrap bare text in HTML elements with <span> tags.

    This function traverses all elements in the HTML structure and wraps
    any text content found in elements with <span> tags. It also wraps
    tail text (text following an element) in <span> tags.

    Args:
        root (html.HtmlElement): The root HTML element to process.

    Returns:
        html.HtmlElement: The modified root element with text wrapped in <span> tags.

    Example:
        Input:
        <div>Hello <p>World</p>!</div>
        Output:
        <div><span>Hello </span><p>World</p><span>!</span></div>
    """
    for elem in root.iter():
        # Skip elements with no children
        if len(elem) == 0:
            continue
        else:
            # Check and wrap the element's text content with <span>
            if elem.text and elem.text.strip():
                span = html.Element("span")
                span.text = elem.text
                elem.text = ""
                elem.insert(0, span)
            # Check and wrap the tail text of each child element with <span>
            for child in elem:
                if child.tail and child.tail.strip():
                    span = html.Element("span")
                    span.text = child.tail
                    child.tail = ""
                    child.addnext(span)
    return root


def unwrap_single_child_tag(root: html.HtmlElement) -> html.HtmlElement:
    """Unwrap elements that only contain a single child tag.

    This function merges the class attributes of parent and child elements
    when a parent element has only one child tag. The parent tag is removed,
    and the class attributes are combined.

    Args:
        root (html.HtmlElement): The root HTML element to process.

    Returns:
        html.HtmlElement: The modified root element with single child tags unwrapped.

    Example:
        Input:
        <div class="parent"><span class="child">Text</span></div>
        Output:
        <span class="parent|child">Text</span>
    """

    def merge_class(A_elem: html.HtmlElement, B_elem: html.HtmlElement) -> str:
        """Merge class attributes of two elements.

        Args:
            A_elem (html.HtmlElement): Parent element.
            B_elem (html.HtmlElement): Child element.

        Returns:
            str: Merged class strings with '|' separator.
        """
        A_str = A_elem.get("class", "").strip()
        B_str = B_elem.get("class", "").strip()
        if A_str and B_str:
            return f"{A_str}|{B_str}"
        if A_str:
            return A_str
        if B_str:
            return B_str
        return ""

    for tag in root.iter():
        children = list(tag.getchildren())
        # Check if the element has only one child and a parent
        if len(children) == 1 and tag.getparent() is not None:
            child = children[0]
            # Merge class attributes
            child.set("class", merge_class(tag, child))
            # Remove the parent tag
            tag.drop_tag()
    return root