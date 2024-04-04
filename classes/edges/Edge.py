from classes.abstracts.Identifiable import Identifiable
from classes.vertices import Vertex


class Edge(Identifiable):

    def __init__(self, v1: Vertex, v2: Vertex, ID=None):
        super().__init__(ID)
        self.__vertices = {v1, v2}
