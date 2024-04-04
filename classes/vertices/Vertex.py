from classes.abstracts.Identifiable import Identifiable
from classes.abstracts.Mutable import Mutable


class Vertex(Identifiable, Mutable):

    def __init__(self, ID=None):
        super().__init__(ID)

    def Copy(self, ID=None):
        copy = self.__class__.__init__(self, ID if ID else self.ID)
        copy.__dict__.update(self.__dict__)
        return copy
