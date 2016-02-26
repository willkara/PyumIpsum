import pickledb


class Cache(object):
    """
    The main Cache object. All different types of caches will extend this class.
    """

    def __init__(self):
        """
        Create an instance of a cache.
        :return:
        """
        self.cachedb = pickledb.load('pickle.db', False)

    def get(self, key):
        """
        Return the model(value) of a given key from the cache.
        :param key: The key to get and return the value of.
        :return: The value of the specified key.
        """
        return self.cachedb.get(key)

    def add(self, key, model):
        """
        Add a model(value) to the cache with a specified key.
        :param key: The key of the model(value) you wish to return. This is the subject/word of the model.
        :param model: The model object of the specified key.
        :return:
        """
        return self.cachedb.set(key, model)

    def get_total(self):
        total = 0
        for _ in self.cachedb.getall():
            total += 1
        return total
