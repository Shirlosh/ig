from classes.graphs.Graph import Graph


def GreedyEdgeColoring(g: Graph):
    """
    Colors the edges of the graph in a greedy way. Faster than .EdgeColoring but uses potentially more colors.
    :return: {colors: {Edge.ID: int}, size: int}, where 'colors' is the map of colors and 'size' is the number of colors used.
    """
    colors, maxColor = {}, 1
    for e in g.Edges.values():
        adjColors = lambda vID: {colors[a.ID] for a in g.AdjacentEdgeList(vID) if colors.get(a.ID, None)}
        c = min(set(range(1, maxColor + 2)) - (adjColors(e.Source.ID) | adjColors(e.Target.ID)))
        maxColor = max(c, maxColor)
        colors[e.ID] = c
    return {'colors': colors, 'size': maxColor}


def EdgeColoring(g: Graph):
    """
    Colors the edges of the graph.
    :return: {colors: {Edge.ID: int}, size: int}, where 'colors' is the map of colors and 'size' is the number of colors used.
    """
    colors, maxColor = {}, -1
    for e in g.Edges.values():
        XID, fID = e.Source.ID, e.Target.ID
        fan = __findMaximalFan(g, XID, fID, colors)
        c, d = __findColor(g, XID, colors), __findColor(g, fan[-1], colors)
        cdPathLen = __findAndInvertCDPath(g, XID, c, d, colors)
        wIdx, w = __findWInFan(g, d, fan, colors) if cdPathLen else (len(fan) - 1, fan[-1])
        __rotateFan(g, XID, fan[: wIdx + 1], colors)
        colors[g.GetBetween(XID, w).ID] = d
        if d > maxColor: maxColor = d
    return {'colors': colors, 'size': maxColor}


def __findMaximalFan(g: Graph, xID, fID, colors):
    """
    :param g: Graph
    :param xID: the id the of the fan vertex
    :param fID: vrtex
    :param colors: {edge.ID: color} map
    :return: maximal fan
    """
    fan, newFans = [], [fID]
    while newFans:
        fan.extend(newFans)
        newFans = [vID for vID in g.Neighbors(xID) if vID not in fan and colors.get(eID := g.GetBetween(xID, vID).ID) is not None and __isColorFree(g, newFans[-1], colors[eID], colors)]
    return fan


def __findColor(g: Graph, vID, colors):
    """
    :param g: Graph
    :param vID: the id of the vertex we want to find the color
    :param colors: colors map {edgeID: color}
    :return: free color
    """
    c = 1
    while not __isColorFree(g, vID, c, colors): c += 1
    return c


def __isColorFree(g, vID, c, colors):
    for uID in g.Neighbors(vID):
        if c == colors.get(g.GetBetween(vID, uID).ID): return False
    return True


def __findAndInvertCDPath(g: Graph, xID, c, d, colors):
    """
    :param g: Graph
    :param xID: source vertex
    :param c: first color of the path
    :param d: second color of the path
    :return: length of the path
    """
    isPathMaximal = False
    visited, curID = {xID}, xID
    while not isPathMaximal:
        isPathMaximal = True
        for vID in g.Neighbors(curID):
            if d == colors.get(eID := g.GetBetween(curID, vID).ID) and vID not in visited:
                colors[eID] = c
                c, d = d, c
                visited.add(curID := vID)
                isPathMaximal = False
                break
    return len(visited) - 1


def __findWInFan(g: Graph, d, fan, colors):
    """
    :param g: Graph
    :param d: Color
    :param fan:
    :param colors: colors map {edge.ID: color}
    :return: w index in the fan , wID
    """
    for i, uID in enumerate(fan):
        if __isColorFree(g, uID, d, colors):
            return i, uID
    return -1, None


def __rotateFan(g: Graph, xID, fan, colors):
    """
    given a fan of a vertex x , assign the color of edge (x,f[i+1]) to the edge (x,f[i])
    :param g: Graph
    :param xID: id of vertex x
    :param fan:
    :param colors: colors map {edge.ID : color}
    """
    for uID, utID in zip(fan, fan[1:]):
        colors[g.GetBetween(xID, uID).ID] = colors[g.GetBetween(xID, utID).ID]

