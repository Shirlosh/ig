import itertools
import sys
from scipy.optimize import linear_sum_assignment
import numpy as np

from classes.graphs.BipartiteGraph import BipartiteGraph


def MinimumWeightMaxMatching(g: BipartiteGraph):
    """
    :param g: BipartiteGraph type each edge contains Weight property type vector
    :return: matches dictionary - {sourceID : targetID} , unmatched vertices list
    """
    matches, unmatched = {}, []
    weights = __costMatrix(g, A := {i: v for i, v in enumerate(sorted(list(g.GetLeftSet)))},
                              B := {i: v for i, v in enumerate(sorted(list(g.GetRightSet)))})
    res = linear_sum_assignment(weights)
    [matches.update({A[u]: B[v]}) if g.AreConnected(A[u], B[v]) else unmatched.append(A[u]) for v, u in zip(*res)]
    return matches, unmatched


def __costMatrix(g, A, B):
    weightLen = max([len(e.Weight) for e in g.Edges.values()])
    weightsVectors = {(i, j): g.GetBetween(u, v).Weight if g.AreConnected(u, v) else [np.inf] * weightLen for i, v in B.items() for j, u in A.items()}

    # sort the weight vector and give each vector a numeric cost
    costMatrix = [[None for _ in A] for _ in B]
    for cost, (c, tup) in enumerate(itertools.groupby(sorted(weightsVectors.items(), key=lambda t: t[1]), lambda t: t[1])):
        for (i, j), _ in list(tup):
            costMatrix[i][j] = cost if c[0] != np.inf else sys.maxsize
    return costMatrix
