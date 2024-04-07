from abc import ABC


class Extendable(ABC):
    def __getattr__(self, prop):
        return None

    def ExtendFrom(self, obj: 'Extendable'):
        self.__dict__.update(obj.__dict__)
