from abc import ABC


class Extendable(ABC):
    def __getattr__(self, prop):
        return None
