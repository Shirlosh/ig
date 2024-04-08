from classes.edges.Edge import Edge
from classes.graphs.Graph import Graph
from classes.vertices.Vertex import Vertex


class BipartiteGraph(Graph):
    def __init__(self, *, sets: tuple[dict, dict] = None):
        super().__init__()
        self.__leftSet, self.__rightSet = sets if sets else {}, {}

    @property
    def GetLeftSet(self):
        return self.__leftSet

    @property
    def GetRightSet(self):
        return self.__rightSet

    def LeftVertex(self, ID):
        return self.__leftSet.get(ID, None)

    def RightVertex(self, ID):
        return self.__leftSet.get(ID, None)

    def AddVertex(self, vertex: Vertex = None, *, setType: str = None):
        if setType == 'left': self.AddLeftVertex(vertex)
        if setType == 'right':
            self.AddRightVertex(vertex)
        else:
            raise Exception("setType must be left/right at BipartiteGraph.AddVertex.")

    def AddLeftVertex(self, vertex: Vertex = None):
        v = super().AddVertex(vertex)
        self.__leftSet[v.ID] = v

    def AddRightVertex(self, vertex: Vertex = None):
        v = super().AddVertex(vertex)
        self.__rightSet[v.ID] = v

    def RemoveVertex(self, vertexID):
        """
        Removes the vertex with ID vertexID and all adjacent edges
        :return: a tuple (v, es) where v is the vertex removed and es is the edges removed or None, None if vertex does not exist.
        """
        v, es = super().RemoveVertex(vertexID)
        if not v: return None, None
        del self.__leftSet[v.ID]
        del self.__rightSet[v.ID]
        return v, es

    def AddEdge(self, edge: Edge):
        vs = edge.Vertices
        if (self.LeftVertex(vs[0].ID) and self.LeftVertex(vs[1].ID)) or \
                (self.RightVertex(vs[0].ID) and self.RightVertex(vs[1].ID)):
            raise Exception("Cannot add an edge inside the same set of vertices in a bipartite graph.")
        return super().AddEdge(edge)
