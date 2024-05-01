from classes.graphs.Graph import Graph


def VertexColoring(g: Graph):
    vertices, colors, color = g.Vertices.copy(), {}, 1
    while vertices:
        sortedV = dict(sorted(vertices.items(), key=lambda x: g.Degree(x[0]), reverse=True))
        while sortedV:
            colors[vID := next(iter(sortedV))] = color
            sortedV.pop(vID, None), [sortedV.pop(uID, None) for uID in g.Neighbors(vID)]
            vertices.pop(vID)
        color += 1
    return {'colors': colors, 'size': color - 1}


