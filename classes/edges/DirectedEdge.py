from classes.edges.Edge import Edge
from classes.vertices.Vertex import Vertex


class DirectedEdge(Edge):
    @property
    def Source(self):
        return self.Vertices[0]

    @property
    def Target(self):
        return self.Vertices[1]
