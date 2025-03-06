class SourceFilter:
    def __init__(self):
        pass

    def filter(
        self,
        content_str: str,
        language: str,
        data_source: str,
        language_details: str,
        content_style: str,
    ) -> dict:
        return {'from_safe_source': False, 'from_domestic_source': False}
