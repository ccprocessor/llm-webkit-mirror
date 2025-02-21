
from llm_web_kit.input.datajson import DataJson
from llm_web_kit.input.file_format import FileFormatConstant


class FileTypeMatcher(object):
    """文件类型匹配器.

    Args:
        object (_type_): _description_
    """

    def is_md_format(self, data_json: DataJson) -> bool:
        """判断文件是否是md文件.

        Args:
            data_json (str): 文件路径

        Returns:
            bool: 如果是md文件返回True，否则返回False
        """
        return data_json.get_file_format().lower() in FileFormatConstant.MARKDOWN

    def is_txt_format(self, data_json: DataJson) -> bool:
        """判断文件是否是txt文件.

        Args:
            file_path (str): 文件路径
            data_json (DataJson): 输入的json数据

        Returns:
            bool: 如果是txt文件返回True，否则返回False
        """
        return data_json.get_file_format().lower() in FileFormatConstant.TXT

    def is_pdf_format(self, data_json: DataJson) -> bool:
        """判断文件是否是pdf文件.

        Args:
            file_path (str): 文件路径
            data_json (DataJson): 输入的json数据

        Returns:
            bool: 如果是pdf文件返回True，否则返回False
        """
        return data_json.get_file_format().lower() in FileFormatConstant.PDF

    def is_html_format(self, data_json: DataJson) -> bool:
        """判断文件是否是html文件.

        Args:
            file_path (str): 文件路径
            data_json (DataJson): 输入的json数据

        Returns:
            bool: 如果是html文件返回True，否则返回False
        """
        return data_json.get_file_format().lower() in FileFormatConstant.HTML

    def is_ebook_format(self, data_json: DataJson) -> bool:
        """Determine whether the file is an ebook file.

        Args:
            file_path (str): File Path.
            data_json (DataJson): Input json data.
        Returns:
            bool: If it is an ebook file, it returns True, otherwise it returns False
        """
        return data_json.get_file_format().lower() in FileFormatConstant.EBOOK
