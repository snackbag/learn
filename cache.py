from helper import millis
from i18n import I18NEngine
import database as db


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
        if key is None:
            return False

        get = self.get(key)
        if get is None:
            return False

        return True


class NothingCache(Cache):
    def cache(self, value, expiration: int = 300000) -> None:
        if not self.should_use(str(value)):
            self._cache[str(value)] = CacheEntry(None, expiration)
            return


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


class UserIDCache(Cache):
    user_check_cache = NothingCache()

    def cache(self, value: db.User, expiration: int = -1) -> None:
        self._cache[str(value.user_id)] = CacheEntry(str(value.user_id), expiration)
        self.user_check_cache.cache(str(value.user_id))
        return

    def should_use(self, key: str):
        value = super().should_use(key)

        if key == "None":
            return False

        if value is True:
            return True

        if not self.user_check_cache.should_use(key):
            query = db.session.query(db.User).filter_by(user_id=int(key)).first()
            if query is None:
                return False

            self.cache(query)
            return query is not None

        return value


class Globals:
    i18n_cache = I18NCache()
    user_id_cache = UserIDCache()
