import uuid
from abc import ABC


class Identifiable(ABC):

    def __init__(self, ID=None):
        self.__ID = ID if ID else uuid.uuid4().hex

    @property
    def ID(self):
        return self.__ID
