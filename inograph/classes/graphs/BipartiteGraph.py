from inograph.classes.edges.Edge import Edge
from inograph.classes.graphs.Graph import Graph
from inograph.classes.vertices.Vertex import Vertex


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
        if setType == 'left': return self.AddLeftVertex(vertex)
        if setType == 'right': return self.AddRightVertex(vertex)
        raise Exception("setType must be left/right at BipartiteGraph.AddVertex.")

    def AddLeftVertex(self, vertex: Vertex = None):
        v = super().AddVertex(vertex)
        self.__leftSet[v.ID] = v
        return v

    def AddRightVertex(self, vertex: Vertex = None):
        v = super().AddVertex(vertex)
        self.__rightSet[v.ID] = v
        return v

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
        """
        Will add the edge only if both vertices are in the bipartite graph and not in the same set.
        Use .Connect/.ConnectFromLeft/.ConnectFromRight to quickly add edges for non-existing vertices.
        :return: The edge added
        """
        vs = edge.Vertices
        if (self.LeftVertex(vs[0].ID) and self.LeftVertex(vs[1].ID)) or \
                (self.RightVertex(vs[0].ID) and self.RightVertex(vs[1].ID)):
            raise Exception("Cannot add an edge inside the same set of vertices in a bipartite graph.")
        return super().AddEdge(edge)

    def Connect(self, vertex1ID, vertex2ID, *, extendFrom=None, fromSet=None):
        """
        Adds an edge between two vertices according to their IDs.
        If a vertex with a given ID does not exist in the graph, a vertex with the ID will be created.
        :param extendFrom: An Extendable object from which properties will be copied to the new edge
        :param fromSet: if both IDs do not exist as vertices in the graph, this must be specified for siding the new vertices
        :return: The added edge
        """
        if fromSet == 'left' or self.LeftVertex(vertex1ID) or self.RightVertex(vertex2ID):
            if self.RightVertex(vertex1ID): raise Exception("Left vertex exists in right set.")
            FromSideV, ToSideV = self.LeftVertex, self.RightVertex
            AddFromV, AddToV = self.AddLeftVertex, self.AddRightVertex
        elif fromSet == 'right' or self.RightVertex(vertex1ID) or self.LeftVertex(vertex2ID):
            if self.LeftVertex(vertex1ID): raise Exception("Right vertex exists in left set.")
            FromSideV, ToSideV = self.RightVertex, self.LeftVertex
            AddFromV, AddToV = self.AddRightVertex, self.AddLeftVertex
        else: raise Exception('.Connect is vague. Must receive ID of at least one existing vertex or fromSet specified.')
        if not FromSideV(vertex1ID): AddFromV(Vertex(ID=vertex1ID))
        if not ToSideV(vertex1ID): AddToV(Vertex(ID=vertex2ID))
        return super().Connect(vertex1ID, vertex2ID, extendFrom=extendFrom)

    def ConnectFromLeft(self, vertex1ID, vertex2ID, *, extendFrom=None):
        self.Connect(vertex1ID, vertex2ID, extendFrom=extendFrom, fromSet='left')

    def ConnectFromRight(self, vertex1ID, vertex2ID, *, extendFrom=None):
        self.Connect(vertex1ID, vertex2ID, extendFrom=extendFrom, fromSet='right')
