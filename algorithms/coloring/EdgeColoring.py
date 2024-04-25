from classes.graphs.Graph import Graph


def EdgeColoring(g: Graph):
    colors, maxColor  = {}, -1
    for e in g.Edges.values():
        XID, fID = e.Source.ID, e.Target.ID
        fan = __findMaximalFan(g, XID, fID, colors)
        c, d = __findColorsCD(g, XID, fan, colors)
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
    fan = [fID]
    isMaximal = False
    lastV = fID
    while not isMaximal:
        isMaximal = True
        for vID in g.Neighbors(xID):
            eID = g.GetBetween(xID, vID).ID
            if vID not in fan and colors.get(eID) is not None and __isColorFree(g, lastV, colors[eID], colors):
                fan.append(lastV := vID)
                isMaximal = False
    return fan


def __findColorsCD(g: Graph, x, fan, colors): # graph vertex vertex
    c = d = 1
    while not __isColorFree(g, x, c, colors):
        c += 1
    while not __isColorFree(g, fan[-1], d, colors):
        d += 1
    return c, d


def __isColorFree(g, vID, c, colors):
    for uID in g.Neighbors(vID):
        if c == colors.get(g.GetBetween(vID, uID).ID):
            return False
    return True


def __findAndInvertCDPath(g: Graph, xID, c, d, colors):  # vertex color, color
    isPathMaximal = False
    visited = {xID}
    curID = xID
    while not isPathMaximal:
        isPathMaximal = True
        for vID in g.Neighbors(curID):
            if d == colors.get(eID := g.GetBetween(curID, vID).ID) and vID not in visited:
                colors[eID] = c
                curID = vID
                c, d = d, c
                isPathMaximal = False
                visited.add(vID)
                break
    return len(visited) - 1


def __findWInFan(g: Graph, d, fan, colors):  # color, fan, colors
    """
    :param g: Graph
    :param d: Color
    :param fan:
    :param colors: colors map
    :return:
    """
    for i, uID in enumerate(fan):
        if __isColorFree(g, uID, d, colors):
            return i, uID
    return -1, None


def __rotateFan(g: Graph, xID, fan, colors):
    for uID, utID in zip(fan, fan[1:]):
        colors[g.GetBetween(xID, uID).ID] = colors[g.GetBetween(xID, utID).ID]

