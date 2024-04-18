from classes.graphs.Graph import Graph


def BFS(g: Graph, fromSet, directed='None'):
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
                   _BFS(g, v.ID, EdgesSubsetType).items()} for v in fromSet}


def _BFS(g: Graph, srcID, EdgesSubsetType):
    visited = {key: False for key in g.Vertices.keys()}
    pathList = {}
    queue = [srcID]
    visited[srcID] = True
    while queue:
        vID = queue.pop(0)
        eds = getattr(g, EdgesSubsetType)(vID)
        for edge in eds:
            neighbor = edge.Source if edge.Source.ID != vID else edge.Target
            if not visited[neighbor.ID]:
                queue.append(neighbor.ID)
                visited[neighbor.ID] = True
                if pathList.get(vID) is None:
                    pathList[neighbor.ID] = [edge.ID]
                else:
                    pathList[neighbor.ID] = pathList[vID] + [edge.ID]
    return pathList
