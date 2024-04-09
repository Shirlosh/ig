from modules.data.dictionaries import ListDictionaryValues
from classes.edges.DirectedEdge import DirectedEdge
from classes.edges.Edge import Edge
from classes.graphs.Graph import Graph
from classes.vertices.Vertex import Vertex


class DirectedGraph(Graph):
    def __init__(self, *, multigraph: bool = False):
        super().__init__(multigraph=multigraph)
        self.__outgoingAdjacency, self.__incomingAdjacency = {}, {}

    def AddVertex(self, vertex: Vertex = None):
        """
        :param vertex: optional, will add the object to the set of vertices, overwrites if Vertex.ID already exists
        :return: the vertex added
        """
        v = super().AddVertex(vertex)
        self.__incomingAdjacency[vertex.ID], self.__outgoingAdjacency[vertex.ID] = {}, {}
        return v

    def RemoveVertex(self, vertexID):
        """
        Removes the vertex with ID vertexID and all adjacent edges
        :return: a tuple (v, es) where v is the vertex removed and es is the edges removed or None, None if vertex does not exist.
        """
        v, es = super().RemoveVertex(vertexID)
        if not v: return None, None
        [self.__incomingAdjacency[e.Target.ID][e.Source.ID].pop(e.ID)
         for e in es if e.Source.ID == vertexID]
        [self._removeEmptyConnection(self.__incomingAdjacency, e.Target.ID, e.Source.ID) for e in es]
        del self.__incomingAdjacency[v.ID]
        del self.__outgoingAdjacency[v.ID]
        return v, es

    def AddEdge(self, edge: DirectedEdge):
        """
        Will add the object edge to the set of edges, overwrites if edge.ID already exists.
        Overwrites the endpoints if the vertices already exist.
        :return: the edge added
        """
        super().AddEdge(edge)
        if self.__outgoingAdjacency[edge.Source.ID].get(edge.Target.ID, None) is None:
            self.__outgoingAdjacency[edge.Source.ID][edge.Target.ID] = {}
        if self.__incomingAdjacency[edge.Target.ID].get(edge.Source.ID, None) is None:
            self.__incomingAdjacency[edge.Target.ID][edge.Source.ID] = {}
        self.__outgoingAdjacency[edge.Source.ID][edge.Target.ID][edge.ID] = edge
        self.__incomingAdjacency[edge.Target.ID][edge.Source.ID][edge.ID] = edge
        return edge

    def RemoveEdge(self, edgeID) -> Edge:
        if e := super().RemoveEdge(edgeID):
            del self.__outgoingAdjacency[e.Source.ID][e.Target.ID][edgeID]
            self._removeEmptyConnection(self.__outgoingAdjacency, e.Source.ID, e.Target.ID)
            del self.__incomingAdjacency[e.Target.ID][e.Source.ID][edgeID]
            self._removeEmptyConnection(self.__incomingAdjacency, e.Target.ID, e.Source.ID)
        return e

    def Connect(self, vertex1ID, vertex2ID):
        """
        Adds an edge between two vertices according to their IDs.
        If a vertex with a given ID does not exist in the graph, a vertex with the ID will be created.
        Raises Exception if an edge exists and _multigraph is False
        :return: the edge added or a dictionary with the edges found
        """
        v1, v2 = self.Vertex(vertex1ID), self.Vertex(vertex2ID)
        return self.AddEdge(DirectedEdge(v1 if v1 else Vertex(ID=vertex1ID), v2 if v2 else Vertex(ID=vertex2ID)))

    def GetFromTo(self, vertex1ID, vertex2ID):
        """
        Returns edges from a vertex to another.
        :return: an Edge if _multigraph is False. Returns a list of edges otherwise
        """
        if not (edgeMap := self.__outgoingAdjacency.get(vertex1ID, {}).get(vertex2ID, None)): return None
        if self._multigraph: return list(edgeMap.values())
        return edgeMap[next(iter(edgeMap))]

    def AreConnectedFromTo(self, vertex1ID, vertex2ID):
        return self.__outgoingAdjacency.get(vertex1ID, {}).get(vertex2ID, None) is not None

    def OutgoingEdges(self, vertexID):
        """
        :return: a dictionary of the form {Vertex.ID: {Edge.ID: Edge}} containing the adjacency of the vertex with ID vertexID.
        """
        return self.__outgoingAdjacency.get(vertexID, None)

    def OutgoingEdgeList(self, vertexID):
        """
        :return: Create a list our of self.OutgoingEdges. Requires more time though.
        """
        if not (d := self.OutgoingEdges(vertexID)): return None
        return ListDictionaryValues(d)

    def IncomingEdges(self, vertexID):
        """
        :return: a dictionary of the form {Vertex.ID: {Edge.ID: Edge}} containing the adjacency of the vertex with ID vertexID.
        """
        return self.__incomingAdjacency.get(vertexID, None)

    def IncomingEdgeList(self, vertexID):
        """
        :return: Create a list our of self.IncomingEdges. Requires more time though.
        """
        if not (d := self.IncomingEdges(vertexID)): return None
        return ListDictionaryValues(d)

    def Targets(self, vertexID):
        """
        :return: All neighbors of the vertex with ID vertexID that have incoming edges from that vertex
        """
        adjacency = self.OutgoingEdges(vertexID)
        return [self.Vertex(vID) for vID in adjacency.keys()] if adjacency else []

    def Sources(self, vertexID):
        """
        :return: All neighbors of the vertex with ID vertexID that have outgoing edges towards that vertex
        """
        adjacency = self.IncomingEdges(vertexID)
        return [self.Vertex(vID) for vID in adjacency.keys()] if adjacency else []

    def OutDegree(self, vertexID):
        edges = self.OutgoingEdges(vertexID)
        return len(edges) if edges else None

    def InDegree(self, vertexID):
        edges = self.IncomingEdges(vertexID)
        return len(edges) if edges else None
