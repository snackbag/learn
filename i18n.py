import json
from pathlib import Path


class I18NEngine:
    fallback_path = Path(f"lang/en_us.json")

    def __init__(self, language: str):
        self.language = language
        self.__keys = {}
        self.__loaded = False

    def load(self):
        if self.__loaded:
            raise Exception("I18N is already loaded to language " + self.language)

        # Load fallback language
        if I18NEngine.fallback_path.is_file():
            with open(I18NEngine.fallback_path) as f:
                self.__load_from_file(f, True)

        # Load required language
        if self.lang_path().is_file():
            with open(self.lang_path()) as f:
                self.__load_from_file(f, False)

        self.__loaded = True

    def lang_path(self):
        return Path(f"lang/{self.language}.json")

    def __load_from_file(self, f, fallback: bool):
        data: dict = json.load(f)

        for key in data.keys():
            self.__keys[key] = {"value": data[key], "fallback": fallback}

    def get(self, key: str) -> str:
        if not self.__loaded:
            print(f"Trying to get value from unloaded I18N - {key=}, {self.language=}")

        get = self.__keys.get(key)
        if get is not None:
            if get["fallback"]:
                print(f"Getting '{key}' from fallback language instead of {self.language}")

            return get["value"]

        return key
