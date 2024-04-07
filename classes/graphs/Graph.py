from classes.edges.Edge import Edge
from classes.vertices.Vertex import Vertex


class Graph:
    """
    A class for graph structure. Can be used as multigraph as well.
    """
    def __init__(self, *, multigraph: bool = False):
        self.__edges, self.__vertices = {}, {}
        self._multigraph = multigraph
        self.__adjacency = {}

    @property
    def Vertices(self) -> dict:
        return self.__vertices

    @property
    def Edges(self) -> dict:
        return self.__edges

    @property
    def Adjacency(self) -> dict:
        return self.__adjacency

    @property
    def IsMultigraph(self):
        return self._multigraph

    def Vertex(self, ID):
        return self.__vertices.get(ID, None)

    def Edge(self, ID):
        return self.__edges.get(ID, None)

    def AddVertex(self, vertex: Vertex = None) -> Vertex:
        """
        :param vertex: optional, will add the object to the set of vertices, overwrites if Vertex.ID already exists
        :return: the vertex added
        """
        vertex = vertex if vertex else Vertex()
        self.__vertices[vertex.ID] = vertex
        self.__adjacency[vertex.ID] = {}
        return vertex

    def RemoveVertex(self, vertexID):
        """
        Removes the vertex with ID vertexID and all adjacent edges
        :return: a tuple (v, es) where v is the vertex removed and es is the edges removed or None, None if vertex does not exist.
        """
        if not (v := self.Vertex(vertexID)): return None, None
        es = [self.RemoveEdge(eID)
              for edgeMap in self.AdjacentEdges(v.ID).values()
              for eID in edgeMap]
        del self.__adjacency[v.ID]
        del self.__vertices[v.ID]
        return v, es

    def AddEdge(self, edge: Edge) -> Edge:
        """
        Will add the object edge to the set of edges, overwrites if edge.ID already exists.
        Overwrites the endpoints if the vertices already exist.
        Raises Exception if there is an edge between the vertices and __multigraph is False
        :return: the edge added
        """
        if self.AreConnected(edge.Vertices[0], edge.Vertices[1]) and not self._multigraph:
            raise Exception("Graph is not a multigraph and an edge already exists between vertices")
        self.AddVertex(v1 := edge.Vertices[0])
        self.AddVertex(v2 := edge.Vertices[1])
        self.__edges[edge.ID] = edge
        if self.__adjacency[v1.ID].get(v2.ID, None) is None:
            self.__adjacency[v1.ID][v2.ID] = {}
        if self.__adjacency[v2.ID].get(v1.ID, None) is None:
            self.__adjacency[v2.ID][v1.ID] = {}
        self.__adjacency[v1.ID][v2.ID][edge.ID] = edge
        self.__adjacency[v2.ID][v1.ID][edge.ID] = edge
        return edge

    def RemoveEdge(self, edgeID) -> Edge:
        if e := self.__edges.pop(edgeID, None):
            v1, v2 = e.Vertices
            del self.__adjacency[v1.ID][v2.ID][edgeID]
            self._removeEmptyConnection(self.__adjacency, v1.ID, v2.ID)
            del self.__adjacency[v2.ID][v1.ID][edgeID]
            self._removeEmptyConnection(self.__adjacency, v2.ID, v1.ID)
        return e

    def Connect(self, vertex1ID, vertex2ID) -> Edge:
        """
        Adds an edge between two vertices according to their IDs.
        If a vertex with a given ID does not exist in the graph, a vertex with the ID will be created.
        Raises Exception if an edge exists and __multigraph is False
        :return: the edge added or a dictionary with the edges found
        """
        v1, v2 = self.Vertex(vertex1ID), self.Vertex(vertex2ID)
        return self.AddEdge(Edge(v1 if v1 else Vertex(ID=vertex1ID), v2 if v2 else Vertex(ID=vertex2ID)))

    def GetBetween(self, vertex1ID, vertex2ID) -> Edge | list | None:
        """
        Returns edges between two vertices given their IDs.
        :return: an Edge if __multigraph is False. Returns a list of edges otherwise
        """
        if not (edgeMap := self.__adjacency.get(vertex1ID, {}).get(vertex2ID, None)): return None
        if self._multigraph: return edgeMap.values()
        return edgeMap[next(iter(edgeMap))]

    def AreConnected(self, vertex1ID, vertex2ID):
        return self.__adjacency.get(vertex1ID, {}).get(vertex2ID, None) is not None

    def AdjacentEdges(self, vertexID) -> dict | None:
        """
        :return: a dictionary of the form {Vertex.ID: {Edge.ID: Edge}} containing the adjacency of the vertex with ID vertexID.
        """
        return self.__adjacency.get(vertexID, None)

    def Neighbors(self, vertexID) -> set:
        edges = self.AdjacentEdges(vertexID)
        return set(edges.keys()) if edges else None

    def Degree(self, vertexID):
        edges = self.AdjacentEdges(vertexID)
        return len(edges) if edges else None

    @property
    def GraphDegree(self):
        return max([self.Degree(v.ID) for v in self.__vertices])

    def _removeEmptyConnection(self, d, v1ID, v2ID):
        if d[v1ID, {}].get(v2ID, None):
            del d[v1ID][v2ID]
