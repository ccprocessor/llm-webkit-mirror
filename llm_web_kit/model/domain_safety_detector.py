class DomainFilter:
    def __init__(self):
        pass

    def filter(
        self,
        content_str: str,
        language: str,
        url: str,
        language_details: str,
        content_style: str,
    ) -> dict:
        return True, {}
