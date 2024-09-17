import json
from pathlib import Path


class I18NEngine:
    def __init__(self, language: str):
        self.language = language
        self.__keys = {}
        self.__loaded = False

    def load(self):
        if self.__loaded:
            raise Exception("I18N is already loaded to language " + self.language)

        # Load fallback language
        with open(Path(f"lang/en_us.json")) as f:
            self.__load_from_file(f)

        # Load required language
        with open(Path(f"lang/{self.language}.json")) as f:
            self.__load_from_file(f)

        self.__loaded = True

    def __load_from_file(self, f):
        data: dict = json.load(f)

        for key in data.keys():
            self.__keys[key] = data[key]

    def get(self, key: str) -> str:
        if not self.__loaded:
            print(f"Trying to get value from unloaded I18N - {key=}, {self.language=}")

        get = self.__keys.get(key)
        if get is not None:
            return get

        return key
