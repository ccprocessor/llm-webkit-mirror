class ParagraphTextType(object):
    TEXT = 'text'
    MARKDOWN = 'md'
    EQUATION_INLINE = 'equation-inline'


class DocElementType(object):
    PARAGRAPH = 'paragraph'
    LIST = 'list'
    TABLE = 'table'
    EQUATION_INTERLINE = 'equation-interline'
    CODE = 'code'
    TITLE = 'title'

    EQUATION_INLINE = ParagraphTextType.EQUATION_INLINE

    IMAGE = 'image'
    AUDIO = 'audio'
    VIDEO = 'video'

    MM_NODE_LIST = [IMAGE, AUDIO, VIDEO]
