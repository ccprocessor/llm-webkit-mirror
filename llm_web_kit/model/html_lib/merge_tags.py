from lxml import html

from llm_web_kit.model.html_lib.base_func import extract_tag_text


def merge_list(root: html.HtmlElement) -> html.HtmlElement:
    """Merge list elements (ul, ol, dl) into their respective inner text.

    Args:
        root (html.HtmlElement): The root HTML element from which lists will be merged.

    Returns:
        html.HtmlElement: The modified root HTML element with lists merged.

    Example:
        Input:
        <ul><li>Item 1</li><li>Item 2</li></ul>
        Output:
        <ul>Item 1Item 2</ul>
    """
    # List of target tag names to merge
    list_tag_names = ["ul", "ol", "dl"]

    # Iterate over each target tag name
    for tag in list_tag_names:
        # Find all elements of the current tag in the root element
        for list_elem in root.findall(f".//{tag}"):
            # Extract the inner text of the list element
            list_inner_text = extract_tag_text(list_elem)

            # Clean up the children of the list element
            for child in list_elem.getchildren():
                # Remove each child element from its parent
                if child.getparent() is not None:
                    child.drop_tree()

            # Set the extracted text as the text content of the list element
            list_elem.text = list_inner_text

    # Return the modified root element
    return root