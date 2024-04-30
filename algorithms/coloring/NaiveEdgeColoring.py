from classes.graphs.Graph import Graph


def NaiveEdgeColoring(g: Graph):
    colors, maxColor = {}, 1
    for e in g.Edges.values():
        adj = g.AdjacentEdgeList(e.Source.ID)
        a = {colors[a.ID] for a in adj if colors.get(a.ID, None)}
        adj = g.AdjacentEdgeList(e.Target.ID)
        b = {colors[a.ID] for a in adj if colors.get(a.ID, None)}
        used = a | b
        c = min(set(range(1, maxColor + 2)) - used)
        maxColor = c if c > maxColor else maxColor
        colors[e.ID] = c

    return {'colors': colors, 'size': maxColor}
