import sys
from queue import PriorityQueue
from inograph.classes.graphs.Graph import Graph


def Dijkstra(g: Graph, fromSet, *, directed='None', weightFunction=lambda e: 1):
    """
    :param g: Graph type
    :param fromSet: set of the sources id's
    :param directed: 'Into' (all path into source vertex) / 'From' (all paths from source vertex) / None (indirect)
    :param weightFunction: function from edge to edge weight
    :return: paths dictionary - {sourceID : {targetID [path to the target-edges list)]}
    """
    EdgesSubsetType = {'Into': 'IncomingEdgeList', 'From': 'OutgoingEdgeList', 'None': 'AdjacentEdgeList'}[directed]
    def reversePath(path):
        path.reverse()
        return path
    return {v.ID: {k: (reversePath(path) if directed == 'Into' else path) for k, path in
                   __dijkstra(g, v.ID, EdgesSubsetType, weightFunction).items()} for v in fromSet}


def __dijkstra(g: Graph, srcID, EdgesSubsetType, weightFunction):
    D = {vID: sys.maxsize for vID in g.Vertices}
    visited = {vID: False for vID in g.Vertices}
    D[srcID] = 0
    pathList = {}
    pq = PriorityQueue()
    pq.put((D[srcID], srcID))
    while not pq.empty():
        (dist, vID) = pq.get()
        visited[vID] = True
        for edge in getattr(g, EdgesSubsetType)(vID):
            neighbor = edge.Source if edge.Source.ID != vID else edge.Target
            if not visited[neighbor.ID]:
                distance = D[vID] + weightFunction(edge.ID)
                if distance < D[neighbor.ID]:
                    pq.put((distance, neighbor.ID))
                    D[neighbor.ID] = distance
                    if pathList.get(vID) is None:
                        pathList[neighbor.ID] = [edge.ID]
                    else:
                        pathList[neighbor.ID] = pathList[vID] + [edge.ID]
    return pathList
