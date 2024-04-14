from classes.abstracts.Identifiable import Identifiable
from classes.abstracts.Extendable import Extendable
from classes.abstracts.Mappable import Mappable


class Vertex(Identifiable, Extendable, Mappable):
    def __init__(self, *, ID=None):
        super().__init__(ID)

    def Copy(self):
        copy = type(self)(ID=self.ID)
        copy.__dict__ = {**self.__dict__, **copy.__dict__}
        return copy
