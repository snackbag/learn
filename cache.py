from helper import millis
from i18n import I18NEngine


class CacheEntry:
    def __init__(self, value, expiration: int = 300000):
        """
        Cache entry for the cache
        :param value: the stored value
        :param expiration: the expiration time in milliseconds. default is 5 minutes
        """

        self.value = value
        self.creation = millis()
        self.expiration = expiration

    def has_expired(self):
        return self.creation + self.expiration > millis()

    def value_or_none(self):
        """
        A function to get the value if it is not expired
        :return: the value or none
        """

        if not self.has_expired():
            return self.value
        return None


class Cache:
    def __init__(self):
        self.__cache: dict[str, CacheEntry] = {}

    def cache(self, value, expiration: int | None = None) -> None:
        raise NotImplementedError("This cache has not implemented caching")

    def get(self, key: str):
        return self.__cache.get(key).value_or_none()

    def is_cached(self, key: str):
        return self.get(key) is not None


class I18NCache(Cache):
    def cache(self, value: I18NEngine, expiration: int | None = None) -> None:
        if not self.is_cached(value.language):
            self.__cache[value.language] = CacheEntry(value)
            return

        if self.get(value.language).has_expired():
            self.__cache[value.language] = CacheEntry(value)
            return


class Globals:
    i18n_cache = I18NCache()