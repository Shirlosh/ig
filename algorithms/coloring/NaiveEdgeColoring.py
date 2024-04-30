from classes.graphs.Graph import Graph


def NaiveEdgeColoring(g: Graph):
    colors, maxColor = {}, 1
    for e in g.Edges.values():
        adjColors = lambda vID: {colors[a.ID] for a in g.AdjacentEdgeList(vID) if colors.get(a.ID, None)}
        c = min(set(range(1, maxColor + 2)) - (adjColors(e.Source.ID) | adjColors(e.Target.ID)))
        maxColor = c if c > maxColor else maxColor
        colors[e.ID] = c

    return {'colors': colors, 'size': maxColor}
