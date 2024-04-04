from classes.abstracts.Identifiable import Identifiable
from classes.abstracts.Mutable import Mutable


class Vertex(Identifiable, Mutable):
    def __init__(self, ID=None):
        super().__init__(ID)
