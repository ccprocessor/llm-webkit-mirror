from lxml import html

from llm_web_kit.model.html_lib.base_func import document_fromstring, get_title
from llm_web_kit.model.html_lib.merge_tags import merge_list
from llm_web_kit.model.html_lib.modify_tags import (unwrap_single_child_tag,
                                                    wrap_bare_text)
from llm_web_kit.model.html_lib.remove_tags import (
    remove_all_tags, remove_blank_tags_recursive, remove_invisible_tags)
from llm_web_kit.model.html_lib.unwrap_tags import unwrap_all_tags


def general_simplify(root: html.HtmlElement) -> tuple[str, html.HtmlElement]:
    """Simplify HTML structure through multiple processing steps.

    Process an HTML element tree through a series of simplification operations including:
    - Removing invisible elements
    - Unwrapping unnecessary tags
    - Wrapping bare text
    - Removing specified tags
    - Merging list structures
    - Cleaning up empty tags

    Args:
        root: The root HtmlElement to process

    Returns:
        tuple: Contains:
            - str: Page title
            - HtmlElement: Simplified root element
    """
    # Get document title from meta tags or <title> tag
    title = get_title(root)

    # Remove tags with invisible content (script, style, etc.)
    root = remove_invisible_tags(root)

    # Remove wrapper tags while preserving their children
    # (e.g., convert <div><span>text</span></div> to <div>text</div>)
    root = unwrap_all_tags(root)

    # Wrap any loose text nodes in <span> tags to maintain structure integrity
    # Handles text directly in parent tags and tail text after child tags
    root = wrap_bare_text(root)

    # Remove tags from pre-defined blacklist (non-content-bearing tags)
    root = remove_all_tags(root)

    # Consolidate list structures by extracting text from nested children
    # (e.g., flatten complex list hierarchies)
    root = merge_list(root)

    # Recursively remove tags with empty content or whitespace-only content
    root = remove_blank_tags_recursive(root)

    # Remove redundant wrapper tags that only contain single child
    # (e.g., convert <div><p>text</p></div> to <p>text</p>)
    root = unwrap_single_child_tag(root)

    return title, root


def general_simplify_html_str(html_str: str) -> str:
    """Simplify raw HTML string using the general simplification pipeline.

    Args:
        html_str: Raw HTML string to process

    Returns:
        str: Simplified HTML string after processing

    Note:
        This is a convenience wrapper that handles HTML parsing and serialization
    """
    # Parse HTML string into element tree
    root = document_fromstring(html_str)
    
    # Apply simplification pipeline
    _, simplified_root = general_simplify(root)
    
    # Serialize processed element tree back to HTML string
    simplified_html_str = html.tostring(simplified_root)
    return simplified_html_str.decode("utf-8")
