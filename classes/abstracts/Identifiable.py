from abc import ABC
from modules.Utility import UUID


class Identifiable(ABC):
    def __init__(self, ID=None):
        self.__ID = ID if ID else UUID()

    @property
    def ID(self):
        return self.__ID
