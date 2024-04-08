from classes.edges.DirectedEdge import DirectedEdge
from classes.graphs.DirectedGraph import DirectedGraph
from classes.vertices.Vertex import Vertex


class Tree(DirectedGraph):
    def __init__(self, *, root: Vertex = None):
        super().__init__(multigraph=False)
        self.__root = root

    @property
    def Root(self):
        return self.__root

    def AddVertex(self, vertex: Vertex = None, *, parentID=None):
        """
        Adds a vertex as a child of a vertex with ID parentID. the parameter parentID is required!
        :return: the edge added to the tree between the vertex and its parent
        """
        if not parentID: raise Exception("Must provide a parent vertex ID for Tree.AddVertex.")
        if not self.Vertex(parentID): raise Exception("Parent provided at Tree.AddVertex does not exist.")
        v = super().AddVertex(vertex)
        return self.Connect(parentID, v.ID)

    def RemoveVertex(self, vertexID):
        """
        Removes the vertex with ID vertexID.
        The entire subtree rooted in the vertex will be deleted as well.
        :return: The subtree removed or None if the vertex does not exist
        """
        if not (root := self.Vertex(vertexID)): return None
        tree = Tree(root=root)
        [tree.AddSubtree(vertexID, self.RemoveSubtree(child.ID)) for child in self.Children(vertexID)]
        super().RemoveVertex(vertexID)
        return tree

    def AddEdge(self, edge: DirectedEdge):
        """
        Will add the object edge to the set of edges, overwrites if edge.ID already exists.
        Overwrites the endpoints if the vertices already exist.
        Will not add the edge if it breaks a tree topology
        :return: the edge added
        """
        if self.Vertex(edge.Target.ID):
            raise Exception("Adding an edge towards an existing vertex would create either circles or multiple parents to a single vertex.")
        return super().AddEdge(edge)

    def RemoveEdge(self, edgeID):
        """
        Removes the edge with ID edgeID.
        The entire subtree under the edge will be removed as well.
        :return: The subtree removed or None if the edge does not exist
        """
        e = self.Edge(edgeID)
        return self.RemoveVertex(e.Target.ID) if e else None

    def Parent(self, vertexID):
        return self.Sources(vertexID)[0] if vertexID != self.__root.ID else None

    def ParentEdge(self, vertexID):
        return self.GetFromTo(self.Parent(vertexID).ID, vertexID) if vertexID != self.__root.ID else None

    def Children(self, vertexID):
        return self.Targets(vertexID)

    def AddSubtree(self, vertexID, subtree):
        """
        :param vertexID: the vertex which is to become the parent of the subtree
        :param subtree: The subtree to add as Tree.
        :return: the edge created between the parent vertex and the subtree
        """
        if not self.Vertex(vertexID): return None
        root = self.AddVertex(subtree.Root)
        edge = self.Connect(vertexID, root.ID)
        [self.AddEdge(e) for e in subtree.Edges.values()]
        return edge

    def RemoveSubtree(self, vertexID):
        return self.RemoveVertex(vertexID)

    def GetSubtree(self, rootID, *, deepcopy: bool = False):
        """
        :param rootID: the root ID of the subtree to return
        :param deepcopy: use if you want copies of the vertices and edge used in self
        :return: a Tree representing the required subtree. If the root does not exist, returns None
        """
        if not (root := self.Vertex(rootID)): return None
        tree = Tree(root=(root.Copy() if deepcopy else root))
        edgesToAdd = self.OutgoingEdgeList(root.ID)
        while edgesToAdd:
            edge = edgesToAdd.pop(0)
            tree.AddEdge(edge)
            edgesToAdd.extend(self.OutgoingEdgeList(edge.Target.ID))
        return tree

    def Ancestors(self, vertexID):
        """
        Returns the ancestors of a vertex with ID vertexID starting with the parent up to the root.
        Returns None if the vertex does not exist.
        """
        if not self.Vertex(vertexID): return None
        if vertexID == self.__root.ID: return []
        ancestors = [p := self.Parent(vertexID)]
        ancestors.extend(self.Ancestors(p.ID))
        return ancestors

    def Height(self, vertexID=None):
        if not self.Vertex(vertexID): return None
        return max([self.Height(child.ID)+1 for child in self.Children(vertexID)], default=0)

    def Depth(self, vertexID):
        if not self.Vertex(vertexID): return None
        if self.__root.ID == vertexID: return 0
        return self.Depth(self.Parent(vertexID)) + 1
