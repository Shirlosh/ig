from classes.abstracts.Mappable import Mappable
from modules.data.dictionaries import ListDictionaryValues
from classes.edges.Edge import Edge
from classes.vertices.Vertex import Vertex


class Graph(Mappable):
    """
    A class for graph structure. Can be used as multigraph as well.
    """
    def __init__(self, *, multigraph: bool = False):
        self.__edges, self.__vertices = {}, {}
        self._multigraph = multigraph
        self.__adjacency = {}

    @property
    def Vertices(self):
        return self.__vertices

    @property
    def Edges(self):
        return self.__edges

    @property
    def Adjacency(self):
        return self.__adjacency

    @property
    def IsMultigraph(self):
        return self._multigraph

    def Vertex(self, ID):
        return self.__vertices.get(ID, None)

    def Edge(self, ID):
        return self.__edges.get(ID, None)

    def AddVertex(self, vertex: Vertex = None):
        """
        :param vertex: optional, will add the object to the set of vertices
        :return: the vertex added, or exception if vertex already exists
        """
        vertex = vertex if vertex else Vertex()
        if self.Vertex(vertex.ID):
            raise Exception("The graph already contains a vertex with this ID.")
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

    def AddEdge(self, edge: Edge):
        """
        Will add the object edge to the set of edges, throws exception if an edge with the same ID exists.
        Raises Exception if there is an edge between the vertices and _multigraph is False
        Raises an exception if the IDs of the endpoints of the given edge exist in the graph on different objects.
        :return: the edge added
        """
        if self.Edge(edge.ID):
            raise Exception("The graph already contains an edge with this ID.")
        if self.AreConnected(edge.Source.ID, edge.Target.ID) and not self._multigraph:
            raise Exception("Graph is not a multigraph and an edge already exists between vertices")
        v1, v2 = self.Vertex(edge.Source.ID), self.Vertex(edge.Target.ID)
        v1 = v1 if v1 else self.AddVertex(edge.Source)
        v2 = v2 if v2 else self.AddVertex(edge.Target)
        if v1 != edge.Source or v2 != edge.Target:
            raise Exception("IDs of endpoints already in the graph but on different objects. You can use .Connect with extendFrom= but the edge would not be the same object.")
        self.__edges[edge.ID] = edge
        if self.__adjacency[v1.ID].get(v2.ID, None) is None: self.__adjacency[v1.ID][v2.ID] = {}
        if self.__adjacency[v2.ID].get(v1.ID, None) is None: self.__adjacency[v2.ID][v1.ID] = {}
        self.__adjacency[v1.ID][v2.ID][edge.ID] = edge
        self.__adjacency[v2.ID][v1.ID][edge.ID] = edge
        return edge

    def RemoveEdge(self, edgeID):
        if e := self.__edges.pop(edgeID, None):
            v1, v2 = e.Vertices
            del self.__adjacency[v1.ID][v2.ID][edgeID]
            self._removeEmptyConnection(self.__adjacency, v1.ID, v2.ID)
            del self.__adjacency[v2.ID][v1.ID][edgeID]
            self._removeEmptyConnection(self.__adjacency, v2.ID, v1.ID)
        return e

    def Connect(self, vertex1ID, vertex2ID, *, extendFrom=None):
        """
        Adds an edge between two vertices according to their IDs.
        If a vertex with a given ID does not exist in the graph, a vertex with the ID will be created.
        :param extendFrom: An Extendable object from which properties will be copied to the new edge
        :return: the edge added
        """
        v1, v2 = self.Vertex(vertex1ID), self.Vertex(vertex2ID)
        e = Edge(v1 if v1 else Vertex(ID=vertex1ID), v2 if v2 else Vertex(ID=vertex2ID))
        if extendFrom: e.UpdateFromObject(extendFrom)
        return self.AddEdge(e)

    def GetBetween(self, vertex1ID, vertex2ID):
        """
        Returns edges between two vertices given their IDs.
        :return: an Edge if _multigraph is False. Returns a list of edges otherwise
        """
        if not (edgeMap := self.__adjacency.get(vertex1ID, {}).get(vertex2ID, None)): return None
        if self._multigraph: return list(edgeMap.values())
        return edgeMap[next(iter(edgeMap))]

    def AreConnected(self, vertex1ID, vertex2ID):
        return self.__adjacency.get(vertex1ID, {}).get(vertex2ID, None) is not None

    def AdjacentEdges(self, vertexID):
        """
        :return: a dictionary of the form {Vertex.ID: {Edge.ID: Edge}} containing the adjacency of the vertex with ID vertexID.
        """
        return self.__adjacency.get(vertexID, None)

    def AdjacentEdgeList(self, vertexID):
        """
        :return: Create a list our of self.AdjacentEdges. Requires more time though.
        """
        if not (d := self.AdjacentEdges(vertexID)): return None
        return ListDictionaryValues(d)

    def Neighbors(self, vertexID):
        edges = self.AdjacentEdges(vertexID)
        return list(edges.keys()) if edges else None

    def Degree(self, vertexID):
        edges = self.AdjacentEdges(vertexID)
        return len(edges) if edges else None

    @property
    def GraphDegree(self):
        return max([self.Degree(vID) for vID in self.__vertices], default=0)

    def Copy(self, *, deep: bool = False):
        copy = type(self)(multigraph=self._multigraph)
        [copy.AddVertex(v.Copy() if deep else v) for v in self.Vertices.values()]
        [copy.AddEdge(e.Copy(deep) if deep else e) for e in self.Edges.values()]
        return copy

    def FromDictionary(self, data):
        for edge in data.get('Edges', {}).values():
            sData, tData = edge['Source'], edge['Target']
            source = Vertex(ID=sData['ID']).UpdateFromDictionary(sData)
            target = Vertex(ID=tData['ID']).UpdateFromDictionary(tData)
            self.AddEdge(Edge(source, target, ID=edge['ID'])).FromDictionary(edge)
        [self.Vertex(v['ID']).UpdateFromDictionary(v) for v in data.get('Vertices', {}).values()]
        return self

    @staticmethod
    def _removeEmptyConnection(d, v1ID, v2ID):
        if d[v1ID, {}].get(v2ID, None):
            del d[v1ID][v2ID]
