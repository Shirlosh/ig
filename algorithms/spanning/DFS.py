from classes.graphs.Graph import Graph


def DFS(g: Graph, fromSet, directed='None'):
    """
    :param g: Graph type
    :param fromSet: set of the sources id's
    :param directed: 'Into' (all path into source vertex) / 'From' (all paths from source vertex) / None (indirect)
    :return: paths dictionary - {sourceID : {targetID [path to the target-edges list)]}
    """
    EdgesSubsetType = {'Into': 'IncomingEdgeList', 'From': 'OutgoingEdgeList', 'None': 'AdjacentEdgeList'}[directed]

    def reversePath(path):
        path.reverse()
        return path

    return {v.ID: {k: (reversePath(path) if directed == 'Into' else path) for k, path in
                   _DFS(g, v.ID, EdgesSubsetType).items()} for v in fromSet}


def _DFS(g: Graph, srcID, EdgesSubsetType):
    visited = {key: False for key in g.Vertices.keys()}
    pathList = {}
    visited[srcID] = True
    queue = [srcID]

    def rec(vID):
        for edge in getattr(g, EdgesSubsetType)(vID):
            neighbor = edge.Source if edge.Source.ID != vID else edge.Target
            if not visited[neighbor.ID]:
                queue.insert(0, neighbor.ID)
                visited[neighbor.ID] = True
                pathList[neighbor.ID] = [edge.ID] if pathList.get(vID) is None else pathList[vID] + [edge.ID]
                rec(neighbor.ID)

    while queue:
        rec(queue.pop(0))

    return pathList
