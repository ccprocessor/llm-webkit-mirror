class ParagraphTextType(object):
    TEXT = 'text'
    MARKDOWN = 'md'
    EQUATION_INLINE = 'equation-inline'
    CODE_INLINE = 'code-inline'


class DocElementType(object):
    PARAGRAPH = 'paragraph'
    LIST = 'list'
    SIMPLE_TABLE = 'simple_table'
    COMPLEX_TABLE = 'complex_table'
    EQUATION_INTERLINE = 'equation-interline'
    CODE = 'code'
    TITLE = 'title'

    EQUATION_INLINE = ParagraphTextType.EQUATION_INLINE

    IMAGE = 'image'
    AUDIO = 'audio'
    VIDEO = 'video'

    MM_NODE_LIST = [IMAGE, AUDIO, VIDEO]

    EXCLUDE_PLAIN_MD_LIST = [CODE, EQUATION_INTERLINE, IMAGE, COMPLEX_TABLE, AUDIO, VIDEO]
    EXCLUDE_PLAIN_MD_INLINE_LIST = [ParagraphTextType.EQUATION_INLINE, ParagraphTextType.CODE_INLINE]
