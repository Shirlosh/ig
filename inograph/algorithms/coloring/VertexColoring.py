from inograph.classes.graphs.Graph import Graph


def GreedyVertexColoring(g: Graph):
    """
    Colors the vertices of the graph in a greedy way. Faster than .VertexColoring but potentially uses more colors.
    :return: {colors: {Vertex.ID: int}, size: int}, where 'colors' is the map of colors and 'size' is the number of colors used.
    """
    colors, maxColor = {}, 1
    for vID in g.Vertices.keys():
        c = min(set(range(1, maxColor + 2)) - {colors[nID] for nID in g.Neighbors(vID) if colors.get(nID, None)})
        maxColor = c if c > maxColor else maxColor
        colors[vID] = c
    return {'colors': colors, 'size': maxColor}


def VertexColoring(g: Graph):
    """
    Colors the vertices of the graph.
    :return: {colors: {Vertex.ID: int}, size: int}, where 'colors' is the map of colors and 'size' is the number of colors used.
    """
    vertices, colors, color = g.Vertices.copy(), {}, 1
    while vertices:
        sortedV = dict(sorted(vertices.items(), key=lambda x: g.Degree(x[0]), reverse=True))
        while sortedV:
            colors[vID := next(iter(sortedV))] = color
            sortedV.pop(vID, None), [sortedV.pop(uID, None) for uID in g.Neighbors(vID)]
            vertices.pop(vID)
        color += 1
    return {'colors': colors, 'size': color - 1}
