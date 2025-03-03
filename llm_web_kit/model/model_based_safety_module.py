from typing import List, Tuple, Any, Type, TypeVar
from llm_web_kit.model.policical import PoliticalDetector, decide_political_by_prob
from llm_web_kit.model.porn_detector import BertModel as EnPornBertModel
from llm_web_kit.model.porn_detector import XlmrModel as ZhPornXlmrModel
from llm_web_kit.exception.exception import ModelInputException

I = TypeVar("I")  # input type
B = TypeVar("B")  # batch type


def check_type(arg_name: str, arg_value: Any, arg_type: Type):
    """check the type of the argument and raise TypeError if the type is not
    matched."""
    if not isinstance(arg_value, arg_type):
        # TODO change TypeError to custom exception
        raise TypeError(
            "The type of {} should be {}, but got {}".format(
                arg_name, arg_type, type(arg_value)
            )
        )


class ModelBasedSafetyDataPack:
    """The data pack for the model based safety module."""

    def __init__(self, content_str: str, language: str, language_details: str):

        self._dict = {}
        # the content of the dataset
        check_type("content_str", content_str, str)
        self._dict["content_str"] = content_str

        # the language of the content
        check_type("language", language, str)
        self._dict["language"] = language

        # the details of the language
        check_type("language_details", language_details, str)
        self._dict["language_details"] = language_details

        # the flag of the processed data should be remained or not
        self._dict["model_based_safety_remained"] = True

        # the details of the model based safety process
        self._dict["model_based_safety_infos"] = {}

    @classmethod
    def from_dict(cls, data: dict):
        new_data_pack = cls(
            content_str=data["content_str"],
            language=data["language"],
            language_details=data["language_details"],
        )
        new_data_pack._dict.update(data)
        return new_data_pack

    def as_dict(self) -> dict:
        return self._dict

    def set_process_result(
        self, model_based_safety_remained: bool, model_based_safety_infos: dict
    ) -> None:
        """set the process result of the model based safety module."""
        check_type("model_based_safety_remained", model_based_safety_remained, bool)
        check_type("model_based_safety_infos", model_based_safety_infos, dict)
        if model_based_safety_remained is False:
            self._dict["model_based_safety_remained"] = False
        self._dict["model_based_safety_infos"].update(model_based_safety_infos)

    def get_output(self) -> dict:
        """get the output of the data pack."""
        return {
            "model_based_safety_remained": self._dict["model_based_safety_remained"],
            "model_based_safety_infos": self._dict["model_based_safety_infos"],
        }


class ContentStrBatchModel:
    def __init__(self, model_config: dict):
        self.model_config = model_config

    def check_support(self, data_pack: ModelBasedSafetyDataPack) -> bool:
        raise NotImplementedError

    def preprocess(self, data_pack: ModelBasedSafetyDataPack) -> Tuple[dict, I]:
        if not self.check_support(data_pack):
            # use class name
            model_name = self.__class__.__name__
            raise ModelInputException(
                f"The data pack is not supported for {model_name}."
            )
        return data_pack.as_dict(), data_pack._dict["content_str"]

    def collate_fn(self, lst: List[Tuple[dict, I]]) -> Tuple[List[dict], B]:
        infos, batch = zip(*lst)
        return list(infos), list(batch)

    def inference(self, batch: B) -> List[dict]:
        """(batch: B) -> results"""
        raise NotImplementedError()

    def postprocess(self, info: dict, result: dict) -> ModelBasedSafetyDataPack:
        """(info: dict, result: dict) -> output"""
        # return {**info, **result}
        raise NotImplementedError()

    def process_one_core(
        self, data_pack: ModelBasedSafetyDataPack
    ) -> ModelBasedSafetyDataPack:
        info, batch = self.preprocess(data_pack)
        batch = self.collate_fn([(info, batch)])[1]
        results = self.inference(batch)
        return self.postprocess(info, results[0])

    def process_one(
        self, content_str: str, language: str, language_details: str
    ) -> dict:
        data_pack = ModelBasedSafetyDataPack(content_str, language, language_details)
        return self.process_one_core(data_pack).get_output()


class ZhEnPoliticalModel(ContentStrBatchModel):
    def __init__(self, model_config: dict):
        super().__init__(model_config)
        self.political_detect = PoliticalDetector(
            model_path=model_config["model_path"],
        )
        self.threshold = model_config["threshold"]

    def check_support(self, data_pack: ModelBasedSafetyDataPack) -> bool:
        return data_pack.language in ["zh", "en"]

    def inference(self, batch: List[str]) -> List[dict]:
        result_list = []
        for content_str in batch:
            predictions, probabilities = self.political_detect.predict(content_str)
            normal_score = decide_political_by_prob(predictions, probabilities)
            result_list.append(
                {
                    "political_prob": normal_score,
                    "political_info": {
                        "predictions": predictions,
                        "probabilities": probabilities,
                    },
                }
            )
        return result_list

    def postprocess(self, info: dict, result: dict) -> dict:
        remained = result["political_prob"] > self.threshold
        datapack = ModelBasedSafetyDataPack.from_dict(info)
        datapack.set_process_result(
            model_based_safety_remained=remained, model_based_safety_infos=result
        )
        return datapack


class EnPronModel(ContentStrBatchModel):
    def __init__(self, model_config: dict):
        super().__init__(model_config)
        self.model = EnPornBertModel(model_config["model_path"])
        self.threshold = model_config["threshold"]

    def check_support(self, data_pack: ModelBasedSafetyDataPack) -> bool:
        return data_pack.language == "en"

    def inference(self, batch: List[str]) -> List[dict]:
        result_list = []
        for content_str in batch:
            prob = self.model.predict(content_str)
            result_list.append(prob)
        return result_list

    def postprocess(self, info: dict, result: dict) -> dict:
        porn_prob = list(result[0].values())[0]
        remained = porn_prob < self.threshold
        datapack = ModelBasedSafetyDataPack.from_dict(info)
        datapack.set_process_result(
            model_based_safety_remained=remained,
            model_based_safety_infos={"porn_prob": porn_prob},
        )
        return datapack
