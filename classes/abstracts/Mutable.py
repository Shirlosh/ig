from abc import ABC


class Mutable(ABC):

    def __getattr__(self, prop):
        return None
