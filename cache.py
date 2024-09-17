from helper import millis
from i18n import I18NEngine


class CacheEntry:
    def __init__(self, value, expiration: int):
        """
        Cache entry for the cache
        :param value: the stored value
        :param expiration: the expiration time in milliseconds.
        """

        self.value = value
        self.creation = millis()
        self.expiration = expiration

    def has_expired(self):
        if self.expiration < 0:
            return False

        return self.creation + self.expiration < millis()

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
        self._cache: dict[str, CacheEntry] = {}

    def cache(self, value, expiration: int = 300000) -> None:
        raise NotImplementedError("This cache has not implemented caching")

    def get(self, key: str):
        get = self._cache.get(key)
        if get is None:
            return None

        return get.value_or_none()

    def is_cached(self, key: str):
        return self.get(key) is not None

    def should_use(self, key: str):
        get = self.get(key)
        if get is None:
            return False

        return True


class I18NCache(Cache):
    def cache(self, value: I18NEngine, expiration: int = 300000) -> None:
        if not self.should_use(value.language):
            self._cache[value.language] = CacheEntry(value, expiration)
            return

    def get_or_create(self, language: str) -> I18NEngine:
        if self.should_use(language):
            return self.get(language)

        engine = I18NEngine(language)
        engine.load()

        self.cache(engine)
        return engine


class Globals:
    i18n_cache = I18NCache()
