from lxml import html


def build_tags_to_unwrap_map():
    """Create a mapping of HTML tag categories to their associated elements.

    Returns:
        dict: A dictionary where keys are category names (str) and values are lists
        of HTML tag names (str) belonging to those categories. Tags in these categories
        typically don't require standalone presentation and can be safely unwrapped.
    """
    return {
        # Inline text semantics tags from HTML5 specification
        "inline_text_semantics": [
            "a",
            "abbr",
            "b",
            "bdi",
            "bdo",
            "br",
            "cite",
            "code",
            "data",
            "dfn",
            "em",
            "i",
            "kbd",
            "mark",
            "q",
            "rp",
            "rt",
            "ruby",
            "s",
            "samp",
            "small",
            "span",
            "strong",
            "sub",
            "sup",
            "time",
            "u",
            "var",
            "wbr",
        ],
        # Tags related to edit demarcation (note: colon in key is preserved as per original)
        "demarcating_edits:": ["ins"],
    }


def get_all_tags_to_unwrap():
    """Compile a consolidated list of all HTML tags that should be unwrapped.

    Returns:
        list: A flattened list of all HTML tag names (str) from all categories
        in the tags-to-unwrap mapping.
    """
    all_tags = []
    for tag_list in build_tags_to_unwrap_map().values():
        all_tags.extend(tag_list)
    return all_tags


def unwrap_all_tags(root: html.HtmlElement) -> html.HtmlElement:
    """Remove specified HTML tags while preserving their contents.

    Processes the HTML tree in-place to unwrap tags from the pre-defined list,
    maintaining the document structure without presentational markup.

    Args:
        root (html.HtmlElement): The root element of the HTML tree to process

    Returns:
        html.HtmlElement: The modified HTML tree root (modified in-place)
    """
    # Get complete list of tags to unwrap
    all_tags = get_all_tags_to_unwrap()

    # Process each tag type sequentially
    for tag in all_tags:
        # Find all elements with current tag name in the tree
        for element in root.findall(f".//{tag}"):
            # Remove the element tag while preserving its contents
            element.drop_tag()

    return root
