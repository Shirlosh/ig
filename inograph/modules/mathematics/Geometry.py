from math import radians, sin, cos, asin, sqrt
import numpy as np


def ReverseVector(vector):
    return -vector[0], -vector[1]


def AngleBetweenVectors(vector1, vector2):
    a, b = np.array(vector1), np.array(vector2)
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    if norm == 0: return 0
    angle = np.arccos(np.clip(np.inner(a, b) / norm, -1.0, 1.0))
    return angle if np.cross(b, a) <= 0 else -angle


def GlobeDistance(locationA, locationB, *, radius: float = 6371.0):
    """
    :param locationA: tuple longitude, latitude
    :param locationB: tuple longitude, latitude
    :param radius: the radius of the sphere in kilometers. Default is the radius of the earth
    :return: The distance between the location on the sphere surface of the earth
    """
    lon1, lon2, lat1, lat2 = radians(locationA[0]), radians(locationB[0]), radians(locationA[1]), radians(locationB[1])
    a = sin((lon2 - lon1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lat2 - lat1) / 2) ** 2
    return 2.0 * asin(sqrt(a)) * radius
