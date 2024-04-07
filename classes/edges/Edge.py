from classes.abstracts.Identifiable import Identifiable
from classes.abstracts.Extendable import Extendable
from classes.vertices import Vertex


class Edge(Identifiable, Extendable):
    def __init__(self, v1: Vertex, v2: Vertex, *, ID=None):
        super().__init__(ID)
        self.__vertices = (v1, v2)

    @property
    def Vertices(self) -> tuple:
        return self.__vertices

    def Copy(self, *, deep: bool = False):
        vs = tuple(v.Copy() for v in self.__vertices) if deep else self.__vertices
        copy = type(self)(*vs, self.ID)
        copy.__dict__ = {**self.__dict__, **copy.__dict__}
        return copy
