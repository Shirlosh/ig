from inograph.classes.vertices.Vertex import Vertex


class Site(Vertex):
    def __init__(self, location: tuple[float, float], *, ID=None):
        super().__init__(ID=ID)
        self.__location = location

    @property
    def Location(self):
        return self.__location

    @Location.setter
    def Location(self, location: tuple[float, float]):
        self.__location = location
