from classes.graphs.Graph import Graph


def NaiveVertexColoring(g: Graph):
    colors, maxColor = {}, 1
    for vID in g.Vertices.keys():
        c = min(set(range(1, maxColor + 2)) - {colors[nID] for nID in g.Neighbors(vID) if colors.get(nID, None)})
        maxColor = c if c > maxColor else maxColor
        colors[vID] = c

    return {'colors': colors, 'size': maxColor}
