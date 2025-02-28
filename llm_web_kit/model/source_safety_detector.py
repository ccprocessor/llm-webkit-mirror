class SourceFilter:
    def __init__(self):
        pass

    def filter(
        self, content_str: str, language: str, language_details: str, content_style: str
    ) ->  dict:
        """Predict the quality score of the content and filter out score below
        the threshold First, check if the language and content_style are
        supported Then get the quality model and threshold, and predict the
        quality score of the content Finally, return the result of whether the
        content should be filtered out.

        Args:
            content_str (str): the content string
            language (str): the language of the content
            language_details (str): the details of the language
            content_style (str): the content style of the content

        Raises:
            TODO use custom exception instead of
            ValueError: raise ValueError if the language and content_style are not supported

        Returns:
            bool: True if the content should remain, False if the content should be filtered out
        """
        # if not self.check_supported(language, content_style):
        #     # TODO move the exception to the upper level
        #     raise ValueError(
        #         f"Unsupport language '{language}' with content_style '{content_style}'"
        #     )
        # else:
            # model, threshold = get_quality_model(language, content_style)
            # prob = model.predict_with_content(content_str, content_style)
            # return prob > threshold, {'quality_prob': prob}
            
        return {"from_safe_source":True,"from_domestic_source":True}
