from classes.graphs.Graph import Graph


def MaximalMatching(g: Graph):
    unmatched, matching = g.Vertices.keys(), {}
    while unmatched:
        vID = unmatched.pop(next(iter(unmatched)))
        friends = [uID for uID in g.Neighbors(vID) if unmatched[uID]]
        if friends:
            fID = friends[0]
            matching[vID], matching[fID] = fID, vID
            del unmatched[fID]
    return matching
