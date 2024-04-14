from classes.edges.Edge import Edge
from classes.graphs.Forest import Forest
from classes.vertices.Vertex import Vertex


class Tree(Forest):
    def __init__(self, *, root: Vertex = None):
        super().__init__()
        if root: self.AddVertex(root)

    @property
    def Root(self):
        return self.Roots[next(iter(self.Roots))]

    def AddVertex(self, vertex: Vertex = None, *, parentID=None):
        """
        Adds a vertex as a child of a vertex with ID parentID. the parameter parentID is required!
        :return: the edge added to the tree between the vertex and its parent
        """
        if not self.Vertices: return super().AddVertex(vertex)
        if not parentID: raise Exception("Must provide a parent vertex ID for Tree.AddVertex.")
        if not self.Vertex(parentID): raise Exception("Parent provided at Tree.AddVertex does not exist.")
        return self.Connect(parentID, super()._AddEndpoint(vertex).ID)

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

    def AddEdge(self, edge: Edge):
        """
        Will add the object edge to the set of edges, overwrites if edge.ID already exists.
        Overwrites the endpoints if the vertices already exist.
        Will not add the edge if it breaks a tree topology
        :return: the edge added
        """
        v = self.Vertex(edge.Target.ID)
        if v and self.Parent(v.ID): raise Exception("Adding an edge towards a vertex with a parent would create either circles or multiple parents to a single vertex.")
        return super().AddEdge(edge)

    def RemoveEdge(self, edgeID):
        """
        Removes the edge with ID edgeID.
        The entire subtree under the edge will be removed as well.
        :return: The subtree removed or None if the edge does not exist
        """
        e = self.Edge(edgeID)
        return self.RemoveVertex(e.Target.ID) if e else None
