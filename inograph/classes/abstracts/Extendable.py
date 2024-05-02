from abc import ABC


class Extendable(ABC):
    def __getattr__(self, prop):
        return None

    def UpdateFromDictionary(self, data):
        self.__dict__.update(data)
        return self

    def UpdateFromObject(self, obj: 'Extendable'):
        self.UpdateFromDictionary(obj.__dict__)
        return self
