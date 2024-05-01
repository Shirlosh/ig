import uuid
from abc import ABC


class Identifiable(ABC):
    def __init__(self, ID=None):
        self.__ID = ID if ID is not None and ID is not False else uuid.uuid4().hex

    @property
    def ID(self):
        return self.__ID

    def generateNewID(self):
        self.__ID = uuid.uuid4().hex
