from inograph.classes.edges.Edge import Edge
from inograph.classes.graphs.DirectedGraph import DirectedGraph
from inograph.classes.vertices.Vertex import Vertex


class Forest(DirectedGraph):
    def __init__(self):
        super().__init__()
        self.__roots = {}

    @property
    def Roots(self):
        return self.__roots

    def IsRoot(self, vertexID):
        return self.__roots.get(vertexID, None) is not None

    def _AddEndpoint(self, vertex: Vertex = None):
        """
        Should be only use right before connecting the vertex to an edge!
        For adding vertices use .AddVertex!
        """
        v = super().AddVertex(vertex)
        return v

    def AddVertex(self, vertex: Vertex = None):
        v = super().AddVertex(vertex)
        self.__roots[v.ID] = v
        return v

    def RemoveVertex(self, vertexID):
        """
        Removes the vertex with ID vertexID and all adjacent edges
        :return: a tuple (v, es) where v is the vertex removed and es is the edges removed or None, None if vertex does not exist.
        """
        if children := self.Children(vertexID) is None: return None, None
        v, es = super().RemoveVertex(vertexID)
        for child in children: self.__roots[child.ID] = child
        return v, es

    def AddEdge(self, edge: Edge):
        """
        Will add the object edge to the set of edges
        Creates the endpoints if the vertices don't exist.
        Will not add the edge if it breaks a forest topology
        :return: the edge added
        """
        if self.Parent(edge.Target.ID): raise Exception("Cannot add an edge towards a vertex that already has a parent in a forest.")
        self.__roots.pop(edge.Target.ID, None)
        if not self.Vertex(edge.Source.ID): self._AddEndpoint(edge.Source)
        if not self.Vertex(edge.Target.ID): self._AddEndpoint(edge.Target)
        return super().AddEdge(edge)

    def RemoveEdge(self, edgeID):
        if not (e := super().RemoveEdge(edgeID)): return None
        self.__roots[e.Target.ID] = e.Target

    def Parent(self, vertexID):
        sources = self.Sources(vertexID)
        return sources[0] if sources else None

    def ParentEdge(self, vertexID):
        return self.GetFromTo(self.Parent(vertexID).ID, vertexID) if vertexID not in self.__roots else None

    def Children(self, vertexID):
        return self.Targets(vertexID)

    def AddSubtree(self, vertexID, subtree):
        """
        :param vertexID: the vertex which is to become the parent of the subtree
        :param subtree: The subtree to add as Tree.
        :return: the edge created between the parent vertex and the subtree
        """
        if not self.Vertex(vertexID): return None
        root = self._AddEndpoint(subtree.Root)
        edge = self.Connect(vertexID, root.ID)
        [self.AddEdge(e) for e in subtree.Edges.values()]
        return edge

    def AddTree(self, tree):
        self.AddVertex(tree.Root)
        [self.AddEdge(e) for e in tree.Edges.values()]
        return tree

    def RemoveSubtree(self, vertexID):
        return self.RemoveVertex(vertexID)

    def RemoveTree(self, rootID):
        return self.RemoveSubtree(rootID)

    def GetSubtree(self, rootID, *, deepcopy: bool = False):
        """
        :param rootID: the root ID of the subtree to return
        :param deepcopy: use if you want copies of the vertices and edge used in self
        :return: a Tree representing the required subtree. If the root does not exist, returns None
        """
        from inograph.classes.graphs.Tree import Tree
        if not (root := self.Vertex(rootID)): return None
        tree = Tree(root=(root.Copy() if deepcopy else root))
        edgesToAdd = self.OutgoingEdgeList(root.ID)
        while edgesToAdd:
            edge = edgesToAdd.pop(0)
            tree.AddEdge(edge)
            edgesToAdd.extend(self.OutgoingEdgeList(edge.Target.ID))
        return tree

    def GetTree(self, rootID, *, deepcopy: bool = False):
        return self.GetSubtree(rootID, deepcopy=deepcopy)

    def Ancestors(self, vertexID):
        """
        Returns the ancestors of a vertex with ID vertexID starting with the parent up to the root.
        Returns None if the vertex does not exist.
        """
        if not self.Vertex(vertexID): return None
        if vertexID in self.__roots: return []
        ancestors = [p := self.Parent(vertexID)]
        ancestors.extend(self.Ancestors(p.ID))
        return ancestors

    def Height(self, vertexID=None):
        if not self.Vertex(vertexID): return None
        return max([self.Height(child.ID)+1 for child in self.Children(vertexID)], default=0)

    def Depth(self, vertexID):
        if not self.Vertex(vertexID): return None
        if vertexID in self.__roots: return 0
        return self.Depth(self.Parent(vertexID)) + 1
